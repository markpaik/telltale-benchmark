# Sanitized-device runbook

This repo generates and scores the telltale corpus. Generation is designed to run on a
**sanitized machine** — no user CLAUDE.md, no skills, no MCP servers, no plugins — so the
graded models' writing style cannot be influenced by operator configuration. The isolation
probe battery verifies that empirically before every batch; a clean device makes the
battery's job trivial instead of load-bearing.

## One-time setup

```sh
git clone <this repo> telltale && cd telltale

# Python deps (system python3 ≥ 3.12 is fine)
python3 -m pip install --break-system-packages pyyaml pandas pytest

# Claude Code CLI — install per docs, then log in with the account whose plan funds generation
claude --version        # harness developed against v2.1.220
claude                  # complete /login, then exit

# Sanity: full test suite (no network, no model calls)
python3 -m pytest tests/ -q          # expect all green
python3 -m telltale registry validate
```

Optional: create `local-markers.txt` at repo root (gitignored) with one contamination-marker
string per line for anything machine-specific the scans should also catch. The account email
is read automatically from `~/.claude.json` at scan time — never commit it.

## Prove isolation, then generate

```sh
# Probe battery per graded model — all four probes must PASS. Refuses stale (>24h) batteries.
python3 -m telltale verify-isolation --model claude-opus-5
python3 -m telltale verify-isolation --model claude-fable-5
python3 -m telltale verify-isolation --model claude-sonnet-5

# Full corpus: 3 models × 15 formats × 8 docs = 360 docs (336 evidence + 24 annex),
# ~4–8 min each, resumable.
# Run per-model, under caffeinate (macOS) so sleep can't freeze the run:
caffeinate -i python3 -m telltale generate --models claude-opus-5
caffeinate -i python3 -m telltale generate --models claude-fable-5
caffeinate -i python3 -m telltale generate --models claude-sonnet-5

python3 -m telltale generate status    # completion matrix any time; re-running skips finished docs
```

Notes:
- On auth expiry the run stops cleanly; `/login` again and re-run the same command (skip
  logic resumes). Failed cells leave `.failed.json` markers; re-run to retry.
- Every doc's sidecar records the isolation battery that gated it, the pinned system-prompt
  hash, word counts, continuation boundaries, and model attribution (mismatch = hard fail).
- The canonical corpus includes the `free-writing` annex cell per model — 8 extra docs each,
  generated the same way (`python3 -m telltale generate --models <model> --formats free-writing`),
  scored Tier-1 only and excluded from the index (R20).
- Commit `corpus/` + `runs/isolation/` per model batch and push.

## Scoring (can run on either machine once the corpus is pushed)

```sh
python3 -m telltale score                 # Tier-1 only (~114 tells, offline, deterministic)
python3 -m telltale score --judge         # + the 7 judge tells via claude-opus-4-6 (CLI calls;
                                          #   cached permanently under cache/judge/)
python3 -m telltale judge audit --pct 5   # consistency audit at corpus scale
python3 -m telltale report --verify runs/<run-id>   # byte-identical reproducibility check
```

Outputs land in `runs/<run-id>/`: `scores.jsonl` (per-doc evidence with quotes),
`matrix.csv`, `scorecard.md`, `manifest.json`.

## Condition tracking

Corpora generated on different machines/conditions must not be silently mixed: the sidecar's
`system_prompt_sha256` + isolation transcript identify the condition. The canonical corpus is
the one generated on the sanitized device; anything generated on a dev machine stays local
(untracked) for pipeline testing only.
