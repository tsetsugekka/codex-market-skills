"""Offline checks for the Call/Put profile and its unchanged raw Net GEX."""
import copy
import unittest
from pathlib import Path

from render_spx_gamma_heatmap import build_payload, render_fragment


class GammaProfileTests(unittest.TestCase):
    def setUp(self):
        self.source = {
            "spot_anchor": 5005,
            "per_expiry": {
                "2026-01-02": {
                    "gex_by_strike": [[5000, 2], [5005, -3]],
                    "call_gex_by_strike": [[5000, 5], [5005, 1]],
                    "put_gex_by_strike": [[5000, -3], [5005, -4]],
                    "net_gex": -1,
                    "call_wall": {"level": 5000},
                    "put_wall": {"level": 5005},
                },
                "2026-01-05": {
                    "gex_by_strike": [[5000, -1], [5005, 2]],
                    "call_gex_by_strike": [[5000, 2], [5005, 4]],
                    "put_gex_by_strike": [[5000, -3], [5005, -2]],
                    "net_gex": 1,
                },
            },
        }

    def test_aggregate_sides_preserve_signed_net_and_expiry_values(self):
        original = copy.deepcopy(self.source)
        payload = build_payload(self.source, 5000, 5010)
        self.assertEqual(payload["aggregateCall"], [7, 5, 0])
        self.assertEqual(payload["aggregatePut"], [-6, -6, 0])
        self.assertEqual(payload["aggregate"], [1, -1, 0])
        self.assertEqual(payload["days"][0]["values"], [2, -3, 0])
        self.assertEqual(payload["days"][0]["putWall"], 5005)
        self.assertEqual(self.source, original)

    def test_only_selected_expiries_are_aggregated(self):
        self.source["expiries"] = ["2026-01-05"]
        self.source["buckets"] = {"All": {
            "gex_by_strike": [[5000, 999]], "net_gex": 999,
            "call_gex_by_strike": [[5000, 1000]],
            "put_gex_by_strike": [[5000, -1]],
            "call_wall": {"level": 5000},
        }}
        payload = build_payload(self.source, 5000, 5005)
        self.assertEqual(payload["aggregateCall"], [2, 4])
        self.assertEqual(payload["aggregatePut"], [-3, -2])
        self.assertEqual(payload["aggregate"], [-1, 2])
        self.assertEqual(payload["allNetGex"], 1)
        self.assertIsNone(payload["allCallWall"])

    def test_missing_sides_are_rejected_instead_of_invented_from_net(self):
        for bucket in self.source["per_expiry"].values():
            del bucket["put_gex_by_strike"]
        with self.assertRaisesRegex(ValueError, "side-specific"):
            build_payload(self.source, 5000, 5005)

    def test_one_missing_expiry_side_does_not_make_a_partial_profile(self):
        del self.source["per_expiry"]["2026-01-05"]["put_gex_by_strike"]
        with self.assertRaisesRegex(ValueError, "2026-01-05.*put_gex_by_strike"):
            build_payload(self.source, 5000, 5005)

    def test_explicit_all_bucket_walls_and_fragment(self):
        self.source["buckets"] = {"All": {
            "gex_by_strike": [[5000, 1], [5005, -1]],
            "call_gex_by_strike": [[5000, 7], [5005, 5]],
            "put_gex_by_strike": [[5000, -6], [5005, -6]],
            "call_wall": {"level": 5000}, "put_wall": {"level": 5005},
        }}
        template = (Path(__file__).resolve().parent.parent / "assets/spx-gamma-heatmap-fragment.html").read_text()
        html, payload = render_fragment(self.source, template, 5000, 5005, 5, 2.25)
        self.assertEqual((payload["allCallWall"], payload["allPutWall"]), (5000, 5005))
        self.assertNotIn("__SPX_GAMMA_", html)
        self.assertIn('"aggregatePut":[-6.0,-6.0]', html)


if __name__ == "__main__":
    unittest.main()
