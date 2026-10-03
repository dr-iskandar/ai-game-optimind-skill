#!/usr/bin/env python3
"""Validate game specifications and enforce matching, explicit approvals."""
import argparse
import json
from pathlib import Path
import sys
try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit("Install requirements: pip install -r requirements.txt") from exc

ROOT = Path(__file__).resolve().parents[1]

class ValidationFailure(ValueError):
    pass

def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationFailure(f"Cannot read {path}: {exc}") from exc

def verify_schema(data, filename):
    schema = load_json(ROOT / "schemas" / filename)
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data),
                    key=lambda e: (list(map(str, e.absolute_path)), e.message))
    if errors:
        raise ValidationFailure("\n".join(
            f"{'.'.join(map(str, e.absolute_path)) or 'root'}: {e.message}" for e in errors[:12]))

def validate_game(game):
    verify_schema(game, "game-spec.schema.json")
    timer = game["gameplay"]["timer"]
    if timer["enabled"] and "seconds" not in timer:
        raise ValidationFailure("gameplay.timer.seconds required when timer is enabled")
    return game

def validate_approval(approval, game, *, allow_test_fixture=False):
    verify_schema(approval, "approval.schema.json")
    if approval["gameId"] != game["id"]:
        raise ValidationFailure("approval gameId does not match game spec id")
    for gate in ("concept", "artDirection"):
        item = approval[gate]
        if item["status"] != "approved":
            raise ValidationFailure(f"{gate}: explicit approval required")
        if item["revision"] != game["revision"]:
            raise ValidationFailure(f"{gate}: approval revision does not match current spec")
        if not item["approvedAt"] or not item["evidence"] or not item["evidence"].strip():
            raise ValidationFailure(f"{gate}: real approval date and evidence required")
        if "TEST FIXTURE" in item["evidence"].upper() and not allow_test_fixture:
            raise ValidationFailure(f"{gate}: mock fixture cannot count as real approval")
    return approval

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--approval", type=Path)
    parser.add_argument("--require-approved", action="store_true")
    parser.add_argument("--allow-test-fixture", action="store_true", help="Demo and tests only")
    args = parser.parse_args(argv)
    try:
        game = validate_game(load_json(args.spec))
        if args.require_approved:
            if not args.approval:
                raise ValidationFailure("--approval required with --require-approved")
            validate_approval(load_json(args.approval), game, allow_test_fixture=args.allow_test_fixture)
        elif args.approval:
            verify_schema(load_json(args.approval), "approval.schema.json")
    except ValidationFailure as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(f"VALID: {game['id']} revision {game['revision']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
