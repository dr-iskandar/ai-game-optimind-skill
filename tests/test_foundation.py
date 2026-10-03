import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_spec import ValidationFailure, load_json, validate_game, validate_approval
from scaffold_game import scaffold

class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.path = ROOT / "examples/sate-match.game-spec.json"
        self.approval = ROOT / "examples/example-approved.approval.json"
        self.game = validate_game(load_json(self.path))

    def test_two_distinct_specs(self):
        self.assertEqual("memory-match", validate_game(load_json(ROOT / "examples/memory-match.game-spec.json"))["id"])

    def test_missing_timer_rejected(self):
        game = json.loads(json.dumps(self.game))
        del game["gameplay"]["timer"]["seconds"]
        with self.assertRaises(ValidationFailure):
            validate_game(game)

    def test_landscape_rejected(self):
        game = json.loads(json.dumps(self.game))
        game["platform"]["orientation"] = "landscape"
        with self.assertRaises(ValidationFailure):
            validate_game(game)

    def test_pending_concept_blocks(self):
        with self.assertRaises(ValidationFailure):
            validate_approval(load_json(ROOT / "examples/pending.approval.json"), self.game)

    def test_fixture_only_when_flagged(self):
        with self.assertRaises(ValidationFailure):
            validate_approval(load_json(self.approval), self.game)
        validate_approval(load_json(self.approval), self.game, allow_test_fixture=True)

    def test_wrong_revision_blocks(self):
        approval = load_json(self.approval)
        approval["concept"]["revision"] = 2
        with self.assertRaises(ValidationFailure):
            validate_approval(approval, self.game, allow_test_fixture=True)

    def test_pending_scaffold_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "starter"
            with self.assertRaises(ValidationFailure):
                scaffold(self.path, ROOT / "examples/pending.approval.json", path)
            self.assertFalse(path.exists())

    def test_scaffold_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "starter"
            scaffold(self.path, self.approval, path, allow_test_fixture=True)
            self.assertTrue((path / "src/logic.js").exists())
            self.assertEqual(json.loads((path / "package.json").read_text())["name"], "sate-match")
            with self.assertRaises(ValidationFailure):
                scaffold(self.path, self.approval, path, allow_test_fixture=True)

if __name__ == "__main__":
    unittest.main()
