#!/usr/bin/env python3
"""
Generate a local gamma exposure report from moomoo OpenD.

The report is intentionally opinionated: charts are evidence, while the
summary turns gamma structure into trading scenarios that can be combined
with the user's Strategy 2 indicators.
"""

from __future__ import annotations

import html
import argparse
import json
import math
import statistics
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

import sys

sys.path.insert(0, str(Path.home() / ".codex/skills/moomooapi/scripts"))
from common import AuType, KLType, RET_OK, Session, check_ret, create_quote_context, safe_close  # noqa: E402


DEFAULT_UNDERLYING = "US.BA"
REPORT_DIR = Path(__file__).resolve().parent


@dataclass
class OptionRow:
    code: str
    expiry: str
    option_type: str
    strike: float
    oi: int
    volume: int
    bid: float
    ask: float
    last: float
    iv: float
    delta: float
    gamma: float
    theta: float
    vega: float
    dte: float


def norm_float(value, default=0.0) -> float:
    try:
        if value is None:
            return default
        f = float(value)
        if math.isnan(f):
            return default
        return f
    except Exception:
        return default


def norm_int(value, default=0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def normal_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def black_scholes_gamma(spot: float, strike: float, iv: float, dte: float) -> float:
    """A zero-rate approximation is enough for locating walls/flip zones."""
    if spot <= 0 or strike <= 0 or iv <= 0:
        return 0.0
    t = max(dte, 0.25) / 365.0
    d1 = (math.log(spot / strike) + 0.5 * iv * iv * t) / (iv * math.sqrt(t))
    return normal_pdf(d1) / (spot * iv * math.sqrt(t))


def signed_gex(row: OptionRow, spot: float, use_model_gamma: bool = False) -> float:
    gamma = black_scholes_gamma(spot, row.strike, row.iv, row.dte) if use_model_gamma else row.gamma
    sign = 1 if row.option_type == "CALL" else -1
    return sign * gamma * row.oi * 100 * spot * spot * 0.01


def moving_average(values: list[float], n: int) -> float | None:
    if len(values) < n:
        return None
    return sum(values[-n:]) / n


def ema(values: Iterable[float], period: int) -> list[float]:
    values = list(values)
    if not values:
        return []
    alpha = 2 / (period + 1)
    out = [values[0]]
    for value in values[1:]:
        out.append(alpha * value + (1 - alpha) * out[-1])
    return out


def compute_kdj(highs: list[float], lows: list[float], closes: list[float], period: int = 9):
    k = 50.0
    d = 50.0
    out = []
    for idx, close in enumerate(closes):
        start = max(0, idx - period + 1)
        low_n = min(lows[start : idx + 1])
        high_n = max(highs[start : idx + 1])
        rsv = 50.0 if high_n == low_n else (close - low_n) / (high_n - low_n) * 100
        k = (2 / 3) * k + (1 / 3) * rsv
        d = (2 / 3) * d + (1 / 3) * k
        j = 3 * k - 2 * d
        out.append((k, d, j))
    return out


def money(v: float) -> str:
    av = abs(v)
    if av >= 1_000_000_000:
        return f"{v/1_000_000_000:.2f}B"
    if av >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    if av >= 1_000:
        return f"{v/1_000:.1f}K"
    return f"{v:.0f}"


def pct(v: float) -> str:
    return f"{v:.2f}%"


def price_level(value) -> str:
    if value is None:
        return "无"
    return f"{float(value):g}"


def add_months(d: date, months: int) -> date:
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)


def parse_quote_date(value) -> date:
    try:
        text = str(value).split(".")[0]
        return datetime.strptime(text, "%Y-%m-%d %H:%M:%S").date()
    except Exception:
        return datetime.now().date()


def is_monthly_expiry(d: date) -> bool:
    # Monthly US expiries are usually the third Friday, but can move to
    # Thursday when Friday is a holiday. Day 15-21 catches both cases.
    return 15 <= d.day <= 21


def is_high_frequency_options_name(underlying: str) -> bool:
    ticker = underlying.split(".")[-1].upper()
    return ticker in {
        "SPY",
        "QQQ",
        "IWM",
        "DIA",
        "TSLA",
        "NVDA",
        "AMD",
        "AAPL",
        "MSFT",
        "AMZN",
        "META",
        "GOOGL",
        "GOOG",
        "PLTR",
    }


def select_option_expiries(underlying: str, expiry_values: list[str], ref_date: date) -> list[str]:
    parsed = []
    for value in expiry_values:
        try:
            parsed.append((datetime.strptime(str(value), "%Y-%m-%d").date(), str(value)))
        except Exception:
            continue
    parsed = sorted((d, s) for d, s in parsed if d >= ref_date)

    selected: set[str] = set()

    # Weeklies in the next two calendar weeks, when listed.
    for d, s in parsed:
        if d <= ref_date + timedelta(days=14):
            selected.add(s)

    # Monthly expiries for current month and next two months.
    monthly_months = {(add_months(ref_date, i).year, add_months(ref_date, i).month) for i in range(3)}
    for d, s in parsed:
        if (d.year, d.month) in monthly_months and is_monthly_expiry(d):
            selected.add(s)

    # Very active names can have daily expiries. Include the next two listed
    # near-term expiries as a proxy for the next two trading-day/daily options.
    if is_high_frequency_options_name(underlying):
        near_daily = [s for d, s in parsed if d <= ref_date + timedelta(days=7)]
        selected.update(near_daily[:2])

    return [s for d, s in parsed if s in selected]


def fetch_report_data(underlying: str):
    ctx = create_quote_context()
    try:
        ret, stock_df = ctx.get_market_snapshot([underlying])
        check_ret(ret, stock_df, ctx, "underlying snapshot")
        stock = stock_df.iloc[0]
        last_price = norm_float(stock["last_price"])
        pre_price = norm_float(stock.get("pre_price"))
        pre_bid = norm_float(stock.get("bid_price"))
        pre_ask = norm_float(stock.get("ask_price"))
        analysis_spot = pre_price or ((pre_bid + pre_ask) / 2 if pre_bid and pre_ask else last_price)
        spot_basis = "盘前价" if pre_price else ("盘前 bid/ask 中值" if pre_bid and pre_ask else "常规盘最近价")

        ret, exp_df = ctx.get_option_expiration_date(underlying)
        check_ret(ret, exp_df, ctx, "option expirations")
        all_expiries = [str(x) for x in exp_df["strike_time"].tolist()]
        quote_date = parse_quote_date(stock.get("update_time", ""))
        expiries = select_option_expiries(underlying, all_expiries, quote_date)
        if not expiries:
            expiries = all_expiries[:6]

        option_codes = []
        for expiry in expiries:
            ret, chain_df = ctx.get_option_chain(underlying, start=expiry, end=expiry)
            check_ret(ret, chain_df, ctx, f"option chain {expiry}")
            option_codes.extend(str(code) for code in chain_df["code"].tolist())

        rows: list[OptionRow] = []
        for start in range(0, len(option_codes), 350):
            ret, snap_df = ctx.get_market_snapshot(option_codes[start : start + 350])
            check_ret(ret, snap_df, ctx, "option snapshot")
            for _, r in snap_df.iterrows():
                if not bool(r.get("option_valid")):
                    continue
                row = OptionRow(
                    code=str(r["code"]),
                    expiry=str(r["strike_time"]),
                    option_type=str(r["option_type"]).upper(),
                    strike=norm_float(r.get("option_strike_price")),
                    oi=norm_int(r.get("option_open_interest")),
                    volume=norm_int(r.get("volume")),
                    bid=norm_float(r.get("bid_price")),
                    ask=norm_float(r.get("ask_price")),
                    last=norm_float(r.get("last_price")),
                    iv=norm_float(r.get("option_implied_volatility")) / 100.0,
                    delta=norm_float(r.get("option_delta")),
                    gamma=norm_float(r.get("option_gamma")),
                    theta=norm_float(r.get("option_theta")),
                    vega=norm_float(r.get("option_vega")),
                    dte=norm_float(r.get("option_expiry_date_distance")),
                )
                if row.oi > 0 and row.strike > 0 and row.iv > 0 and row.gamma > 0:
                    rows.append(row)

        ret, k_df, _ = ctx.request_history_kline(
            underlying,
            start="2026-02-01",
            end=None,
            ktype=KLType.K_DAY,
            autype=AuType.QFQ,
            max_count=200,
            session=Session.NONE,
        )
        check_ret(ret, k_df, ctx, "daily kline")

        closes = [norm_float(x) for x in k_df["close"].tolist()]
        highs = [norm_float(x) for x in k_df["high"].tolist()]
        lows = [norm_float(x) for x in k_df["low"].tolist()]
        volumes = [norm_int(x) for x in k_df["volume"].tolist()]
        dates = [str(x) for x in k_df["time_key"].tolist()]
        kdj = compute_kdj(highs, lows, closes)
        macd_fast = ema(closes, 6)
        macd_slow = ema(closes, 13)
        dif = [a - b for a, b in zip(macd_fast, macd_slow)]
        dea = ema(dif, 5)

        return {
            "stock": {
                "code": underlying,
                "name": str(stock.get("name", "BA")),
                "spot": analysis_spot,
                "spot_basis": spot_basis,
                "last_price": last_price,
                "pre_price": pre_price,
                "pre_high": norm_float(stock.get("pre_high_price")),
                "pre_low": norm_float(stock.get("pre_low_price")),
                "pre_volume": norm_int(stock.get("pre_volume")),
                "pre_change_rate": norm_float(stock.get("pre_change_rate")),
                "prev_close": norm_float(stock.get("prev_close_price")),
                "bid": pre_bid,
                "ask": pre_ask,
                "volume": norm_int(stock.get("volume")),
                "turnover": norm_float(stock.get("turnover")),
                "update_time": str(stock.get("update_time", "")),
            },
            "expiries": expiries,
            "options": rows,
            "daily": {
                "dates": dates,
                "close": closes,
                "high": highs,
                "low": lows,
                "volume": volumes,
                "ma5": moving_average(closes, 5),
                "ma10": moving_average(closes, 10),
                "ma20": moving_average(closes, 20),
                "ma50": moving_average(closes, 50),
                "kdj": kdj[-1],
                "dif": dif[-1],
                "dea": dea[-1],
            },
        }
    finally:
        safe_close(ctx)


def analyze(data):
    spot = data["stock"]["spot"]
    rows: list[OptionRow] = data["options"]
    net_current = sum(signed_gex(row, spot) for row in rows)
    by_strike: dict[float, float] = {}
    call_oi_by_strike: dict[float, int] = {}
    put_oi_by_strike: dict[float, int] = {}
    for row in rows:
        by_strike[row.strike] = by_strike.get(row.strike, 0.0) + signed_gex(row, spot)
        if row.option_type == "CALL":
            call_oi_by_strike[row.strike] = call_oi_by_strike.get(row.strike, 0) + row.oi
        else:
            put_oi_by_strike[row.strike] = put_oi_by_strike.get(row.strike, 0) + row.oi

    min_grid = math.floor((spot * 0.82) / 2.5) * 2.5
    max_grid = math.ceil((spot * 1.18) / 2.5) * 2.5
    grid = []
    s = min_grid
    while s <= max_grid + 1e-9:
        net = sum(signed_gex(row, s, use_model_gamma=True) for row in rows)
        grid.append({"spot": round(s, 2), "gex": net})
        s += 2.5

    flips = []
    for a, b in zip(grid, grid[1:]):
        if a["gex"] == 0 or a["gex"] * b["gex"] < 0:
            # Linear interpolation is enough for a rough flip zone.
            span = b["spot"] - a["spot"]
            denom = abs(a["gex"]) + abs(b["gex"])
            flip = a["spot"] + span * (abs(a["gex"]) / denom) if denom else a["spot"]
            flips.append(flip)

    max_abs = max(abs(x["gex"]) for x in grid) or 1
    walls = sorted(by_strike.items(), key=lambda kv: kv[1], reverse=True)[:10]
    pits = sorted(by_strike.items(), key=lambda kv: kv[1])[:10]
    nearest_wall_above = next((w for w in sorted(walls) if w[0] >= spot), None)
    nearest_support_wall = next((w for w in sorted(walls, reverse=True) if w[0] <= spot), None)
    flip = flips[0] if flips else None
    daily = data["daily"]
    last_close = daily["close"][-1]
    ma20 = daily["ma20"]
    ma50 = daily["ma50"]
    k, d, j = daily["kdj"]
    dif = daily["dif"]
    dea = daily["dea"]
    ret_20d = (last_close / daily["close"][-21] - 1) * 100 if len(daily["close"]) >= 21 else 0
    avg_vol20 = statistics.mean(daily["volume"][-20:])

    regime = "正 gamma" if net_current > 0 else "负 gamma"
    stance = "偏震荡上行、上方阻力密集" if net_current > 0 and nearest_wall_above else "偏趋势放大，风控优先"
    if flip and spot < flip:
        stance = "跌入负 gamma 区，趋势放大风险更高"

    return {
        "net_current": net_current,
        "grid": grid,
        "max_abs_grid": max_abs,
        "walls": walls,
        "pits": pits,
        "nearest_wall_above": nearest_wall_above,
        "nearest_support_wall": nearest_support_wall,
        "flip": flip,
        "call_oi_by_strike": call_oi_by_strike,
        "put_oi_by_strike": put_oi_by_strike,
        "regime": regime,
        "stance": stance,
        "ret_20d": ret_20d,
        "avg_vol20": avg_vol20,
        "j": j,
        "dif": dif,
        "dea": dea,
        "ma20": ma20,
        "ma50": ma50,
    }


def sparkline_path(points, width=620, height=230, pad=22):
    xs = [p["spot"] for p in points]
    ys = [p["gex"] for p in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    if ymin == ymax:
        ymin -= 1
        ymax += 1
    out = []
    for i, p in enumerate(points):
        x = pad + (p["spot"] - xmin) / (xmax - xmin) * (width - pad * 2)
        y = height - pad - (p["gex"] - ymin) / (ymax - ymin) * (height - pad * 2)
        out.append(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}")
    return " ".join(out)


def bar_svg(walls, pits, spot):
    items = sorted({k for k, _ in walls[:8] + pits[:8]})
    values = {k: 0.0 for k in items}
    for k, v in walls + pits:
        if k in values:
            values[k] = v
    maxv = max(abs(v) for v in values.values()) or 1
    bars = []
    for i, strike in enumerate(items):
        x = 50 + i * 44
        h = abs(values[strike]) / maxv * 126
        y = 150 - h if values[strike] >= 0 else 150
        fill = "#2563eb" if values[strike] >= 0 else "#dc2626"
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="28" height="{h:.1f}" rx="3" fill="{fill}"></rect>')
        bars.append(f'<text x="{x+14}" y="184" text-anchor="middle" class="axis">{strike:g}</text>')
    spot_x = 50 + (min(range(len(items)), key=lambda i: abs(items[i] - spot))) * 44 + 14 if items else 50
    return "\n".join(bars) + f'<line x1="{spot_x}" x2="{spot_x}" y1="20" y2="174" stroke="#111827" stroke-dasharray="4 4"></line>'


def option_table(rows: list[OptionRow], spot: float):
    near = sorted(rows, key=lambda r: (abs(r.strike - spot), r.expiry, r.option_type))[:28]
    body = []
    for r in near:
        mid = (r.bid + r.ask) / 2 if r.bid and r.ask else r.last
        body.append(
            "<tr>"
            f"<td>{html.escape(r.expiry)}</td><td>{html.escape(r.option_type)}</td><td>{r.strike:g}</td>"
            f"<td>{r.oi:,}</td><td>{r.volume:,}</td><td>{r.iv*100:.1f}%</td>"
            f"<td>{r.delta:.2f}</td><td>{r.gamma:.4f}</td><td>{mid:.2f}</td>"
            "</tr>"
        )
    return "\n".join(body)


def render_html(data, a):
    stock = data["stock"]
    ticker = stock["code"].split(".")[-1]
    spot = stock["spot"]
    path = sparkline_path(a["grid"])
    flip = a["flip"]
    flip_text = f"{flip:.2f}" if flip else "未检出"
    wall_above = a["nearest_wall_above"][0] if a["nearest_wall_above"] else None
    support_wall = a["nearest_support_wall"][0] if a["nearest_support_wall"] else None
    wall_text = price_level(wall_above)
    support_text = price_level(support_wall)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    next_wall = next((k for k, _ in a["walls"] if k > (wall_above or spot) + 0.01), None)
    next_wall_text = price_level(next_wall)

    if a["net_current"] > 0:
        simple_now = f"{ticker} 盘前在 {spot:.2f}，已经顶到第一道期权阻力 {wall_text} 附近。这里更像会磨一磨的位置，不像刚启动的顺风区。"
        simple_action = (
            f"我不会在这里直接追。开盘后如果能放量站稳 {wall_text}，再看下一道 {next_wall_text}；"
            f"如果冲不上去，先按 {support_text}-{wall_text} 之间震荡处理。"
        )
        simple_wrong = f"如果跌破 {support_text} 还收不回，短线多头热度降温；如果跌破 {flip_text}，就不是普通回调，而是下跌更容易被放大的区域。"
        core_take = simple_now
    else:
        simple_now = f"{ticker} 盘前在 {spot:.2f}，但期权结构偏负 gamma，价格更容易顺着一个方向放大。"
        simple_action = f"这种结构下我更看重开盘前 30 分钟方向，不急着逆势抄底或摸顶。重新站回 {flip_text} 上方，才把它当震荡盘看。"
        simple_wrong = f"如果价格站回 {flip_text} 且成交不放大，负 gamma 的风险会下降。"
        core_take = simple_now

    strategy_take = (
        "Gamma 只告诉我哪里容易卡住、哪里容易加速；真正进出场仍看策略2。"
        f"在 {wall_text} 附近，如果 KDJ 高位拐头、MACD 走弱或 FVG 被打回，我会把它看成冲高失败；"
        f"如果放量站稳 {wall_text}，再用 KDJ/MACD 确认是否能去 {next_wall_text}。"
    )

    risk_take = (
        "注意：盘前只有股票在动，期权 Greeks/OI 多数还是上一个交易时段的状态。"
        "所以这份报告适合做开盘前地图，不适合当自动交易信号。开盘后如果成交和期权量明显改变，需要重跑一次。"
    )

    grid_json = json.dumps(a["grid"])
    walls_json = json.dumps([{"strike": k, "gex": v} for k, v in a["walls"][:8]])
    pits_json = json.dumps([{"strike": k, "gex": v} for k, v in a["pits"][:8]])

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(ticker)} Gamma Exposure Report</title>
  <style>
    :root {{
      --bg: #f7f8f3;
      --ink: #16201b;
      --muted: #5f6d66;
      --line: #d9ded5;
      --panel: #ffffff;
      --blue: #2563eb;
      --red: #dc2626;
      --green: #0f766e;
      --amber: #b45309;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--bg);
      letter-spacing: 0;
    }}
    header {{
      padding: 28px 34px 20px;
      border-bottom: 1px solid var(--line);
      background: #fbfcf8;
    }}
    h1 {{ margin: 0; font-size: 30px; line-height: 1.1; font-weight: 760; }}
    .sub {{ margin-top: 8px; color: var(--muted); font-size: 14px; }}
    main {{
      display: grid;
      grid-template-columns: minmax(330px, 0.88fr) minmax(560px, 1.5fr);
      gap: 22px;
      padding: 22px 34px 34px;
      max-width: 1440px;
      margin: 0 auto;
    }}
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      min-width: 0;
      overflow-x: auto;
    }}
    h2 {{ margin: 0 0 12px; font-size: 17px; }}
    h3 {{ margin: 18px 0 8px; font-size: 14px; color: var(--muted); text-transform: uppercase; }}
    p {{ margin: 0 0 12px; line-height: 1.64; font-size: 14px; }}
    .metric-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }}
    .metric {{ border-top: 1px solid var(--line); padding-top: 10px; min-height: 66px; }}
    .metric b {{ display: block; font-size: 24px; line-height: 1.1; }}
    .metric span {{ color: var(--muted); font-size: 12px; }}
    .pill-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 2px; }}
    .pill {{ border: 1px solid var(--line); border-radius: 999px; padding: 6px 10px; font-size: 12px; background: #fafbf7; }}
    .blue {{ color: var(--blue); }} .red {{ color: var(--red); }} .green {{ color: var(--green); }} .amber {{ color: var(--amber); }}
    .chart {{ width: 100%; height: auto; display: block; }}
    .axis {{ fill: #66756e; font-size: 11px; }}
    .small {{ color: var(--muted); font-size: 12px; line-height: 1.5; }}
    table {{ width: 100%; min-width: 680px; border-collapse: collapse; font-size: 12px; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 8px 6px; text-align: right; }}
    th:first-child, td:first-child, th:nth-child(2), td:nth-child(2) {{ text-align: left; }}
    th {{ color: var(--muted); font-weight: 650; }}
    .two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .callout {{ background: #f4f7fb; border-left: 4px solid var(--blue); padding: 12px; border-radius: 6px; }}
    .danger {{ background: #fff7f5; border-left-color: var(--red); }}
    @media (max-width: 980px) {{
      main {{ grid-template-columns: 1fr; padding: 16px; }}
      header {{ padding: 22px 16px; }}
      .two {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(ticker)} Gamma Exposure Report</h1>
    <div class="sub">数据源：moomoo OpenD · 标的 {html.escape(stock["code"])} · 股票更新时间 {html.escape(stock["update_time"])} · 报告生成 {generated}</div>
  </header>
  <main>
    <section>
      <h2>一句话</h2>
      <p class="callout">{html.escape(core_take)}</p>
      <h3>我会怎么做</h3>
      <p>{html.escape(simple_action)}</p>
      <h3>什么情况说明我错了</h3>
      <p class="callout danger">{html.escape(simple_wrong)}</p>
      <h3>怎么和策略2配合</h3>
      <p>{html.escape(strategy_take)}</p>

      <h3>关键读数</h3>
      <div class="metric-grid">
        <div class="metric"><b>{spot:.2f}</b><span>{html.escape(stock["spot_basis"])}基准价</span></div>
        <div class="metric"><b>{stock["bid"]:.2f}/{stock["ask"]:.2f}</b><span>盘前 bid/ask</span></div>
        <div class="metric"><b class="{'blue' if a["net_current"] > 0 else 'red'}">{money(a["net_current"])}</b><span>当前净 GEX</span></div>
        <div class="metric"><b>{flip_text}</b><span>估算 gamma flip</span></div>
        <div class="metric"><b>{wall_text}</b><span>上方最近 gamma wall</span></div>
        <div class="metric"><b>{support_text}</b><span>下方正 gamma 支撑墙</span></div>
        <div class="metric"><b>{pct(a["ret_20d"])}</b><span>约 20 日涨跌幅</span></div>
        <div class="metric"><b>{a["j"]:.1f}</b><span>日线 KDJ J 值</span></div>
      </div>

      <h3>策略2怎么用</h3>
      <div class="pill-row">
        <span class="pill">240-250：先看阻力/钉扎</span>
        <span class="pill">站稳 250：再看 255/260</span>
        <span class="pill">跌破 {flip_text}：负 gamma 风险</span>
        <span class="pill">J 高位转弱：追多降权</span>
      </div>
      <p class="small">术语翻译：gamma wall = 容易卡住的价格；gamma flip = 市场性格切换线；正 gamma = 更容易震荡和钉住，负 gamma = 更容易加速。</p>
      <p class="small">日线 MA20：{a["ma20"]:.2f}，MA50：{a["ma50"]:.2f}；快速 MACD DIF/DEA：{a["dif"]:.2f}/{a["dea"]:.2f}。这些不是替代 gamma，而是用来确认 wall 处的突破、失败或反转。</p>
      <p class="small">常规盘最后价：{stock["last_price"]:.2f}；盘前价：{stock["pre_price"]:.2f}，盘前涨幅：{stock["pre_change_rate"]:.2f}%，盘前区间：{stock["pre_low"]:.2f}-{stock["pre_high"]:.2f}，盘前成交量：{stock["pre_volume"]:,}。</p>
      <p class="small">{html.escape(risk_take)}</p>
    </section>

    <section>
      <h2>Gamma Surface</h2>
      <svg class="chart" viewBox="0 0 680 280" role="img" aria-label="{html.escape(ticker)} gamma exposure curve">
        <rect x="0" y="0" width="680" height="280" fill="#fff"></rect>
        <line x1="38" x2="642" y1="140" y2="140" stroke="#d9ded5"></line>
        <path d="{path}" fill="none" stroke="#2563eb" stroke-width="3"></path>
        <line x1="38" x2="642" y1="34" y2="34" stroke="#eef1eb"></line>
        <line x1="38" x2="642" y1="246" y2="246" stroke="#eef1eb"></line>
        <text x="38" y="267" class="axis">{a["grid"][0]["spot"]:g}</text>
        <text x="322" y="267" class="axis">spot price grid</text>
        <text x="622" y="267" class="axis">{a["grid"][-1]["spot"]:g}</text>
        <text x="42" y="26" class="axis">positive gamma: volatility dampening</text>
        <text x="42" y="160" class="axis">zero / flip</text>
      </svg>
      <p class="small">曲线使用期权链的 IV、DTE、OI 在假设价格网格上重算 Black-Scholes gamma，再按 Call 正、Put 负汇总。曲线越高，越接近“做市商逆势对冲导致价格变慢”的区域。</p>

      <div class="two">
        <div>
          <h3>Strike Gamma Wall</h3>
          <svg class="chart" viewBox="0 0 440 205">
            <line x1="34" x2="410" y1="150" y2="150" stroke="#d9ded5"></line>
            {bar_svg(a["walls"], a["pits"], spot)}
          </svg>
        </div>
        <div>
          <h3>我会盯的价格</h3>
          <p><b class="green">支撑/阻力墙：</b>{", ".join(f"{k:g}" for k, _ in a["walls"][:6])}</p>
          <p><b class="red">负 gamma 洼地：</b>{", ".join(f"{k:g}" for k, _ in a["pits"][:6])}</p>
          <p><b>Flip：</b>{flip_text}。在它上方，倾向用“震荡、钉扎、突破确认”；在它下方，倾向用“趋势放大、快进快出”。</p>
        </div>
      </div>

      <h3>ATM 附近期权样本</h3>
      <table>
        <thead><tr><th>到期</th><th>类型</th><th>Strike</th><th>OI</th><th>Vol</th><th>IV</th><th>Delta</th><th>Gamma</th><th>Mid</th></tr></thead>
        <tbody>{option_table(data["options"], spot)}</tbody>
      </table>
    </section>
  </main>
  <script>
    window.gammaReportData = {{
      grid: {grid_json},
      walls: {walls_json},
      pits: {pits_json}
    }};
  </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Generate a moomoo OpenD gamma exposure HTML report")
    parser.add_argument("code", nargs="?", default=DEFAULT_UNDERLYING, help="Stock code, e.g. US.BA or US.MP")
    parser.add_argument("--output", default=None, help="Output HTML path")
    args = parser.parse_args()

    code = args.code.upper()
    ticker = code.split(".")[-1].lower()
    report_path = Path(args.output) if args.output else REPORT_DIR / f"{ticker}_gamma_report.html"

    data = fetch_report_data(code)
    analysis = analyze(data)
    report_path.write_text(render_html(data, analysis), encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
