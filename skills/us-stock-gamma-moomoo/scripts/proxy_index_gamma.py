#!/usr/bin/env python3
"""Convert ETF option gamma levels to a live index/CFD anchor.

For markets without local index-option chains in moomoo, such as Nikkei 225
for a US session workflow, use a liquid ETF option chain as the positioning
proxy and convert ETF strikes with a same-session index/ETF ratio.
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
from common import RET_OK, create_quote_context, safe_close  # noqa: E402


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert ETF option gamma levels to an index/CFD anchor")
    parser.add_argument("proxy_symbol", nargs="?", default="US.EWJ", help="ETF option proxy, e.g. US.EWJ")
    parser.add_argument("--index-anchor", type=float, required=True, help="Current index/CFD anchor, e.g. Nikkei 225 CFD")
    parser.add_argument("--index-name", default="日经225 CFD")
    parser.add_argument("--round-to", type=float, default=50)
    parser.add_argument("--months", type=int, default=1)
    parser.add_argument("--output", help="Output JSON path")
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
        etf_spot = pre or ((bid + ask) / 2 if bid > 0 and ask > 0 else last)
        if etf_spot <= 0:
            raise RuntimeError("Proxy ETF spot is unavailable")
        ratio = args.index_anchor / etf_spot

        ret, exp_df = ctx.get_option_expiration_date(args.proxy_symbol)
        if ret != RET_OK:
            raise RuntimeError(exp_df)
        quote_dt = parse_quote_date(stock.get("update_time", ""))
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
            "index_anchor": args.index_anchor,
            "proxy_symbol": args.proxy_symbol,
            "proxy_spot": etf_spot,
            "conversion": {
                "method": "index_level = ETF_strike * (index_anchor / proxy_spot)",
                "ratio": ratio,
                "round_to": args.round_to,
                "limitation": "This is a proxy positioning map, not a domestic index-option dealer book.",
            },
            "stock_snapshot": {
                "last": last,
                "pre_or_after": pre,
                "bid": bid,
                "ask": ask,
                "update_time": str(stock.get("update_time", "")),
            },
            "selected_expiries": expiries,
            "buckets": {"ALL": aggregate(rows, etf_spot, ratio, args.round_to), **expiry_buckets},
        }
        path = Path(args.output) if args.output else SCRIPT_DIR / f"{args.proxy_symbol.split('.')[-1].lower()}_proxy_index_gamma_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        safe_close(ctx)


if __name__ == "__main__":
    main()
