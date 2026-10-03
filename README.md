# AI Game Optimind Skill

A reusable AI Game Studio workflow for **mobile-portrait 2D web games**, designed for Codex and adaptable to ChatGPT Work/Astra workflows.

**Sprint 1 implemented:** skill instructions, concept/art approval gates, JSON spec contracts, an approval-gated Vite/vanilla-JS starter, examples (Sate Match + Memory Match), foundation tests, and CI definitions.

**Important:** a generated starter is not the finished custom game. The skill asks for explicit approval of the *game concept* and *art direction* separately before autonomous implementation. Push, publish, release, destructive edits and spending require distinct permission.

## Repository contents

Sprint 1 source is checked in directly: `SKILL.md`, `references/`, `schemas/`,
`examples/`, `scripts/`, `templates/mobile-portrait/`, `tests/` and GitHub Actions CI.
A ZIP snapshot is also available from the project development conversation if needed.

## Install in Codex

```bash
git clone https://github.com/dr-iskandar/ai-game-optimind-skill.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/ai-game-optimind-skill" ~/.codex/skills/ai-game-optimind
```

Ask Codex: **Use the ai-game-optimind skill to design a mobile portrait game**.

If using the ZIP package rather than cloning this repository, extract it and point your Codex skills path at the extracted `ai-game-optimind-skill` folder. For ChatGPT Work/Astra, reference the same SKILL.md and project spec inside an accessible workspace; GitHub access alone is not an automatic skill installation.

## Test the included full source package

```bash
pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 scripts/validate_spec.py --spec examples/sate-match.game-spec.json
python3 scripts/scaffold_game.py --spec examples/sate-match.game-spec.json --approval examples/example-approved.approval.json --out /tmp/optimind-starter --allow-test-fixture
cd /tmp/optimind-starter
npm install
npm test
npm run build
npm run dev:lan
```

`--allow-test-fixture` is **only for demos**; it is not evidence of a real user's approval. Normal production generation requires genuine approval evidence matching the current spec revision.

Sprint 2: uploaded-asset inspection, atlas/sprite processing, optimization and provenance. Sprint 3: wider gameplay templates and integrated FX/audio. Sprint 4: visual browser QA and multi-game evaluations.

**Licensing:** Public availability is not a reuse license. The project owner has not yet chosen an open-source license; user-uploaded artwork/fonts are excluded.
