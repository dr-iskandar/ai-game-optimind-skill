---
name: ai-game-optimind
description: Plan, art-direct, scaffold, build, and verify small 2D mobile-portrait web games from user ideas, references, screenshots, or uploaded assets. Use for creating or revising casual web games, with separate explicit concept and art-direction approvals.
---

# AI Game Studio · Optimind

Use this skill to turn a game idea into a testable mobile-portrait web game. Sprint 1 currently includes specification, approval-gated scaffold and initial tests. Do not claim complete automated illustration, sprite extraction, or screenshot QA until those later modules are implemented.

## Required workflow
1. Discover goals and existing project constraints. Read `references/game-design.md`. Create `game-spec.json` using `schemas/game-spec.schema.json`.
2. **Concept approval:** present genre, loop, win/lose, scoring, timer, reset, quizzes and acceptance criteria; obtain *explicit* user agreement. Record exact evidence, revision, timestamp in `approval.json`.
3. **Art approval:** consult `references/art-direction.md`; show proposed palette, typography, example visual/actual mockup or clearly labeled moodboard. Obtain a *separate explicit* user agreement with revision/timestamp/evidence.
4. Do not forge approval or infer it from silence. Implement autonomously only after both gates. Use `python3 scripts/scaffold_game.py --spec <spec> --approval <approval> --out <new-directory>` for a starter. This starter does not automatically implement arbitrary spec mechanics.
5. Produce only assets you may lawfully use. Record provenance/permission in the asset manifest. Avoid distributing user fonts or copyrighted reference images without consent. Consult `references/asset-production.md` and `references/animation-audio.md`.
6. Make gameplay data/rules the source of truth. A visual-only change must not silently alter mechanics. On a mechanic change, update spec revision and relevant tests; re-approve changed areas.
7. Verify with unit tests and build. Report any checks not actually run; do not call a successful build a real-device test. Consult `references/qa-standards.md`.
8. Do not delete/overwrite user work, incur costs, push, force-push, publish, deploy or change sharing without task-specific authorization. Inspect existing repo and branch first. Read `references/permissions.md`.
9. Deliver implementation status, tests, remaining work, and LAN preview instructions. Adapt explanations to novice users without concealing limitations.

## Default MVP
Vite + vanilla HTML/CSS/JavaScript, portrait-first web game, centered phone-width view on desktop. Prefer CSS motion and SVG for simple components; reserve WebP sprite sheets for frame FX. Use more complex engines only when justified. Concept/art approval is human; the rest may be automated within granted permissions.

## Local checks
```bash
pip install -r requirements.txt
python3 scripts/validate_spec.py --spec examples/sate-match.game-spec.json
python3 -m unittest discover -s tests -v
```
`examples/example-approved.approval.json` is a **mock fixture**; the optional `--allow-test-fixture` flag is only for demos/tests, never real approvals.
