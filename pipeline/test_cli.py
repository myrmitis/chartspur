"""Offline CLI checks using synthetic persisted inputs and disposable outputs."""

import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest


PIPELINE = Path(__file__).resolve().parent


def write_summary_inputs(work):
    (work / "brief.json").write_text(json.dumps({
        "latest_ts": 2_000_000, "sample_genre": "Games",
        "brief": {"apps": 40}, "checkout_open": False, "price_usd": 19,
    }))
    (work / "ledger.json").write_text("{}\n")


class PipelineCLITest(unittest.TestCase):
    def test_estimate_exports_screenshots_and_snapshot_velocity(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            # The CLI uses paths beside its source. Give it a disposable workspace.
            shutil.copytree(
                PIPELINE, work / "pipeline",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (work / "data").mkdir()
            with sqlite3.connect(work / "data" / "appintel.db") as db:
                db.executescript("""
                    CREATE TABLE apps(trackId INTEGER PRIMARY KEY, name TEXT,
                        seller TEXT, genre TEXT, price REAL DEFAULT 0, artwork TEXT,
                        screenshots TEXT, description TEXT);
                    CREATE TABLE snapshots(trackId INTEGER, ts INTEGER, rank INTEGER,
                        chart TEXT, rating REAL, rating_count INTEGER, price REAL,
                        PRIMARY KEY(trackId, ts, chart));
                """)
                for tid in range(1, 41):
                    shots = (json.dumps(["https://example.invalid/first.png"])
                             if tid == 1 else "not-json" if tid == 2 else None)
                    db.execute("INSERT INTO apps VALUES (?,?,?,?,?,?,?,?)", (
                        tid, f"Synthetic App {tid}", "Synthetic Seller", "Games",
                        0, "", shots, "Synthetic description"))
                    db.execute("INSERT INTO snapshots VALUES (?,?,?,?,?,?,?)", (
                        tid, 2_000_000, tid, "topfreeapplications", 4.5,
                        110 if tid == 1 else 42, 0))
                db.execute("INSERT INTO snapshots VALUES (?,?,?,?,?,?,?)", (
                    1, 2_000_000 - 2 * 86400, 2, "topfreeapplications", 4.5, 100, 0))
            result = subprocess.run(
                [sys.executable, "pipeline/estimate.py"], cwd=work,
                capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rows = json.loads((work / "data" / "live.json").read_text())
            self.assertEqual(len(rows), 40)
            self.assertEqual({row["updated_ts"] for row in rows}, {2_000_000})
            by_id = {row["trackId"]: row for row in rows}
            self.assertEqual(by_id[1]["screenshots"], ["https://example.invalid/first.png"])
            self.assertEqual(by_id[2]["screenshots"], [])
            self.assertEqual(by_id[3]["screenshots"], [])
            self.assertIsNone(by_id[2]["rc_velocity"])
            self.assertEqual(by_id[1]["rc_velocity"], 5.0)

    def test_summary_writes_relative_output(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            write_summary_inputs(work)
            result = subprocess.run(
                [sys.executable, str(PIPELINE / "summary.py"),
                 "--brief", "brief.json", "--ledger", "ledger.json",
                 "--out", "summary.json"], cwd=work,
                capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            document = json.loads((work / "summary.json").read_text())
            self.assertEqual(document["snapshot_ts"], 2_000_000)
            self.assertEqual(document["sample_genre"], "Games")
            self.assertEqual(document["sample_app_count"], 40)
            self.assertFalse(document["checkout_open"])
            self.assertEqual(document["cash_collected_usd"], 0)


    def test_summary_decision_honors_epoch_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            write_summary_inputs(work)
            for now in (1, 0):
                result = subprocess.run(
                    [sys.executable, str(PIPELINE / "summary.py"),
                     "--brief", "brief.json", "--ledger", "ledger.json",
                     "--decide", "--event", "workflow_dispatch", "--now", str(now)],
                    cwd=work, capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                document = json.loads(result.stdout)
                self.assertIn("## Chartspur operating summary 1970-01-01", document["body"])
                self.assertIn("<!-- appsignal-summary:1970-01-01 -->", document["body"])


if __name__ == "__main__":
    unittest.main()
