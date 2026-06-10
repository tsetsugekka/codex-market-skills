#!/usr/bin/env python3
"""SPX/SPXW intraday gamma map using the dedicated index-option workflow."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path.home() / ".codex/skills/moomooapi/scripts"))
from common import RET_OK, create_quote_context, safe_close  # noqa: E402


UNDERLYING = "US..SPX"
SPY = "US.SPY"
SCRIPT_DIR = Path(__file__).resolve().parent
OPTION_CHAIN_DELAY_SECONDS = 3.2
OPTION_CHAIN_RETRY_DELAY_SECONDS = 31.0


def f(value, default=0.0) -> float:
    try:
        if value is None:
            return default
        out = float(value)
        return default if math.isnan(out) else out
    except Exception:
        return default


def i(value, default=0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def mid(row) -> float:
    bid = f(row.get("bid_price"))
    ask = f(row.get("ask_price"))
    last = f(row.get("last_price"))
    return (bid + ask) / 2 if bid > 0 and ask > 0 else last


def normal_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def bs_gamma(spot: float, strike: float, iv: float, dte: float) -> float:
    if spot <= 0 or strike <= 0 or iv <= 0:
        return 0.0
    t = max(dte, 0.15) / 365.0
    d1 = (math.log(spot / strike) + 0.5 * iv * iv * t) / (iv * math.sqrt(t))
    return normal_pdf(d1) / (spot * iv * math.sqrt(t))


def bs_vanna(spot: float, strike: float, iv: float, dte: float) -> float:
    if spot <= 0 or strike <= 0 or iv <= 0:
        return 0.0
    t = max(dte, 0.15) / 365.0
    sqrt_t = math.sqrt(t)
    d1 = (math.log(spot / strike) + 0.5 * iv * iv * t) / (iv * sqrt_t)
    d2 = d1 - iv * sqrt_t
    return -normal_pdf(d1) * d2 / iv


def signed_gex(row: dict, spot: float, use_model: bool = False) -> float:
    gamma = bs_gamma(spot, row["strike"], row["iv"], row["dte"]) if use_model else row["gamma"]
    sign = 1 if row["type"] == "CALL" else -1
    return sign * gamma * row["oi"] * 100 * spot * spot * 0.01


def signed_vex(row: dict, spot: float) -> float:
    sign = 1 if row["type"] == "CALL" else -1
    return sign * bs_vanna(spot, row["strike"], row["iv"], row["dte"]) * 0.01 * row["oi"] * 100 * spot


def top_items(mapping: dict[float, float], n: int = 12, reverse: bool = True) -> list[list[float]]:
    return [[float(k), float(v)] for k, v in sorted(mapping.items(), key=lambda kv: kv[1], reverse=reverse)[:n]]


def weighted_anchor_from_parity(rows: list[dict]) -> tuple[float, list[tuple]]:
    pairs: dict[float, dict[str, dict]] = defaultdict(dict)
    for row in rows:
        if row["bucket"] == "0DTE" and row["mid"] > 0:
            pairs[row["strike"]][row["type"]] = row

    estimates = []
    for strike, pair in pairs.items():
        call = pair.get("CALL")
        put = pair.get("PUT")
        if not call or not put:
            continue
        if call["mid"] <= 0 or put["mid"] <= 0:
            continue
        call_spread = max(call["ask"] - call["bid"], 0.01) if call["ask"] and call["bid"] else 999
        put_spread = max(put["ask"] - put["bid"], 0.01) if put["ask"] and put["bid"] else 999
        liquidity = max(call["volume"] + put["volume"] + call["oi"] + put["oi"], 1)
        estimate = strike + call["mid"] - put["mid"]
        weight = liquidity / (1 + call_spread + put_spread)
        estimates.append((estimate, strike, weight, call["mid"], put["mid"], call_spread + put_spread, liquidity))

    if not estimates:
        raise RuntimeError("No valid SPXW put-call parity pairs")

    rough = statistics.median([x[0] for x in estimates])
    nearby = [x for x in estimates if abs(x[0] - rough) <= 8]
    nearby = sorted(nearby, key=lambda x: x[2], reverse=True)[:18] or sorted(estimates, key=lambda x: x[2], reverse=True)[:18]
    weighted = sum(x[0] * x[2] for x in nearby) / sum(x[2] for x in nearby)
    median = statistics.median(sorted(x[0] for x in nearby))
    return (weighted + median) / 2, sorted(nearby, key=lambda x: x[2], reverse=True)[:12]


def aggregate(rows: list[dict], spot: float, label: str) -> dict:
    if not rows:
        return {
            "label": label,
            "count": 0,
            "net_gex": 0.0,
            "net_vex": 0.0,
            "gex_by_strike": [],
            "vex_by_strike": [],
            "walls": [],
            "pits": [],
            "vanna_walls": [],
            "vanna_pits": [],
            "flips": [],
            "top_call_oi": [],
            "top_put_oi": [],
            "top_volume": [],
        }

    by_strike: dict[float, float] = defaultdict(float)
    by_vanna: dict[float, float] = defaultdict(float)
    call_oi: dict[float, int] = defaultdict(int)
    put_oi: dict[float, int] = defaultdict(int)
    volume: dict[float, int] = defaultdict(int)
    for row in rows:
        by_strike[row["strike"]] += signed_gex(row, spot)
        by_vanna[row["strike"]] += signed_vex(row, spot)
        volume[row["strike"]] += row["volume"]
        if row["type"] == "CALL":
            call_oi[row["strike"]] += row["oi"]
        else:
            put_oi[row["strike"]] += row["oi"]

    grid = []
    s = math.floor((spot - 220) / 5) * 5
    while s <= math.ceil((spot + 220) / 5) * 5:
        grid.append((s, sum(signed_gex(r, s, use_model=True) for r in rows)))
        s += 5
    flips = []
    for (s1, g1), (s2, g2) in zip(grid, grid[1:]):
        if g1 == 0 or g1 * g2 < 0:
            denom = abs(g1) + abs(g2)
            flips.append(s1 + (s2 - s1) * abs(g1) / denom if denom else s1)

    return {
        "label": label,
        "count": len(rows),
        "net_gex": float(sum(signed_gex(r, spot) for r in rows)),
        "net_vex": float(sum(signed_vex(r, spot) for r in rows)),
        "gex_by_strike": [[float(k), float(v)] for k, v in sorted(by_strike.items())],
        "vex_by_strike": [[float(k), float(v)] for k, v in sorted(by_vanna.items())],
        "walls": top_items(by_strike, reverse=True),
        "pits": top_items(by_strike, reverse=False),
        "vanna_walls": top_items(by_vanna, reverse=True),
        "vanna_pits": top_items(by_vanna, reverse=False),
        "flips": [float(x) for x in flips],
        "top_call_oi": [[float(k), int(v)] for k, v in sorted(call_oi.items(), key=lambda kv: kv[1], reverse=True)[:8]],
        "top_put_oi": [[float(k), int(v)] for k, v in sorted(put_oi.items(), key=lambda kv: kv[1], reverse=True)[:8]],
        "top_volume": [[float(k), int(v)] for k, v in sorted(volume.items(), key=lambda kv: kv[1], reverse=True)[:8]],
    }


def money(value: float) -> str:
    sign = "-" if value < 0 else ""
    value = abs(value)
    if value >= 1_000_000_000:
        return f"{sign}{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{sign}{value / 1_000_000:.1f}M"
    return f"{sign}{value:,.0f}"


def levels(items: list[list[float]] | list[float], limit: int = 8) -> str:
    if not items:
        return "无"
    values = []
    for item in items[:limit]:
        if isinstance(item, (list, tuple)):
            values.append(float(item[0]))
        else:
            values.append(float(item))
    return ", ".join(f"{x:g}" for x in values)


def levels_with_value(items: list[list[float]], limit: int = 6) -> str:
    if not items:
        return "无"
    return ", ".join(f"{level:g}({money(value)})" for level, value in items[:limit])


def level_numbers(items: list[list[float]], limit: int = 5) -> str:
    if not items:
        return "无"
    return " / ".join(f"{float(level):.0f}" for level, _ in items[:limit])


def first_level(items: list[list[float]] | list[float]) -> float | None:
    if not items:
        return None
    first = items[0]
    if isinstance(first, (list, tuple)):
        return float(first[0])
    return float(first)


def weekday_label(expiry: str) -> str:
    names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    try:
        return names[datetime.strptime(expiry, "%Y-%m-%d").weekday()]
    except Exception:
        return ""


def parse_strikes(raw: str | None) -> list[float]:
    if not raw:
        return []
    strikes = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        strikes.append(float(item))
    return strikes


def strike_map(bucket: dict, key: str = "gex_by_strike") -> dict[float, float]:
    out = {}
    for level, value in bucket.get(key, []):
        out[float(level)] = float(value)
    if out:
        return out
    for level, value in bucket.get("walls", []) + bucket.get("pits", []):
        out[float(level)] = float(value)
    return out


def sign_label(value: float) -> str:
    if value > 0:
        return "正"
    if value < 0:
        return "负"
    return "零"


def strike_change_label(prev: float, current: float) -> str:
    if prev > 0 and current < 0:
        return "正转负：支撑跑路/降级为加速风险"
    if prev < 0 and current > 0:
        return "负转正：支撑恢复/加速风险缓和"
    if current < 0 and current < prev:
        return "负 gamma 增强：下方加速风险上升"
    if current > 0 and current < prev:
        return "正 gamma 减弱：支撑/钉扎变弱"
    if current > 0 and current > prev:
        return "正 gamma 增强：支撑/钉扎增强"
    if current < 0 and current > prev:
        return "负 gamma 减弱：加速风险缓和"
    return "变化不大"


def default_watch_strikes(prev: dict, current: dict) -> list[float]:
    strikes: set[float] = set()
    spot = float(current.get("spot_anchor", 0) or 0)
    if spot:
        strikes.add(round(spot / 25) * 25)
        strikes.add(round(spot / 50) * 50)
    for result in [prev, current]:
        zero = result.get("buckets", {}).get("0DTE", {})
        for key in ["walls", "pits"]:
            for level, _ in zero.get(key, [])[:4]:
                strikes.add(float(level))
    return sorted(strikes)


def compare_snapshots(prev: dict, current: dict, watch_strikes: list[float]) -> dict:
    if not watch_strikes:
        watch_strikes = default_watch_strikes(prev, current)
    comparison = {
        "previous_generated": prev.get("generated", ""),
        "current_generated": current.get("generated", ""),
        "watched_strikes": watch_strikes,
        "strike_changes": {},
    }
    for bucket_name in ["0DTE", "Next2", "Fri2w", "All"]:
        prev_bucket = prev.get("buckets", {}).get(bucket_name, {})
        current_bucket = current.get("buckets", {}).get(bucket_name, {})
        prev_map = strike_map(prev_bucket)
        current_map = strike_map(current_bucket)
        rows = []
        for strike in watch_strikes:
            if strike not in prev_map or strike not in current_map:
                continue
            prev_value = prev_map[strike]
            current_value = current_map[strike]
            delta = current_value - prev_value
            sign_changed = (prev_value > 0 > current_value) or (prev_value < 0 < current_value)
            material = sign_changed or abs(delta) >= 250_000_000 or abs(current_value) >= 500_000_000
            if not material:
                continue
            rows.append(
                {
                    "strike": strike,
                    "previous_gex": prev_value,
                    "current_gex": current_value,
                    "delta": delta,
                    "previous_sign": sign_label(prev_value),
                    "current_sign": sign_label(current_value),
                    "label": strike_change_label(prev_value, current_value),
                }
            )
        if rows:
            comparison["strike_changes"][bucket_name] = rows
    return comparison


def render_comparison(comparison: dict) -> list[str]:
    changes = comparison.get("strike_changes", {})
    if not changes:
        return []
    zero = changes.get("0DTE", [])
    all_rows = changes.get("All", [])
    near_rows = changes.get("Next2", []) + changes.get("Fri2w", [])

    def levels_for(rows: list[dict], predicate, limit: int = 4) -> str:
        selected = [row for row in rows if predicate(row)]
        selected = sorted(selected, key=lambda row: abs(row["current_gex"]), reverse=True)[:limit]
        return ", ".join(f"{row['strike']:g}" for row in selected) if selected else ""

    support_lost = levels_for(zero, lambda row: row["previous_gex"] > 0 > row["current_gex"])
    downside_risk = levels_for(zero, lambda row: row["current_gex"] < 0 and row["delta"] < 0)
    broad_downside = levels_for(all_rows or near_rows, lambda row: row["current_gex"] < 0 and row["delta"] < 0)
    positive_weaker = levels_for(zero, lambda row: row["current_gex"] > 0 and row["delta"] < 0)

    lines = ["", "结构变化解读："]
    if support_lost:
        lines.append(f"- 支撑质量恶化：{support_lost} 一带出现正转负，原先的钉扎/缓冲消失，回踩更容易变成顺势下探。")
    elif downside_risk:
        lines.append(f"- 下方风险增强：{downside_risk} 一带负 gamma 继续加深，说明这里不是稳固支撑，更像破位后的加速/磁吸区。")
    else:
        lines.append("- 支撑没有明显恢复：未看到关键下方执行价从负转正，短线反弹仍需要价格重新站回 flip 才能确认。")

    if broad_downside:
        lines.append(f"- 风险重心下移：近端/全窗口负 gamma 压力集中在 {broad_downside} 一带，预示跌破第一道防线后容易向下一组流动性区扩散。")
    if positive_weaker:
        lines.append(f"- 上方钉扎变弱：{positive_weaker} 一带正 gamma 减弱，反弹阻尼下降但也代表承接变薄，盘中更容易急涨急跌。")
    lines.append("- 交易含义：这类变化本身通常不是第一卖因，但会在价格跌破 flip 或关键位后放大现货卖压；要用价格是否快速收回关键位来确认支撑是否真的还在。")
    return lines


def render_text_report(result: dict) -> str:
    spot = result["spot_anchor"]
    zero = result["buckets"].get("0DTE", {})
    all_bucket = result["buckets"].get("All", {})
    next2 = result["buckets"].get("Next2", {})
    fri2w = result["buckets"].get("Fri2w", {})
    zero_regime = "正 gamma" if zero.get("net_gex", 0) > 0 else "负 gamma"
    all_regime = "正 gamma" if all_bucket.get("net_gex", 0) > 0 else "负 gamma"
    top_wall = zero.get("walls", [[None, 0]])[0][0] if zero.get("walls") else None
    top_pit = zero.get("pits", [[None, 0]])[0][0] if zero.get("pits") else None
    wall_text = f"{top_wall:g}" if top_wall is not None else "无"
    pit_text = f"{top_pit:g}" if top_pit is not None else "无"

    lines = [
            "SPX/SPXW intraday gamma memo",
            "",
            f"一句话：SPX 锚点 {spot:.2f}（{result.get('spot_method', '')}），0DTE 为 {zero_regime}，全窗口为 {all_regime}；0DTE 主 wall {wall_text}，主 pit {pit_text}。",
            f"我会怎么做：先把 {levels(zero.get('walls', []), 4)} 当作上方钉扎/阻力观察，把 {levels(zero.get('pits', []), 4)} 当作下方加速风险区；突破或跌破后再用期指、成交和宏观 tape 确认。",
            f"什么情况说明我错了：若价格穿越 0DTE flip {levels(zero.get('flips', []), 4)} 后没有延续，说明当日期权地图被现货流或宏观消息覆盖。",
            "",
            "0DTE：",
            f"- 净 GEX: {money(zero.get('net_gex', 0))}; 净 VEX: {money(zero.get('net_vex', 0))}; 样本数: {zero.get('count', 0)}",
            f"- Gamma walls: {levels_with_value(zero.get('walls', []))}",
            f"- Gamma pits: {levels_with_value(zero.get('pits', []))}",
            f"- Vanna positive zones: {levels_with_value(zero.get('vanna_walls', []))}",
            f"- Vanna negative zones: {levels_with_value(zero.get('vanna_pits', []))}",
            "",
            "近端窗口：",
            f"- Next2 walls: {levels_with_value(next2.get('walls', []), 5)}",
            f"- Next2 pits: {levels_with_value(next2.get('pits', []), 5)}",
            f"- Fri2w walls: {levels_with_value(fri2w.get('walls', []), 5)}",
            f"- Fri2w pits: {levels_with_value(fri2w.get('pits', []), 5)}",
            "",
            f"数据：生成 {result.get('generated', '')}; 到期日 {', '.join(result.get('expiries', []))}; SPY 只作 sanity check，不作为 SPX 点位换算主流程。",
    ]
    lines.extend(render_comparison(result.get("comparison", {})))
    return "\n".join(lines)


def expiry_bias(bucket: dict, spot: float) -> str:
    net = float(bucket.get("net_gex", 0) or 0)
    flip = first_level(bucket.get("flips", []))
    if net < -7_000_000_000:
        return "最弱/偏弱"
    if net < -2_500_000_000:
        return "偏弱"
    if net < 0:
        return "弱势缓和"
    if flip and spot >= flip:
        return "偏修复"
    return "中性偏修复"


def render_by_expiry_report(result: dict) -> str:
    spot = float(result["spot_anchor"])
    per_expiry = result.get("per_expiry", {})
    expiries = [expiry for expiry in result.get("expiries", []) if expiry in per_expiry]
    if not expiries:
        return render_text_report(result)

    future_flips = [
        first_level(per_expiry[e].get("flips", []))
        for e in expiries[1:4]
        if first_level(per_expiry[e].get("flips", []))
    ]
    flips = future_flips or [first_level(per_expiry[e].get("flips", [])) for e in expiries if first_level(per_expiry[e].get("flips", []))]
    repair_low = min(flips) if flips else None
    repair_high = max(flips[:4]) if flips else None
    today = expiries[0]
    today_bucket = per_expiry[today]
    first_resistance = first_level(today_bucket.get("walls", []))
    first_risk = first_level(today_bucket.get("pits", []))

    if repair_low and repair_high and repair_high - repair_low >= 15:
        repair_text = f"{repair_low:.0f}-{repair_high:.0f}"
    elif repair_low:
        repair_text = f"{repair_low:.0f}"
    else:
        repair_text = "主要 flip 区"
    resistance_text = f"{first_resistance:.0f}" if first_resistance else "第一压力"
    risk_text = f"{first_risk:.0f}" if first_risk else "第一风险位"

    net_values = [(expiry, float(per_expiry[expiry].get("net_gex", 0) or 0)) for expiry in expiries]
    weakest = min(net_values, key=lambda item: item[1])[0]
    easing = [expiry for expiry, net in net_values if expiry != weakest and net < 0 and abs(net) < abs(net_values[0][1]) * 0.45]
    easing_text = "、".join(easing[:2]) if easing else ""

    lines = [
        "SPX/SPXW future-days gamma memo",
        "",
        f"从“未来几天 gamma”角度看：现价约 {spot:.0f}，短线还没修复，未来几天更像高波动、反弹先看卖压；除非先收回 {resistance_text}，进一步站上 {repair_text}。",
        "",
        "按具体到期日看：",
    ]

    for idx, expiry in enumerate(expiries):
        bucket = per_expiry[expiry]
        net = float(bucket.get("net_gex", 0) or 0)
        flip = first_level(bucket.get("flips", []))
        walls = level_numbers(bucket.get("walls", []), 5)
        pits = level_numbers(bucket.get("pits", []), 5)
        flip_text = f"{flip:.0f}" if flip else "NA"
        bias = expiry_bias(bucket, spot)
        day = weekday_label(expiry)
        if idx == 0:
            lead = "当天到期"
        elif idx <= 2:
            lead = "近端到期"
        else:
            lead = "后续到期"
        if net < 0 and flip and spot < flip:
            meaning = f"现价在 flip {flip_text} 下方，仍是负 gamma 压制；反弹到上方压力位更容易先遇到卖压。"
        elif net < 0:
            meaning = "净 GEX 仍为负，说明结构还没有切回稳定钉扎。"
        else:
            meaning = "净 GEX 转正，结构开始偏向钉扎/均值回归，但仍要看价格是否守住关键位。"
        lines.extend(
            [
                "",
                f"**{expiry} {day}，{lead}：{bias}**",
                f"净 GEX {money(net)}，flip {flip_text}。下方风险主要在 {pits}；上方压力/钉扎在 {walls}。{meaning}",
            ]
        )

    lines.extend(
        [
            "",
            "我的推演：",
            "",
            f"**基准情形**：围绕 {risk_text} 到 {resistance_text} 高波动震荡，反弹先看能否站稳第一压力；站不上，仍是弱势结构。",
            f"**偏空情形**：跌破 {risk_text} 后反抽弱，容易继续向下一组 put gamma 风险位扩散。",
            f"**修复情形**：先重新站回 {resistance_text}，再看 {repair_text}；只有站上主要 future flip 区，未来几天才可能从“下跌放大”切回“震荡修复”。",
            "",
            f"所以按日期结论是：{weakest} 最弱；" + (f"{easing_text} 的弱势开始缓和但还没转强；" if easing_text else "") + f"真正修复要看价格能否重新站上 {repair_text}。",
            "",
            f"数据：生成 {result.get('generated', '')}; 到期日 {', '.join(expiries)}; SPY 只作 sanity check，不作为 SPX 点位换算主流程。",
        ]
    )
    lines.extend(render_comparison(result.get("comparison", {})))
    return "\n".join(lines)


def get_option_chain(ctx, expiry: str, strike_min: float, strike_max: float, retry_delay: float):
    ret, chain = ctx.get_option_chain(UNDERLYING, start=expiry, end=expiry)
    if ret != RET_OK and "频率" in str(chain):
        time.sleep(retry_delay)
        ret, chain = ctx.get_option_chain(UNDERLYING, start=expiry, end=expiry)
    if ret != RET_OK:
        raise RuntimeError(chain)
    return chain[(chain["strike_price"] >= strike_min) & (chain["strike_price"] <= strike_max)].copy()


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a SPX/SPXW intraday gamma text memo")
    parser.add_argument("--json-output", help="Optional JSON path; use only when a raw data file is explicitly requested")
    parser.add_argument("--output", dest="json_output", help=argparse.SUPPRESS)
    parser.add_argument("--compare-json", help="Previous JSON snapshot to compare against")
    parser.add_argument("--watch-strikes", help="Comma-separated strikes to compare, e.g. 7400,7425,7450")
    parser.add_argument("--by-expiry-report", action="store_true", help="Render each selected expiry date separately for future-days gamma reads")
    parser.add_argument("--strike-min", type=float, default=6600)
    parser.add_argument("--strike-max", type=float, default=8200)
    parser.add_argument("--future-count", type=int, default=4)
    parser.add_argument("--chain-delay", type=float, default=OPTION_CHAIN_DELAY_SECONDS)
    parser.add_argument("--retry-delay", type=float, default=OPTION_CHAIN_RETRY_DELAY_SECONDS)
    args = parser.parse_args()

    ctx = create_quote_context()
    try:
        _, spy_df = ctx.get_market_snapshot([SPY])
        spy = spy_df.iloc[0].to_dict() if len(spy_df) else {}

        ret, exp_df = ctx.get_option_expiration_date(UNDERLYING)
        if ret != RET_OK:
            raise RuntimeError(exp_df)
        expiries = []
        for x in exp_df["strike_time"].tolist():
            sx = str(x)
            if sx not in expiries:
                expiries.append(sx)
        if not expiries:
            raise RuntimeError("No SPX option expiries returned")

        today = expiries[0]
        near_expiries = expiries[1 : 1 + max(args.future_count, 0)]
        friday_expiries = [x for x in expiries[1:] if datetime.strptime(x, "%Y-%m-%d").weekday() == 4][:2]
        selected_expiries = []
        for expiry in [today, *near_expiries, *friday_expiries]:
            if expiry not in selected_expiries:
                selected_expiries.append(expiry)

        chain_frames = []
        for idx, expiry in enumerate(selected_expiries):
            if idx:
                time.sleep(args.chain_delay)
            chain = get_option_chain(ctx, expiry, args.strike_min, args.strike_max, args.retry_delay)
            if expiry == today:
                chain = chain[
                    (chain["expiration_cycle"].astype(str) == "WEEK")
                    & (chain["option_settlement_mode"].astype(str) == "PM")
                    & (chain["name"].astype(str).str.contains("SPXW"))
                ]
            chain_frames.append(chain)

        codes = []
        meta = {}
        for chain in chain_frames:
            for _, r in chain.iterrows():
                code = str(r["code"])
                expiry = str(r["strike_time"])
                codes.append(code)
                meta[code] = {
                    "expiry": expiry,
                    "bucket": "0DTE" if expiry == today else "FUTURE",
                    "type": str(r["option_type"]).upper(),
                    "strike": f(r["strike_price"]),
                    "name": str(r["name"]),
                }

        rows = []
        for start in range(0, len(codes), 350):
            ret, snap = ctx.get_market_snapshot(codes[start : start + 350])
            if ret != RET_OK:
                raise RuntimeError(snap)
            for _, r in snap.iterrows():
                code = str(r["code"])
                m = meta.get(code)
                if not m:
                    continue
                row = {
                    **m,
                    "oi": i(r.get("option_open_interest")),
                    "volume": i(r.get("volume")),
                    "bid": f(r.get("bid_price")),
                    "ask": f(r.get("ask_price")),
                    "last": f(r.get("last_price")),
                    "iv": f(r.get("option_implied_volatility")) / 100.0,
                    "delta": f(r.get("option_delta")),
                    "gamma": f(r.get("option_gamma")),
                    "dte": f(r.get("option_expiry_date_distance")),
                }
                row["mid"] = mid(r)
                if row["oi"] > 0 and row["strike"] > 0 and row["iv"] > 0 and row["gamma"] > 0:
                    rows.append(row)

        spot, parity = weighted_anchor_from_parity(rows)
        future_expiries = sorted({r["expiry"] for r in rows if r["expiry"] != today})
        next2 = set(future_expiries[:2])
        friday2 = set([x for x in future_expiries if datetime.strptime(x, "%Y-%m-%d").weekday() == 4][:2])

        buckets = {
            "0DTE": aggregate([r for r in rows if r["bucket"] == "0DTE"], spot, "0DTE SPXW PM"),
            "Next2": aggregate([r for r in rows if r["expiry"] in next2], spot, "Next 2 listed expiries"),
            "Fri2w": aggregate([r for r in rows if r["expiry"] in friday2], spot, "Next two Friday expiries"),
            "All": aggregate(rows, spot, "All selected near expiries"),
        }
        per_expiry = {
            expiry: aggregate([r for r in rows if r["expiry"] == expiry], spot, f"Expiry {expiry}")
            for expiry in selected_expiries
        }

        out = {
            "generated": datetime.now().isoformat(timespec="seconds"),
            "spot_anchor": spot,
            "spot_method": "SPXW 0DTE put-call parity weighted median/trimmed mean; SPY only sanity check",
            "spy_snapshot": {k: str(spy.get(k, "")) for k in ["last_price", "bid_price", "ask_price", "update_time", "open_price", "high_price", "low_price", "prev_close_price"]},
            "parity_estimates_near_spot": parity,
            "row_count": len(rows),
            "expiries": selected_expiries,
            "filters": {"0DTE": "SPXW + PM settled only", "strike_window": [args.strike_min, args.strike_max]},
            "buckets": buckets,
            "per_expiry": per_expiry,
        }
        if args.compare_json:
            previous = json.loads(Path(args.compare_json).read_text(encoding="utf-8"))
            out["comparison"] = compare_snapshots(previous, out, parse_strikes(args.watch_strikes))
        print(render_by_expiry_report(out) if args.by_expiry_report else render_text_report(out))
        if args.json_output:
            path = Path(args.json_output)
            path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"\nJSON data: {path}")
    finally:
        safe_close(ctx)


if __name__ == "__main__":
    main()
