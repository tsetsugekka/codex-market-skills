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
        "walls": top_items(by_strike, reverse=True),
        "pits": top_items(by_strike, reverse=False),
        "vanna_walls": top_items(by_vanna, reverse=True),
        "vanna_pits": top_items(by_vanna, reverse=False),
        "flips": [float(x) for x in flips],
        "top_call_oi": [[float(k), int(v)] for k, v in sorted(call_oi.items(), key=lambda kv: kv[1], reverse=True)[:8]],
        "top_put_oi": [[float(k), int(v)] for k, v in sorted(put_oi.items(), key=lambda kv: kv[1], reverse=True)[:8]],
        "top_volume": [[float(k), int(v)] for k, v in sorted(volume.items(), key=lambda kv: kv[1], reverse=True)[:8]],
    }


def get_option_chain(ctx, expiry: str, strike_min: float, strike_max: float, retry_delay: float):
    ret, chain = ctx.get_option_chain(UNDERLYING, start=expiry, end=expiry)
    if ret != RET_OK and "频率" in str(chain):
        time.sleep(retry_delay)
        ret, chain = ctx.get_option_chain(UNDERLYING, start=expiry, end=expiry)
    if ret != RET_OK:
        raise RuntimeError(chain)
    return chain[(chain["strike_price"] >= strike_min) & (chain["strike_price"] <= strike_max)].copy()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a SPX/SPXW intraday gamma JSON report")
    parser.add_argument("--output", help="Output JSON path")
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
        }
        path = Path(args.output) if args.output else SCRIPT_DIR / f"spx_intraday_latest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(path)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    finally:
        safe_close(ctx)


if __name__ == "__main__":
    main()
