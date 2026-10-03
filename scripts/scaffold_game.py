#!/usr/bin/env python3
"""Safely scaffold a playable starter only after two explicit approval gates."""
import argparse
from html import escape
import json
from pathlib import Path
import shutil
from validate_spec import ValidationFailure, load_json, validate_game, validate_approval

ROOT = Path(__file__).resolve().parents[1]

def scaffold(spec_path, approval_path, output, *, allow_test_fixture=False):
    game = validate_game(load_json(spec_path))
    validate_approval(load_json(approval_path), game, allow_test_fixture=allow_test_fixture)
    output = Path(output).resolve()
    if output.exists():
        raise ValidationFailure(f"Refusing to overwrite existing path: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "templates/mobile-portrait", output)
    try:
        html = output / "index.html"
        html.write_text(html.read_text().replace("__GAME_TITLE__", escape(game["title"])), encoding="utf-8")
        pkg = output / "package.json"
        obj = json.loads(pkg.read_text())
        obj["name"] = game["id"]
        pkg.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
        (output / "game-spec.json").write_text(json.dumps(game, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (output / "SCAFFOLD-NOTE.md").write_text(
            "# Playable starter, not completed custom game\n\nImplement spec-specific rules and tests before delivery. Do not expose approval records or licensed artwork.\n", encoding="utf-8")
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise
    return output

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--approval", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--allow-test-fixture", action="store_true", help="Only for demos/tests")
    args = parser.parse_args()
    try:
        print("Created:", scaffold(args.spec, args.approval, args.out, allow_test_fixture=args.allow_test_fixture))
    except ValidationFailure as exc:
        parser.exit(1, f"Cannot scaffold: {exc}\n")

if __name__ == "__main__":
    main()
