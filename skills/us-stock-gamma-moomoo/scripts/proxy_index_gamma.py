#!/usr/bin/env python3
"""Convert ETF option gamma levels to a time-aligned index/futures anchor.

For markets without local index-option chains in moomoo, such as Nikkei 225
for a US session workflow, use a liquid ETF option chain as the positioning
proxy. If the ETF is closed, convert ETF strikes with the index/futures value
at the ETF quote timestamp, then optionally bridge that futures level to the
current target index/CFD level.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path.home() / ".codex/skills/moomooapi/scripts"))
from common import KLType, RET_OK, create_quote_context, safe_close  # noqa: E402


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


def normal_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def bs_vanna(spot: float, strike: float, iv: float, dte: float) -> float:
    if spot <= 0 or strike <= 0 or iv <= 0:
        return 0.0
    t = max(dte, 0.25) / 365.0
    sqrt_t = math.sqrt(t)
    d1 = (math.log(spot / strike) + 0.5 * iv * iv * t) / (iv * sqrt_t)
    d2 = d1 - iv * sqrt_t
    return -normal_pdf(d1) * d2 / iv


def parse_quote_date(value) -> datetime:
    try:
        return datetime.strptime(str(value).split(".")[0], "%Y-%m-%d %H:%M:%S")
    except Exception:
        return datetime.now()


def snapshot_price(ctx, symbol: str) -> tuple[float, dict]:
    ret, df = ctx.get_market_snapshot([symbol])
    if ret != RET_OK or len(df) == 0:
        return 0.0, {"error": str(df)}
    row = df.iloc[0]
    bid = f(row.get("bid_price"))
    ask = f(row.get("ask_price"))
    last = f(row.get("last_price")) or f(row.get("cur_price"))
    price = (bid + ask) / 2 if bid > 0 and ask > 0 else last
    return price, {
        "symbol": symbol,
        "last": last,
        "bid": bid,
        "ask": ask,
        "update_time": str(row.get("update_time", "")),
        "name": str(row.get("name", "")),
    }


def historical_close_near(ctx, symbol: str, target_dt: datetime, tolerance_minutes: int) -> tuple[float, dict]:
    """Return the nearest 1-minute close at or before target_dt when available."""
    start = target_dt.strftime("%Y-%m-%d")
    ret, df, _ = ctx.request_history_kline(
        symbol,
        start=start,
        end=start,
        ktype=KLType.K_1M,
        max_count=1000,
    )
    if ret != RET_OK or len(df) == 0:
        return 0.0, {"error": str(df)}

    best = None
    for _, row in df.iterrows():
        try:
            t = datetime.strptime(str(row.get("time_key", "")).split(".")[0], "%Y-%m-%d %H:%M:%S")
        except Exception:
            continue
        if t <= target_dt:
            best = (t, f(row.get("close")))
    if not best:
        return 0.0, {"error": f"no bar at or before {target_dt.isoformat(timespec='seconds')}"}
    t, close = best
    gap = abs((target_dt - t).total_seconds()) / 60
    if gap > tolerance_minutes:
        return 0.0, {"error": f"nearest bar {t.isoformat(timespec='seconds')} exceeds tolerance {tolerance_minutes}m"}
    return close, {"symbol": symbol, "time": t.isoformat(timespec="seconds"), "close": close, "gap_minutes": gap}


def build_conversion(args, ctx, proxy_spot: float, proxy_time: datetime) -> tuple[float, dict]:
    if args.direct_index_anchor:
        ratio = args.direct_index_anchor / proxy_spot
        return ratio, {
            "method": "direct: index_level = ETF_strike * (direct_index_anchor / proxy_spot)",
            "ratio": ratio,
            "proxy_time": proxy_time.isoformat(timespec="seconds"),
            "direct_index_anchor": args.direct_index_anchor,
            "round_to": args.round_to,
            "limitation": "Direct conversion is only valid when the index anchor and ETF spot are time-aligned.",
        }

    bridge_at_proxy_time = args.bridge_anchor_at_proxy_time
    bridge_at_proxy_source = {"source": "manual", "value": bridge_at_proxy_time}
    if not bridge_at_proxy_time and args.bridge_symbol:
        bridge_at_proxy_time, bridge_at_proxy_source = historical_close_near(
            ctx, args.bridge_symbol, proxy_time, args.time_tolerance_minutes
        )
    if not bridge_at_proxy_time:
        raise RuntimeError(
            "Missing time-aligned bridge anchor. Provide --bridge-anchor-at-proxy-time "
            "with the NKDmain/CFD value at the EWJ quote time, or enable historical access for --bridge-symbol."
        )

    bridge_current = args.bridge_current
    bridge_current_source = {"source": "manual", "value": bridge_current}
    if not bridge_current and args.bridge_symbol:
        bridge_current, bridge_current_source = snapshot_price(ctx, args.bridge_symbol)
    if not bridge_current:
        bridge_current = bridge_at_proxy_time
        bridge_current_source = {"source": "fallback_to_bridge_at_proxy_time", "value": bridge_current}

    final_anchor = args.final_anchor
    final_source = {"source": "manual", "value": final_anchor}
    if not final_anchor and args.final_symbol:
        final_anchor, final_source = snapshot_price(ctx, args.final_symbol)
    if not final_anchor:
        final_anchor = bridge_current
        final_source = {"source": "fallback_to_bridge_current", "value": final_anchor}

    bridge_ratio = bridge_at_proxy_time / proxy_spot
    final_bridge_ratio = final_anchor / bridge_current
    ratio = bridge_ratio * final_bridge_ratio
    return ratio, {
        "method": "two_step: ETF_strike -> bridge at ETF quote time -> current final index/CFD",
        "formula": "final_level = ETF_strike * (bridge_at_proxy_time / proxy_spot) * (final_anchor / bridge_current)",
        "ratio": ratio,
        "bridge_ratio_at_proxy_time": bridge_ratio,
        "final_to_bridge_current_ratio": final_bridge_ratio,
        "proxy_time": proxy_time.isoformat(timespec="seconds"),
        "proxy_spot": proxy_spot,
        "bridge_symbol": args.bridge_symbol,
        "bridge_at_proxy_time": bridge_at_proxy_time,
        "bridge_at_proxy_source": bridge_at_proxy_source,
        "bridge_current": bridge_current,
        "bridge_current_source": bridge_current_source,
        "final_symbol": args.final_symbol,
        "final_anchor": final_anchor,
        "final_source": final_source,
        "round_to": args.round_to,
        "limitation": "This is a proxy positioning map. EWJ options reflect US-listed Japan ETF positioning plus FX/ETF-flow effects, not the full domestic Nikkei option dealer book.",
    }


def choose_expiries(expiries: list[str], quote_dt: datetime, extra_months: int) -> list[str]:
    parsed = []
    for value in expiries:
        try:
            d = datetime.strptime(str(value), "%Y-%m-%d")
        except Exception:
            continue
        if d.date() >= quote_dt.date():
            parsed.append(d)
    parsed = sorted(dict.fromkeys(parsed))

    selected = [d for d in parsed if d.date() <= (quote_dt + timedelta(days=14)).date()]
    monthly = [d for d in parsed if 15 <= d.day <= 21]
    monthly_added = 0
    for d in monthly:
        if d not in selected:
            selected.append(d)
            monthly_added += 1
        if monthly_added >= extra_months:
            break
    return [d.strftime("%Y-%m-%d") for d in sorted(dict.fromkeys(selected))]


def round_level(value: float, step: float) -> float:
    if step <= 0:
        return value
    return round(value / step) * step


def signed_gex(row: dict, spot: float) -> float:
    sign = 1 if row["type"] == "CALL" else -1
    return sign * row["gamma"] * row["oi"] * 100 * spot * spot * 0.01


def signed_vex(row: dict, spot: float) -> float:
    sign = 1 if row["type"] == "CALL" else -1
    return sign * bs_vanna(spot, row["strike"], row["iv"], row["dte"]) * row["oi"] * 100 * spot * 0.01


def top(mapping: dict[float, float], reverse: bool = True, n: int = 12) -> list[list[float]]:
    return [[float(k), float(v)] for k, v in sorted(mapping.items(), key=lambda kv: kv[1], reverse=reverse)[:n]]


def money(value: float) -> str:
    sign = "-" if value < 0 else ""
    value = abs(value)
    if value >= 1_000_000_000:
        return f"{sign}{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{sign}{value / 1_000_000:.1f}M"
    return f"{sign}{value:,.0f}"


def level_list(items: list[list[float]], limit: int = 6) -> str:
    if not items:
        return "无"
    return ", ".join(f"{level:g}({money(value)})" for level, value in items[:limit])


def aggregate(rows: list[dict], etf_spot: float, ratio: float, round_to: float) -> dict:
    by_index: dict[float, float] = {}
    by_vanna: dict[float, float] = {}
    call_oi: dict[float, int] = {}
    put_oi: dict[float, int] = {}
    for row in rows:
        level = round_level(row["strike"] * ratio, round_to)
        by_index[level] = by_index.get(level, 0.0) + signed_gex(row, etf_spot)
        by_vanna[level] = by_vanna.get(level, 0.0) + signed_vex(row, etf_spot)
        if row["type"] == "CALL":
            call_oi[level] = call_oi.get(level, 0) + row["oi"]
        else:
            put_oi[level] = put_oi.get(level, 0) + row["oi"]

    return {
        "count": len(rows),
        "net_gex_proxy": float(sum(signed_gex(r, etf_spot) for r in rows)),
        "net_vex_proxy": float(sum(signed_vex(r, etf_spot) for r in rows)),
        "index_walls": top(by_index, True),
        "index_pits": top(by_index, False),
        "index_vanna_walls": top(by_vanna, True),
        "index_vanna_pits": top(by_vanna, False),
        "index_call_oi": [[float(k), int(v)] for k, v in sorted(call_oi.items(), key=lambda kv: kv[1], reverse=True)[:10]],
        "index_put_oi": [[float(k), int(v)] for k, v in sorted(put_oi.items(), key=lambda kv: kv[1], reverse=True)[:10]],
    }


def render_text(result: dict) -> str:
    all_bucket = result["buckets"].get("ALL", {})
    conversion = result["conversion"]
    ratio = conversion.get("ratio", 0)
    regime = "正 gamma" if all_bucket.get("net_gex_proxy", 0) > 0 else "负 gamma"
    walls = all_bucket.get("index_walls", [])
    pits = all_bucket.get("index_pits", [])
    top_wall = f"{walls[0][0]:g}" if walls else "无"
    top_pit = f"{pits[0][0]:g}" if pits else "无"

    return "\n".join(
        [
            f"{result['index_name']} proxy gamma memo",
            "",
            f"一句话：用 {result['proxy_symbol']} 期权链换算到指数锚点，当前全窗口为 {regime}；主 wall {top_wall}，主 pit {top_pit}。",
            f"我会怎么做：把 {level_list(walls, 4)} 当作上方钉扎/阻力，把 {level_list(pits, 4)} 当作下方加速风险区；必须结合日经期货/CFD 实时价格确认。",
            "什么情况说明我错了：若日经现货/期货流直接穿越这些换算位且不回头，说明 EWJ 代理期权流不足以主导当下指数盘。",
            "",
            "换算：",
            f"- Method: {conversion.get('method', '')}",
            f"- Ratio: {ratio:.6f}; proxy spot: {result.get('proxy_spot', 0):.3f}; round_to: {conversion.get('round_to', '')}",
            f"- Proxy anchor time: {result['stock_snapshot'].get('proxy_anchor_time_used', '')}",
            f"- Limitation: {conversion.get('limitation', '')}",
            "",
            "关键位：",
            f"- Net GEX proxy: {money(all_bucket.get('net_gex_proxy', 0))}; Net VEX proxy: {money(all_bucket.get('net_vex_proxy', 0))}; 样本数: {all_bucket.get('count', 0)}",
            f"- Index gamma walls: {level_list(walls)}",
            f"- Index gamma pits: {level_list(pits)}",
            f"- Index vanna positive zones: {level_list(all_bucket.get('index_vanna_walls', []))}",
            f"- Index vanna negative zones: {level_list(all_bucket.get('index_vanna_pits', []))}",
            "",
            f"数据：生成 {result.get('generated', '')}; 到期日 {', '.join(result.get('selected_expiries', []))}。EWJ 是代理簿，不是日本本土日经期权全量 dealer book。",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert ETF option gamma levels to an index/CFD anchor")
    parser.add_argument("proxy_symbol", nargs="?", default="US.EWJ", help="ETF option proxy, e.g. US.EWJ")
    parser.add_argument("--index-name", default="日经225 / NKD-NIY proxy")
    parser.add_argument("--proxy-spot-at-anchor-time", type=float, help="Override proxy ETF spot at the chosen anchor time, e.g. EWJ overnight quote at Japan close")
    parser.add_argument("--proxy-anchor-time", help="Override proxy anchor timestamp, e.g. 2026-05-15T15:30:00+09:00")
    parser.add_argument("--bridge-symbol", default="US.NKDmain", help="Time-aligned bridge futures/CFD symbol, e.g. US.NKDmain")
    parser.add_argument("--final-symbol", default="US.NIYmain", help="Current final index/CFD symbol, e.g. US.NIYmain")
    parser.add_argument("--bridge-anchor-at-proxy-time", type=float, help="Bridge value at the proxy ETF quote time, e.g. NKDmain when EWJ closed")
    parser.add_argument("--bridge-current", type=float, help="Current bridge value, e.g. current NKDmain")
    parser.add_argument("--final-anchor", type=float, help="Current final index/CFD value, e.g. current NIYmain")
    parser.add_argument("--direct-index-anchor", type=float, help="Fallback direct index anchor; only valid if time-aligned with the ETF spot")
    parser.add_argument("--round-to", type=float, default=50)
    parser.add_argument("--months", type=int, default=1)
    parser.add_argument("--time-tolerance-minutes", type=int, default=10)
    parser.add_argument("--json-output", help="Optional JSON path; use only when a raw data file is explicitly requested")
    parser.add_argument("--output", dest="json_output", help=argparse.SUPPRESS)
    parser.add_argument("--chain-delay", type=float, default=OPTION_CHAIN_DELAY_SECONDS)
    parser.add_argument("--retry-delay", type=float, default=OPTION_CHAIN_RETRY_DELAY_SECONDS)
    args = parser.parse_args()

    ctx = create_quote_context()
    try:
        ret, stock_df = ctx.get_market_snapshot([args.proxy_symbol])
        if ret != RET_OK:
            raise RuntimeError(stock_df)
        stock = stock_df.iloc[0]
        last = f(stock.get("last_price"))
        pre = f(stock.get("pre_price")) or f(stock.get("after_price"))
        bid = f(stock.get("bid_price"))
        ask = f(stock.get("ask_price"))
        etf_spot = args.proxy_spot_at_anchor_time or pre or ((bid + ask) / 2 if bid > 0 and ask > 0 else last)
        if etf_spot <= 0:
            raise RuntimeError("Proxy ETF spot is unavailable")
        quote_dt = parse_quote_date(args.proxy_anchor_time or stock.get("update_time", ""))
        ratio, conversion = build_conversion(args, ctx, etf_spot, quote_dt)

        ret, exp_df = ctx.get_option_expiration_date(args.proxy_symbol)
        if ret != RET_OK:
            raise RuntimeError(exp_df)
        expiries = choose_expiries([str(x) for x in exp_df["strike_time"].tolist()], quote_dt, args.months)

        rows = []
        by_expiry: dict[str, list[dict]] = {}
        for idx, expiry in enumerate(expiries):
            if idx:
                time.sleep(args.chain_delay)
            ret, chain = ctx.get_option_chain(args.proxy_symbol, start=expiry, end=expiry)
            if ret != RET_OK and "频率" in str(chain):
                time.sleep(args.retry_delay)
                ret, chain = ctx.get_option_chain(args.proxy_symbol, start=expiry, end=expiry)
            if ret != RET_OK:
                by_expiry[expiry] = [{"error": str(chain)}]
                continue
            codes = [str(x) for x in chain["code"].dropna().tolist()]
            expiry_rows = []
            for start in range(0, len(codes), 350):
                ret, snap = ctx.get_market_snapshot(codes[start : start + 350])
                if ret != RET_OK:
                    raise RuntimeError(snap)
                for _, r in snap.iterrows():
                    option_type = str(r.get("option_type", "")).upper()
                    row = {
                        "expiry": expiry,
                        "type": option_type,
                        "strike": f(r.get("option_strike_price")),
                        "oi": i(r.get("option_open_interest")),
                        "volume": i(r.get("volume")),
                        "iv": f(r.get("option_implied_volatility")) / 100.0,
                        "gamma": f(r.get("option_gamma")),
                        "dte": f(r.get("option_expiry_date_distance")),
                    }
                    if option_type in {"CALL", "PUT"} and row["strike"] > 0 and row["oi"] > 0 and row["iv"] > 0 and row["gamma"] > 0:
                        expiry_rows.append(row)
                        rows.append(row)
            by_expiry[expiry] = expiry_rows

        expiry_buckets = {expiry: aggregate(items, etf_spot, ratio, args.round_to) for expiry, items in by_expiry.items() if items and "error" not in items[0]}
        result = {
            "generated": datetime.now().isoformat(timespec="seconds"),
            "index_name": args.index_name,
            "proxy_symbol": args.proxy_symbol,
            "proxy_spot": etf_spot,
            "conversion": conversion,
            "stock_snapshot": {
                "last": last,
                "pre_or_after": pre,
                "bid": bid,
                "ask": ask,
                "update_time": str(stock.get("update_time", "")),
                "proxy_spot_used": etf_spot,
                "proxy_anchor_time_used": quote_dt.isoformat(timespec="seconds"),
            },
            "selected_expiries": expiries,
            "buckets": {"ALL": aggregate(rows, etf_spot, ratio, args.round_to), **expiry_buckets},
        }
        print(render_text(result))
        if args.json_output:
            path = Path(args.json_output)
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"\nJSON data: {path}")
    finally:
        safe_close(ctx)


if __name__ == "__main__":
    main()
