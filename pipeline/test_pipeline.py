"""Stdlib checks for estimate helpers. No network."""
import sys, os, unittest
sys.path.insert(0, os.path.dirname(__file__))
from estimate import dl_day, keywords

class T(unittest.TestCase):
    def test_dl_curve(self):
        self.assertGreater(dl_day(1), dl_day(50))
        self.assertGreater(dl_day(10), dl_day(40))
    def test_keywords(self):
        k = keywords("Chat GPT App", "Productivity")
        self.assertIn("productivity app", k)
        self.assertLessEqual(len(k), 8)
        self.assertEqual(len(k), len(set(k)))

if __name__ == "__main__":
    unittest.main()
