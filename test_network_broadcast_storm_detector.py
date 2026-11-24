import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import detect

def row(switch, port, pps):
    return {"switch": switch, "port": port, "broadcast_pps": str(pps)}

class TestBroadcastStorm(unittest.TestCase):
    def test_storm(self):
        r, _ = detect([row("SW-01", "Gi0/1", 1200)])
        self.assertEqual(r[0][3], "STORM")

    def test_exactly_storm_level_is_high(self):
        r, _ = detect([row("SW-01", "Gi0/1", 500)])
        self.assertEqual(r[0][3], "HIGH")

    def test_high(self):
        r, _ = detect([row("SW-01", "Gi0/2", 250)])
        self.assertEqual(r[0][3], "HIGH")

    def test_exactly_max_is_ok(self):
        r, _ = detect([row("SW-01", "Gi0/3", 100)])
        self.assertEqual(r[0][3], "OK")

    def test_custom_max(self):
        r, _ = detect([row("SW-01", "Gi0/1", 300)], max_pps=50)
        self.assertEqual(r[0][3], "STORM")

    def test_highest_first(self):
        r, _ = detect([row("SW-01", "Gi0/1", 40), row("SW-02", "Gi0/5", 1200),
                       row("SW-01", "Gi0/2", 250)])
        self.assertEqual([x[1] for x in r], ["Gi0/5", "Gi0/2", "Gi0/1"])

    def test_invalid_row_is_skipped(self):
        r, skipped = detect([row("SW-01", "Gi0/1", "lots"),
                             row("SW-01", "Gi0/2", 40)])
        self.assertEqual((len(r), skipped), (1, 1))

    def test_empty_input(self):
        self.assertEqual(detect([]), ([], 0))
