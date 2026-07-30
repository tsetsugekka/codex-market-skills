#!/usr/bin/env python3
"""Render a theme-aware SPX gamma heatmap HTML fragment from OpenD JSON."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


STRIKE_STEP = 5.0
MAGNET_WINDOW = 250.0
MAGNET_DECAY = 100.0


def finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def strike_map(bucket: dict[str, Any]) -> dict[float, float]:
    result: dict[float, float] = {}
    for item in bucket.get("gex_by_strike", []):
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        strike = finite_number(item[0])
        value = finite_number(item[1])
        if strike is None or value is None:
            continue
        result[round(strike, 6)] = result.get(round(strike, 6), 0.0) + value
    return result


def choose_flip(items: Any, spot: float) -> float | None:
    levels: list[float] = []
    if isinstance(items, list):
        for item in items:
            candidate = item[0] if isinstance(item, (list, tuple)) and item else item
            level = finite_number(candidate)
            if level is not None:
                levels.append(level)
    return min(levels, key=lambda level: abs(level - spot)) if levels else None


def normalize_wall(raw: Any) -> float | None:
    if isinstance(raw, dict):
        return finite_number(raw.get("level"))
    if isinstance(raw, (list, tuple)) and raw:
        return finite_number(raw[0])
    scalar = finite_number(raw)
    if scalar is not None:
        return scalar
    return None


def fallback_rough_magnet(
    mapping: dict[float, float], spot: float
) -> dict[str, Any] | None:
    nearby = [
        (strike, value)
        for strike, value in mapping.items()
        if abs(strike - spot) <= MAGNET_WINDOW
    ]
    positive = [(strike, value) for strike, value in nearby if value > 0]
    if not positive:
        return None

    weighted = [
        (
            strike,
            value,
            value * math.exp(-abs(strike - spot) / MAGNET_DECAY),
        )
        for strike, value in positive
    ]
    total_weight = sum(item[2] for item in weighted)
    if total_weight <= 0:
        return None

    raw_level = sum(strike * weight for strike, _, weight in weighted) / total_weight
    level = round(raw_level / STRIKE_STEP) * STRIKE_STEP
    concentration = (
        sum(
            weight
            for strike, _, weight in weighted
            if abs(strike - level) <= 25.0
        )
        / total_weight
    )
    gross = sum(abs(value) for _, value in nearby)
    positive_share = sum(value for _, value in positive) / gross if gross else 0.0
    score = 0.65 * concentration + 0.35 * positive_share
    confidence = "high" if score >= 0.65 else "medium" if score >= 0.42 else "low"
    return {
        "level": float(level),
        "distance_from_spot": float(level - spot),
        "confidence": confidence,
        "score": float(score),
        "method": "positive-GEX distance-decay centroid",
        "window_points": MAGNET_WINDOW,
        "decay_points": MAGNET_DECAY,
        "source": "renderer-fallback",
    }


def normalize_rough_magnet(
    raw: Any, mapping: dict[float, float], spot: float
) -> dict[str, Any] | None:
    if isinstance(raw, dict):
        level = finite_number(raw.get("level"))
        if level is not None:
            return {
                "level": level,
                "distance_from_spot": finite_number(raw.get("distance_from_spot")),
                "confidence": str(raw.get("confidence") or "unknown"),
                "score": finite_number(raw.get("score")),
                "method": str(
                    raw.get("method") or "positive-GEX distance-decay centroid"
                ),
                "window_points": finite_number(raw.get("window_points")),
                "decay_points": finite_number(raw.get("decay_points")),
                "source": "json",
            }
    scalar = finite_number(raw)
    if scalar is not None:
        return {
            "level": scalar,
            "distance_from_spot": scalar - spot,
            "confidence": "unknown",
            "score": None,
            "method": "JSON rough magnet",
            "window_points": None,
            "decay_points": None,
            "source": "json",
        }
    return fallback_rough_magnet(mapping, spot)


def strike_grid(min_strike: float, max_strike: float) -> list[float]:
    count = int(round((max_strike - min_strike) / STRIKE_STEP))
    return [min_strike + index * STRIKE_STEP for index in range(count + 1)]


def normalize_expiries(source: dict[str, Any]) -> list[str]:
    per_expiry = source.get("per_expiry")
    if not isinstance(per_expiry, dict) or not per_expiry:
        raise ValueError("JSON must contain a non-empty per_expiry object")

    requested = source.get("expiries")
    candidates = requested if isinstance(requested, list) else list(per_expiry)
    expiries: list[str] = []
    seen: set[str] = set()
    for value in candidates:
        expiry = str(value)
        if expiry in per_expiry and expiry not in seen:
            expiries.append(expiry)
            seen.add(expiry)
    if not expiries:
        raise ValueError("JSON expiries do not match per_expiry keys")
    return expiries


def build_payload(
    source: dict[str, Any], min_strike: float, max_strike: float
) -> dict[str, Any]:
    spot = finite_number(source.get("spot_anchor"))
    if spot is None or spot <= 0:
        raise ValueError("JSON must contain a positive spot_anchor")

    grid = strike_grid(min_strike, max_strike)
    expiries = normalize_expiries(source)
    per_expiry_source = source["per_expiry"]
    days: list[dict[str, Any]] = []

    for expiry in expiries:
        bucket = per_expiry_source[expiry]
        if not isinstance(bucket, dict):
            raise ValueError(f"per_expiry[{expiry!r}] must be an object")
        mapping = strike_map(bucket)
        if not mapping:
            raise ValueError(f"per_expiry[{expiry!r}] has no usable gex_by_strike")
        magnet = normalize_rough_magnet(bucket.get("rough_magnet"), mapping, spot)
        days.append(
            {
                "expiry": expiry,
                "netGex": finite_number(bucket.get("net_gex")) or 0.0,
                "flip": choose_flip(bucket.get("flips"), spot),
                "magnet": magnet,
                "callWall": normalize_wall(bucket.get("call_wall")),
                "putWall": normalize_wall(bucket.get("put_wall")),
                "values": [mapping.get(round(strike, 6), 0.0) for strike in grid],
            }
        )

    buckets = source.get("buckets")
    all_bucket = buckets.get("All", {}) if isinstance(buckets, dict) else {}
    all_mapping = strike_map(all_bucket) if isinstance(all_bucket, dict) else {}
    if all_mapping:
        aggregate = [all_mapping.get(round(strike, 6), 0.0) for strike in grid]
    else:
        aggregate = [
            sum(day["values"][index] for day in days) for index in range(len(grid))
        ]

    all_net_gex = (
        finite_number(all_bucket.get("net_gex"))
        if isinstance(all_bucket, dict)
        else None
    )
    if all_net_gex is None:
        all_net_gex = sum(day["netGex"] for day in days)

    all_flip = (
        choose_flip(all_bucket.get("flips"), spot)
        if isinstance(all_bucket, dict)
        else None
    )

    return {
        "generated": str(source.get("generated") or ""),
        "spot": spot,
        "minStrike": min_strike,
        "maxStrike": max_strike,
        "strikeStep": STRIKE_STEP,
        "allNetGex": all_net_gex,
        "allFlip": all_flip,
        "aggregate": aggregate,
        "days": days,
    }


def validate_args(args: argparse.Namespace) -> None:
    if args.max_strike <= args.min_strike:
        raise ValueError("--max-strike must be greater than --min-strike")
    for name, value in (
        ("--min-strike", args.min_strike),
        ("--max-strike", args.max_strike),
    ):
        if abs(value / STRIKE_STEP - round(value / STRIKE_STEP)) > 1e-8:
            raise ValueError(f"{name} must align to the native 5-point grid")
    if args.smooth_radius < 0:
        raise ValueError("--smooth-radius must be zero or greater")
    if args.smooth_sigma <= 0:
        raise ValueError("--smooth-sigma must be positive")


def render_fragment(
    source: dict[str, Any],
    template: str,
    min_strike: float,
    max_strike: float,
    smooth_radius: int,
    smooth_sigma: float,
) -> tuple[str, dict[str, Any]]:
    payload = build_payload(source, min_strike, max_strike)
    required = {
        "__SPX_GAMMA_PAYLOAD__": json.dumps(
            payload, ensure_ascii=False, separators=(",", ":")
        ).replace("</", "<\\/"),
        "__SMOOTH_RADIUS__": str(smooth_radius),
        "__SMOOTH_SIGMA__": repr(float(smooth_sigma)),
    }
    fragment = template
    for marker, replacement in required.items():
        if fragment.count(marker) != 1:
            raise ValueError(f"Template must contain exactly one {marker} marker")
        fragment = fragment.replace(marker, replacement)

    lowered = fragment.lower()
    for forbidden in ("<html", "<head", "<body"):
        if forbidden in lowered:
            raise ValueError(f"Generated output must be a fragment; found {forbidden}")
    return fragment, payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render an inline SPX daily-expiry gamma heatmap from "
            "spx_intraday_latest.py JSON."
        )
    )
    parser.add_argument("json_input", type=Path)
    parser.add_argument("html_output", type=Path)
    parser.add_argument("--min-strike", type=float, default=7000.0)
    parser.add_argument("--max-strike", type=float, default=7700.0)
    parser.add_argument("--smooth-radius", type=int, default=5)
    parser.add_argument("--smooth-sigma", type=float, default=2.25)
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parent.parent
        / "assets"
        / "spx-gamma-heatmap-fragment.html",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_args(args)
    source = json.loads(args.json_input.read_text(encoding="utf-8"))
    if not isinstance(source, dict):
        raise ValueError("Input JSON root must be an object")
    template = args.template.read_text(encoding="utf-8")
    fragment, payload = render_fragment(
        source,
        template,
        args.min_strike,
        args.max_strike,
        args.smooth_radius,
        args.smooth_sigma,
    )
    args.html_output.parent.mkdir(parents=True, exist_ok=True)
    args.html_output.write_text(fragment, encoding="utf-8")

    sources = [
        day["magnet"]["source"] if day["magnet"] else "unavailable"
        for day in payload["days"]
    ]
    print(
        "Rendered "
        f"{len(payload['days'])} real expiries, "
        f"{len(payload['aggregate'])} strikes "
        f"({payload['minStrike']:g}-{payload['maxStrike']:g} by 5)."
    )
    print(
        "Daily rough magnets: "
        f"JSON={sources.count('json')}, "
        f"fallback={sources.count('renderer-fallback')}, "
        f"unavailable={sources.count('unavailable')}."
    )
    print(f"HTML fragment: {args.html_output}")


if __name__ == "__main__":
    main()
