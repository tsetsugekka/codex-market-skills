#!/usr/bin/env python3
"""
Print a gamma/vanna exposure memo from moomoo OpenD.

The memo is intentionally opinionated: option structure is evidence, while
the summary turns gamma structure into trading scenarios that can be combined
with technical confirmation.
"""

from __future__ import annotations

import argparse
import math
import statistics
import time
from dataclasses import dataclass
from datetime import date, datetime, time as dt_time, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Iterable

import sys

sys.path.insert(0, str(Path.home() / ".codex/skills/moomooapi/scripts"))
from common import AuType, KLType, RET_OK, Session, check_ret, create_quote_context, safe_close  # noqa: E402


DEFAULT_UNDERLYING = "US.BA"
OPTION_CHAIN_DELAY_SECONDS = 3.2
OPTION_CHAIN_RETRY_DELAY_SECONDS = 31.0


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


def black_scholes_vanna(spot: float, strike: float, iv: float, dte: float) -> float:
    """Delta change per 1.00 vol unit; multiply by 0.01 for one IV point."""
    if spot <= 0 or strike <= 0 or iv <= 0:
        return 0.0
    t = max(dte, 0.25) / 365.0
    sqrt_t = math.sqrt(t)
    d1 = (math.log(spot / strike) + 0.5 * iv * iv * t) / (iv * sqrt_t)
    d2 = d1 - iv * sqrt_t
    return -normal_pdf(d1) * d2 / iv


def black_scholes_charm(spot: float, strike: float, iv: float, dte: float) -> float:
    """Approximate delta change from time decay per year, zero-rate version."""
    if spot <= 0 or strike <= 0 or iv <= 0:
        return 0.0
    t = max(dte, 0.25) / 365.0
    sqrt_t = math.sqrt(t)
    d1 = (math.log(spot / strike) + 0.5 * iv * iv * t) / (iv * sqrt_t)
    d2 = d1 - iv * sqrt_t
    return normal_pdf(d1) * d2 / (2 * t)


def signed_gex(row: OptionRow, spot: float, use_model_gamma: bool = False) -> float:
    gamma = black_scholes_gamma(spot, row.strike, row.iv, row.dte) if use_model_gamma else row.gamma
    sign = 1 if row.option_type == "CALL" else -1
    return sign * gamma * row.oi * 100 * spot * spot * 0.01


def signed_vex(row: OptionRow, spot: float) -> float:
    sign = 1 if row.option_type == "CALL" else -1
    # Spot-equivalent delta-dollar change for a one-vol-point IV move.
    return sign * black_scholes_vanna(spot, row.strike, row.iv, row.dte) * 0.01 * row.oi * 100 * spot


def signed_dex(row: OptionRow, spot: float) -> float:
    # Option delta-dollar exposure using the option's native delta sign.
    return row.delta * row.oi * 100 * spot


def signed_charm_exposure(row: OptionRow, spot: float) -> float:
    sign = 1 if row.option_type == "CALL" else -1
    # Spot-equivalent delta-dollar change from one calendar day of time decay.
    return sign * black_scholes_charm(spot, row.strike, row.iv, row.dte) / 365.0 * row.oi * 100 * spot


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


def pct_distance(spot: float, level) -> str:
    if level is None or spot <= 0:
        return "无"
    return f"{(float(level) / spot - 1) * 100:+.2f}%"


def price_level(value) -> str:
    if value is None:
        return "无"
    return f"{float(value):g}"


def fmt_num(value, digits: int = 2) -> str:
    if value is None:
        return "无"
    return f"{float(value):.{digits}f}"


def level_list(items, limit: int = 6) -> str:
    if not items:
        return "无"
    return ", ".join(f"{k:g}({money(v)})" for k, v in items[:limit])


def oi_level_list(items, limit: int = 6) -> str:
    if not items:
        return "无"
    return ", ".join(f"{k:g}({v:,})" for k, v in items[:limit])


def iv_text(iv_value) -> str:
    if iv_value is None:
        return "无"
    return f"{iv_value * 100:.1f}%"


def render_iv_smile(smile: dict) -> str:
    if not smile:
        return "无"
    skew = "无" if smile.get("skew") is None else f"{smile['skew'] * 100:+.1f} vol pts"
    return (
        f"{smile.get('expiry')} front expiry; ATM {iv_text(smile.get('atm'))}; "
        f"put wing {iv_text(smile.get('put_wing'))}; call wing {iv_text(smile.get('call_wing'))}; "
        f"skew {skew}; {smile.get('label', '无')}"
    )


def signed_call_gex(row: OptionRow, spot: float, use_model_gamma: bool = False) -> float:
    if row.option_type != "CALL":
        return 0.0
    gamma = black_scholes_gamma(spot, row.strike, row.iv, row.dte) if use_model_gamma else row.gamma
    return gamma * row.oi * 100 * spot * spot * 0.01


def signed_put_abs_gex(row: OptionRow, spot: float, use_model_gamma: bool = False) -> float:
    if row.option_type != "PUT":
        return 0.0
    gamma = black_scholes_gamma(spot, row.strike, row.iv, row.dte) if use_model_gamma else row.gamma
    return gamma * row.oi * 100 * spot * spot * 0.01


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


def choose_stock_anchor(stock) -> tuple[float, str]:
    last_price = norm_float(stock.get("last_price"))
    bid = norm_float(stock.get("bid_price"))
    ask = norm_float(stock.get("ask_price"))
    pre_price = norm_float(stock.get("pre_price"))
    after_price = norm_float(stock.get("after_price"))
    overnight_price = norm_float(stock.get("overnight_price"))

    now_et = datetime.now(ZoneInfo("America/New_York"))
    t = now_et.time()
    weekday = now_et.weekday()

    def midpoint():
        return (bid + ask) / 2 if bid > 0 and ask > 0 else 0.0

    candidates: list[tuple[float, str]] = []
    # Moomoo keeps old pre_price values after the pre-market ends. Choose by
    # active U.S. session first so stale pre-market prints do not become the
    # Gamma/Vanna pricing anchor during after-hours or overnight trading.
    if weekday < 5 and dt_time(9, 30) <= t < dt_time(16, 0):
        candidates = [(last_price, "常规盘最近成交参考价"), (midpoint(), "bid/ask 中值参考价")]
    elif weekday < 5 and dt_time(16, 0) <= t < dt_time(20, 0):
        candidates = [(after_price, "盘后参考价"), (midpoint(), "bid/ask 中值参考价"), (last_price, "常规盘最近成交参考价")]
    elif (weekday == 6 and t >= dt_time(20, 0)) or weekday < 5 and (t < dt_time(4, 0) or t >= dt_time(20, 0)):
        candidates = [(overnight_price, "隔夜盘参考价"), (midpoint(), "bid/ask 中值参考价"), (after_price, "盘后参考价"), (last_price, "常规盘最近成交参考价")]
    elif weekday < 5 and dt_time(4, 0) <= t < dt_time(9, 30):
        candidates = [(pre_price, "盘前参考价"), (overnight_price, "隔夜盘参考价"), (midpoint(), "bid/ask 中值参考价"), (last_price, "常规盘最近成交参考价")]
    else:
        candidates = [(last_price, "常规盘最近成交参考价"), (overnight_price, "隔夜盘参考价"), (after_price, "盘后参考价"), (midpoint(), "bid/ask 中值参考价")]

    for price, basis in candidates:
        if price > 0:
            return price, basis
    return 0.0, "无可用行情锚点"


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
        near_daily = []
        for d, s in parsed:
            if d <= ref_date + timedelta(days=7) and s not in near_daily:
                near_daily.append(s)
        selected.update(near_daily[:2])

    out = []
    seen = set()
    for _, s in parsed:
        if s in selected and s not in seen:
            out.append(s)
            seen.add(s)
    return out


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
        analysis_spot, spot_basis = choose_stock_anchor(stock)

        ret, exp_df = ctx.get_option_expiration_date(underlying)
        check_ret(ret, exp_df, ctx, "option expirations")
        all_expiries = [str(x) for x in exp_df["strike_time"].tolist()]
        quote_date = parse_quote_date(stock.get("update_time", ""))
        expiries = select_option_expiries(underlying, all_expiries, quote_date)
        if not expiries:
            expiries = all_expiries[:6]

        option_codes = []
        for idx, expiry in enumerate(expiries):
            if idx:
                time.sleep(OPTION_CHAIN_DELAY_SECONDS)
            ret, chain_df = ctx.get_option_chain(underlying, start=expiry, end=expiry)
            if ret != RET_OK and "频率" in str(chain_df):
                time.sleep(OPTION_CHAIN_RETRY_DELAY_SECONDS)
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
                if row.oi > 0 and row.strike > 0 and row.iv > 0 and row.gamma > 0 and row.dte >= 0:
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
                "after_price": norm_float(stock.get("after_price")),
                "overnight_price": norm_float(stock.get("overnight_price")),
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
    vanna_by_strike: dict[float, float] = {}
    dex_by_strike: dict[float, float] = {}
    charm_by_strike: dict[float, float] = {}
    call_oi_by_strike: dict[float, int] = {}
    put_oi_by_strike: dict[float, int] = {}
    for row in rows:
        by_strike[row.strike] = by_strike.get(row.strike, 0.0) + signed_gex(row, spot)
        vanna_by_strike[row.strike] = vanna_by_strike.get(row.strike, 0.0) + signed_vex(row, spot)
        dex_by_strike[row.strike] = dex_by_strike.get(row.strike, 0.0) + signed_dex(row, spot)
        charm_by_strike[row.strike] = charm_by_strike.get(row.strike, 0.0) + signed_charm_exposure(row, spot)
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
    vanna_walls = sorted(vanna_by_strike.items(), key=lambda kv: kv[1], reverse=True)[:10]
    vanna_pits = sorted(vanna_by_strike.items(), key=lambda kv: kv[1])[:10]
    dex_walls = sorted(dex_by_strike.items(), key=lambda kv: kv[1], reverse=True)[:10]
    dex_pits = sorted(dex_by_strike.items(), key=lambda kv: kv[1])[:10]
    charm_walls = sorted(charm_by_strike.items(), key=lambda kv: kv[1], reverse=True)[:10]
    charm_pits = sorted(charm_by_strike.items(), key=lambda kv: kv[1])[:10]
    call_oi_shelves = sorted(call_oi_by_strike.items(), key=lambda kv: kv[1], reverse=True)[:10]
    put_oi_shelves = sorted(put_oi_by_strike.items(), key=lambda kv: kv[1], reverse=True)[:10]
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
        "net_vanna": sum(signed_vex(row, spot) for row in rows),
        "net_dex": sum(signed_dex(row, spot) for row in rows),
        "net_charm": sum(signed_charm_exposure(row, spot) for row in rows),
        "grid": grid,
        "max_abs_grid": max_abs,
        "walls": walls,
        "pits": pits,
        "vanna_walls": vanna_walls,
        "vanna_pits": vanna_pits,
        "dex_walls": dex_walls,
        "dex_pits": dex_pits,
        "charm_walls": charm_walls,
        "charm_pits": charm_pits,
        "call_oi_shelves": call_oi_shelves,
        "put_oi_shelves": put_oi_shelves,
        "iv_smile": summarize_iv_smile(rows, spot),
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


def find_gamma_flip(rows: list[OptionRow], spot: float) -> float | None:
    if not rows or spot <= 0:
        return None
    min_grid = math.floor((spot * 0.82) / 2.5) * 2.5
    max_grid = math.ceil((spot * 1.18) / 2.5) * 2.5
    prev_spot = None
    prev_gex = None
    s = min_grid
    while s <= max_grid + 1e-9:
        net = sum(signed_gex(row, s, use_model_gamma=True) for row in rows)
        if prev_gex is not None and (net == 0 or prev_gex * net < 0):
            span = s - prev_spot
            denom = abs(prev_gex) + abs(net)
            return prev_spot + span * (abs(prev_gex) / denom) if denom else prev_spot
        prev_spot = s
        prev_gex = net
        s += 2.5
    return None


def top_level(levels: dict[float, float], positive_only: bool = False, abs_rank: bool = False):
    items = [(k, v) for k, v in levels.items() if (v > 0 or not positive_only)]
    if not items:
        return None, 0.0
    key = (lambda kv: abs(kv[1])) if abs_rank else (lambda kv: kv[1])
    strike, value = max(items, key=key)
    return strike, value


def weighted_avg(rows: list[OptionRow]) -> float | None:
    if not rows:
        return None
    total_weight = sum(max(row.oi, 1) for row in rows)
    if total_weight <= 0:
        return None
    return sum(row.iv * max(row.oi, 1) for row in rows) / total_weight


def summarize_iv_smile(rows: list[OptionRow], spot: float) -> dict:
    if not rows or spot <= 0:
        return {}
    front_expiry = sorted({row.expiry for row in rows})[0]
    front = [row for row in rows if row.expiry == front_expiry]
    atm_band = [row for row in front if abs(row.strike / spot - 1) <= 0.03]
    put_wing = [row for row in front if row.option_type == "PUT" and 0.85 <= row.strike / spot <= 0.97]
    call_wing = [row for row in front if row.option_type == "CALL" and 1.03 <= row.strike / spot <= 1.15]
    atm = weighted_avg(atm_band)
    put_iv = weighted_avg(put_wing)
    call_iv = weighted_avg(call_wing)
    skew = (put_iv - call_iv) if put_iv is not None and call_iv is not None else None
    if skew is None:
        label = "资料不足"
    elif skew > 0.08:
        label = "下行尾部溢价高"
    elif skew < -0.08:
        label = "上行追涨/挤压溢价高"
    else:
        label = "双侧较均衡"
    return {
        "expiry": front_expiry,
        "atm": atm,
        "put_wing": put_iv,
        "call_wing": call_iv,
        "skew": skew,
        "label": label,
    }


def analyze_by_expiry(data):
    spot = data["stock"]["spot"]
    rows: list[OptionRow] = data["options"]
    grouped: dict[str, list[OptionRow]] = {}
    for row in rows:
        grouped.setdefault(row.expiry, []).append(row)

    out = []
    for expiry in sorted(grouped):
        expiry_rows = grouped[expiry]
        net_gex = sum(signed_gex(row, spot) for row in expiry_rows)
        net_vex = sum(signed_vex(row, spot) for row in expiry_rows)
        net_dex = sum(signed_dex(row, spot) for row in expiry_rows)
        net_charm = sum(signed_charm_exposure(row, spot) for row in expiry_rows)
        by_strike: dict[float, float] = {}
        call_by_strike: dict[float, float] = {}
        put_by_strike: dict[float, float] = {}
        for row in expiry_rows:
            by_strike[row.strike] = by_strike.get(row.strike, 0.0) + signed_gex(row, spot)
            call_by_strike[row.strike] = call_by_strike.get(row.strike, 0.0) + signed_call_gex(row, spot)
            put_by_strike[row.strike] = put_by_strike.get(row.strike, 0.0) + signed_put_abs_gex(row, spot)

        gamma_wall, gamma_wall_value = top_level(by_strike, positive_only=True)
        if gamma_wall is None:
            gamma_wall, gamma_wall_value = top_level(by_strike, abs_rank=True)
        call_wall, call_wall_value = top_level(call_by_strike)
        put_wall, put_wall_value = top_level(put_by_strike)
        pits = sorted(by_strike.items(), key=lambda kv: kv[1])[:3]
        walls = sorted(by_strike.items(), key=lambda kv: kv[1], reverse=True)[:3]
        flip = find_gamma_flip(expiry_rows, spot)

        out.append(
            {
                "expiry": expiry,
                "dte": min((row.dte for row in expiry_rows), default=0),
                "net_gex": net_gex,
                "net_vex": net_vex,
                "net_dex": net_dex,
                "net_charm": net_charm,
                "vol_trigger": flip,
                "gamma_wall": gamma_wall,
                "gamma_wall_value": gamma_wall_value,
                "call_wall": call_wall,
                "call_wall_value": call_wall_value,
                "put_wall": put_wall,
                "put_wall_value": put_wall_value,
                "walls": walls,
                "pits": pits,
            }
        )
    return out


def directional_label(spot: float, item: dict) -> str:
    trigger = item["vol_trigger"]
    put_wall = item["put_wall"]
    call_wall = item["call_wall"]
    net_gex = item["net_gex"]
    if trigger and spot < trigger and net_gex < 0:
        return "偏空/高波动"
    if put_wall and call_wall and put_wall <= spot <= call_wall:
        if trigger and spot >= trigger:
            return "中性偏多修复"
        return "中性战场"
    if trigger and spot >= trigger and net_gex >= 0:
        return "偏多钉扎"
    if net_gex < 0:
        return "高波动战场"
    return "中性"


def render_by_expiry_text(data, analysis, per_expiry):
    stock = data["stock"]
    spot = stock["spot"]
    ticker = stock["code"].split(".")[-1]
    lines = [
        f"{ticker} by-expiry gamma directional memo",
        "",
        f"- 定价锚点价: {spot:.2f} ({stock['spot_basis']}; 更新时间 {stock['update_time']})",
        f"All selected expiries: net GEX {money(analysis['net_current'])}; gamma flip {fmt_num(analysis['flip']) if analysis['flip'] else '未检出'}; regime {analysis['regime']}",
        "",
        "| Expiration | DTE | Bias | Volatility Trigger | Gamma Wall | Call Wall | Put Wall | 距VT | 距CW | 距PW | Net GEX | Net VEX | Net DEX | Charm/day |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in per_expiry:
        lines.append(
            "| {expiry} | {dte:.0f} | {bias} | {trigger} | {gamma_wall} | {call_wall} | {put_wall} | {dist_trigger} | {dist_call} | {dist_put} | {net_gex} | {net_vex} | {net_dex} | {net_charm} |".format(
                expiry=item["expiry"],
                dte=item["dte"],
                bias=directional_label(spot, item),
                trigger=price_level(item["vol_trigger"]),
                gamma_wall=price_level(item["gamma_wall"]),
                call_wall=price_level(item["call_wall"]),
                put_wall=price_level(item["put_wall"]),
                dist_trigger=pct_distance(spot, item["vol_trigger"]),
                dist_call=pct_distance(spot, item["call_wall"]),
                dist_put=pct_distance(spot, item["put_wall"]),
                net_gex=money(item["net_gex"]),
                net_vex=money(item["net_vex"]),
                net_dex=money(item["net_dex"]),
                net_charm=money(item["net_charm"]),
            )
        )

    nearest_trigger_items = [x for x in per_expiry if x["vol_trigger"] is not None]
    nearest_trigger = min(nearest_trigger_items, key=lambda x: abs(x["vol_trigger"] - spot)) if nearest_trigger_items else None
    nearest_call = min((x for x in per_expiry if x["call_wall"] and x["call_wall"] >= spot), key=lambda x: x["call_wall"] - spot, default=None)
    nearest_put = min((x for x in per_expiry if x["put_wall"] and x["put_wall"] <= spot), key=lambda x: spot - x["put_wall"], default=None)

    upper = nearest_call["call_wall"] if nearest_call else analysis["nearest_wall_above"][0] if analysis["nearest_wall_above"] else None
    lower = nearest_put["put_wall"] if nearest_put else analysis["nearest_support_wall"][0] if analysis["nearest_support_wall"] else None
    trigger = nearest_trigger["vol_trigger"] if nearest_trigger else analysis["flip"]

    lines.extend(
        [
            "",
            "*Volatility Trigger 是本脚本用同一期权链重算的 gamma flip / volatility-regime 近似，不是任何第三方专有公式。",
            "",
            "结论：",
            f"- 当前最接近的 regime 分水岭在 {price_level(trigger)}；现价 {spot:.2f} {'在其上方，偏修复' if trigger and spot >= trigger else '在其下方，偏高波动/防守' if trigger else '缺少明确 trigger'}。",
            f"- 上方先看 {price_level(upper)}；站稳才看更高 call/gamma wall。下方先看 {price_level(lower)}；跌破会让负 gamma/pit 风险变重要。",
            "- 多空判断以现价是否站稳 trigger、是否突破 call wall、是否跌破 put wall 为准；不要只看单个远端 call 或 put 仓位。",
        ]
    )
    return "\n".join(lines)


def render_text(data, a):
    stock = data["stock"]
    ticker = stock["code"].split(".")[-1]
    spot = stock["spot"]
    flip_text = fmt_num(a["flip"]) if a["flip"] else "未检出"
    wall_above = a["nearest_wall_above"][0] if a["nearest_wall_above"] else None
    support_wall = a["nearest_support_wall"][0] if a["nearest_support_wall"] else None
    call_wall = a["call_oi_shelves"][0][0] if a["call_oi_shelves"] else wall_above
    put_wall = a["put_oi_shelves"][0][0] if a["put_oi_shelves"] else support_wall
    next_wall = next((k for k, _ in a["walls"] if k > (wall_above or spot) + 0.01), None)
    wall_text = price_level(wall_above)
    support_text = price_level(support_wall)
    next_wall_text = price_level(next_wall)
    lower_decision = put_wall if put_wall is not None and put_wall <= spot else support_wall
    lower_decision_text = price_level(lower_decision)
    trigger = a["flip"]
    close_to_call = call_wall is not None and abs(call_wall / spot - 1) <= 0.04
    close_to_put = put_wall is not None and abs(put_wall / spot - 1) <= 0.04
    iv_label = a["iv_smile"].get("label", "资料不足") if a["iv_smile"] else "资料不足"

    if trigger and spot < trigger:
        bias = "中性偏空/高波动"
        reason = f"现价低于 volatility trigger {flip_text}，gamma regime 尚未修复"
    elif a["net_current"] > 0 and close_to_call and close_to_put:
        bias = "中性钉扎"
        reason = "正 gamma 且现价夹在近端 call/put 仓位之间"
    elif a["net_current"] > 0:
        bias = "中性偏多修复"
        reason = "净 GEX 为正，价格更容易围绕墙位均值回归"
    else:
        bias = "高波动战场"
        reason = "净 GEX 为负，突破/跌破方向更容易被放大"

    if a["net_current"] > 0:
        one_line = (
            f"{ticker} 当前按 {stock['spot_basis']} {spot:.2f} 做锚，结论为 {bias}。"
            f"{reason}；上方第一 gamma wall 在 {wall_text}，下方第一防守看 {lower_decision_text}。"
        )
        action = (
            f"不把 gamma wall 当追涨信号。若放量站稳 {wall_text}，再看 {next_wall_text}；"
            f"若冲不上，先按 {lower_decision_text}-{wall_text} 的钉扎/震荡处理。"
        )
        wrong = f"跌破 {lower_decision_text} 且收不回，多头结构降权；跌破 flip {flip_text}，趋势放大风险上升。"
    else:
        one_line = (
            f"{ticker} 当前按 {stock['spot_basis']} {spot:.2f} 做锚，结论为 {bias}。"
            f"{reason}；价格更容易顺着突破或跌破方向放大。"
        )
        action = f"先看开盘前后方向确认，不急着逆势抄底或摸顶；重新站回 flip {flip_text} 上方，再按震荡盘处理。"
        wrong = f"若价格站回 {flip_text} 且成交不放大，负 gamma 风险下降。"

    return "\n".join(
        [
            f"{ticker} gamma/vanna memo",
            "",
            f"一句话：{one_line}",
            f"我会怎么做：{action}",
            f"什么情况说明我错了：{wrong}",
            "",
            "关键位：",
            f"- 定价锚点价: {spot:.2f} ({stock['spot_basis']}; 更新时间 {stock['update_time']})",
            f"- Volatility Trigger / Gamma Flip: {flip_text} (距VT {pct_distance(spot, a['flip'])})",
            f"- Gamma Wall: {wall_text} (距GW {pct_distance(spot, wall_above)}); Call Wall: {price_level(call_wall)} (距CW {pct_distance(spot, call_wall)}); Put Wall: {price_level(put_wall)} (距PW {pct_distance(spot, put_wall)})",
            f"- 净 GEX: {money(a['net_current'])}; 净 VEX: {money(a['net_vanna'])}; 净 DEX: {money(a['net_dex'])}; Charm/day: {money(a['net_charm'])}; regime: {a['regime']}",
            f"- Gamma walls: {level_list(a['walls'])}",
            f"- Negative gamma pits: {level_list(a['pits'])}",
            f"- Vanna positive zones: {level_list(a['vanna_walls'])}",
            f"- Vanna negative zones: {level_list(a['vanna_pits'])}",
            f"- DEX positive zones: {level_list(a['dex_walls'])}",
            f"- DEX negative zones: {level_list(a['dex_pits'])}",
            f"- Charm positive zones: {level_list(a['charm_walls'])}",
            f"- Charm negative zones: {level_list(a['charm_pits'])}",
            f"- Call OI shelves: {oi_level_list(a['call_oi_shelves'])}",
            f"- Put OI shelves: {oi_level_list(a['put_oi_shelves'])}",
            f"- Front IV smile/skew: {render_iv_smile(a['iv_smile'])}",
            "",
            "结论如何综合这些项目：",
            f"- VT/Gamma Flip 决定 regime；当前 {spot:.2f} 相对 {flip_text} 给出主方向框架。",
            f"- GW/CW/PW 决定最近交易战场；当前离 CW {pct_distance(spot, call_wall)}、离 PW {pct_distance(spot, put_wall)}。",
            f"- GEX 给出钉扎或放大；VEX 看 IV 变化后的压力区；DEX/Charm 用来判断近端对冲和时间流逝是否会强化墙位。",
            f"- IV smile 目前为 `{iv_label}`，若波动率继续抬升，要降低单纯按正 gamma 修复的信心；若 IV 回落，Vanna/Charm 区域更容易发挥吸引或钉扎作用。",
            "",
            "技术确认配合：",
            f"- 20日涨跌幅 {pct(a['ret_20d'])}; MA20 {fmt_num(a['ma20'])}; MA50 {fmt_num(a['ma50'])}",
            f"- KDJ J {a['j']:.1f}; 快速 MACD DIF/DEA {a['dif']:.2f}/{a['dea']:.2f}",
            "- Gamma 只给地图；突破、失败或反转仍要用成交、KDJ/MACD、FVG/均线结构确认。",
            "",
            "数据注意：这里的定价锚点价用于重算 Gamma/Vanna，不一定是正式交易时段的实时成交价；盘前/隔夜股票字段可能更新，但期权 IV/OI/Greeks 多数仍是上一期权交易时段状态。开盘后若现货或期权量明显变化，需要重跑。",
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="Print a moomoo OpenD gamma exposure text memo")
    parser.add_argument("code", nargs="?", default=DEFAULT_UNDERLYING, help="Stock code, e.g. US.BA or US.MP")
    parser.add_argument(
        "--by-expiry-report",
        action="store_true",
        help="Print a per-expiry trigger/wall table with directional labels",
    )
    args = parser.parse_args()

    code = args.code.upper()

    data = fetch_report_data(code)
    analysis = analyze(data)
    if args.by_expiry_report:
        print(render_by_expiry_text(data, analysis, analyze_by_expiry(data)))
    else:
        print(render_text(data, analysis))


if __name__ == "__main__":
    main()
