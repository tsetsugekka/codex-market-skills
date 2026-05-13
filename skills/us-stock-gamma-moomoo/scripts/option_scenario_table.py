#!/usr/bin/env python3
"""Build a short-dated option value scenario table.

This is intentionally data-provider agnostic. Fetch live option IV/bid/ask/spot
with moomoo first, then pass the current IV, strike, expiry, and spot grid here.
"""

from __future__ import annotations

import argparse
import math
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(spot: float, strike: float, years: float, rate: float, vol: float, kind: str) -> float:
    intrinsic = max(spot - strike, 0.0) if kind == "C" else max(strike - spot, 0.0)
    if years <= 0 or vol <= 0:
        return intrinsic
    sqrt_t = math.sqrt(years)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * years) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    if kind == "C":
        return spot * norm_cdf(d1) - strike * math.exp(-rate * years) * norm_cdf(d2)
    return strike * math.exp(-rate * years) * norm_cdf(-d2) - spot * norm_cdf(-d1)


def parse_dt(value: str, tz: ZoneInfo) -> datetime:
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def parse_spots(args: argparse.Namespace) -> list[float]:
    if args.spots:
        return [float(part.strip()) for part in args.spots.split(",") if part.strip()]
    if args.spot_min is None or args.spot_max is None:
        raise SystemExit("Pass either --spots or both --spot-min and --spot-max.")
    step = args.spot_step
    n = int(round((args.spot_max - args.spot_min) / step))
    return [round(args.spot_min + i * step, 4) for i in range(n + 1)]


def build_times(asof: datetime, expiry: datetime, interval_min: int) -> list[datetime]:
    times: list[datetime] = []
    t = asof
    while t < expiry:
        times.append(t)
        t += timedelta(minutes=interval_min)
    if not times or times[-1] != expiry:
        times.append(expiry)
    return times


def fmt_price(value: float) -> str:
    if value >= 10:
        return f"{value:.1f}"
    if value >= 1:
        return f"{value:.2f}"
    return f"{value:.3f}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a markdown scenario table for a short-dated option.")
    parser.add_argument("--kind", choices=["C", "P"], required=True, help="Option type: C or P.")
    parser.add_argument("--strike", type=float, required=True)
    parser.add_argument("--iv", type=float, required=True, help="Annualized IV. Accepts 0.16 or 16 for 16%.")
    parser.add_argument("--expiry", required=True, help="ISO datetime. Naive values are interpreted in --timezone.")
    parser.add_argument("--asof", help="ISO datetime. Defaults to now in --timezone.")
    parser.add_argument("--timezone", default="Asia/Tokyo")
    parser.add_argument("--interval-min", type=int, default=30)
    parser.add_argument("--rate", type=float, default=0.04, help="Annual risk-free rate. Accepts 0.04 or 4 for 4%.")
    parser.add_argument("--spots", help="Comma-separated underlying prices.")
    parser.add_argument("--spot-min", type=float)
    parser.add_argument("--spot-max", type=float)
    parser.add_argument("--spot-step", type=float, default=10.0)
    args = parser.parse_args()

    tz = ZoneInfo(args.timezone)
    asof = parse_dt(args.asof, tz) if args.asof else datetime.now(tz)
    expiry = parse_dt(args.expiry, tz)
    if expiry < asof:
        raise SystemExit("Expiry is before as-of time.")

    vol = args.iv / 100.0 if args.iv > 3 else args.iv
    rate = args.rate / 100.0 if args.rate > 1 else args.rate
    spots = parse_spots(args)
    times = build_times(asof, expiry, args.interval_min)

    headers = ["Spot"] + [t.strftime("%H:%M") for t in times]
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(["---"] * len(headers)) + " |")
    for spot in spots:
        row = [f"{spot:g}"]
        for t in times:
            years = max((expiry - t).total_seconds(), 0.0) / (365.0 * 24.0 * 60.0 * 60.0)
            row.append(fmt_price(bs_price(spot, args.strike, years, rate, vol, args.kind)))
        print("| " + " | ".join(row) + " |")

    print()
    print(f"Assumptions: {args.kind} strike {args.strike:g}, IV {vol:.2%}, rate {rate:.2%}, timezone {args.timezone}.")
    print("Real fills can differ because IV, spread, and liquidity change intraday.")


if __name__ == "__main__":
    main()
