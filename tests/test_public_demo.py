import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "samples" / "public-demo-v1.json"


class PublicDemoTest(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(SAMPLE.read_text(encoding="utf-8"))

    def test_sample_is_explicitly_dummy(self):
        self.assertEqual("public-demo-v1", self.payload["schemaVersion"])
        self.assertEqual("DUMMY", self.payload["provenance"])
        self.assertIn("실제 관측 또는 예측 결과가 아닙니다", self.payload["notice"])

    def test_sample_has_no_external_identifiers(self):
        serialized = json.dumps(self.payload).lower()
        for forbidden in ("http://", "https://", "api_key", "token", "password", "nx=", "ny="):
            self.assertNotIn(forbidden, serialized)

    def test_metrics_have_public_example_shape(self):
        self.assertGreater(len(self.payload["metrics"]), 0)
        for metric in self.payload["metrics"]:
            self.assertEqual({"name", "value", "unit"}, set(metric))


if __name__ == "__main__":
    unittest.main()
