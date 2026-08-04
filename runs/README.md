# Runs

Every directory here is one scoring run, named
`<UTC timestamp>-<corpus hash prefix>-<registry hash prefix>`. A run is
reproducible from its own `manifest.json`:
`python3 -m telltale report --verify runs/<dir>` recomputes it and requires the
outputs to come back byte-identical.

## The shakedown reference run

**`20260804T210242Z-d827d5a5-369d107e`** is the current reference run for the
shakedown, and everything quoted in `SHAKEDOWN.md` should be read against it.
224 documents, 121 active tells, judge sample of 60 documents, seed 7. It
verifies clean.

It supersedes `20260803T145220Z-d827d5a5-051c8ca2`. That run was correct for the
code that produced it, but two things changed underneath it:

- The judge/code disagreement rate had the wrong denominator (SHAKEDOWN §2.2,
  fixed in M8g.2). The published figure moved from "0 of 292 counted spans" to
  "0 of 2,217 adjudicated spans". Zero either way — the numerator was never in
  doubt — but the scorecard text differs, so `--verify` against the older run
  fails under current code. That is the check working, not breaking.
- The registry gained 12 discovery candidates, so its hash moved from
  `051c8ca2` to `369d107e`. Candidates are not scored, so no number moved on
  account of that; the hash is in the directory name because the registry is
  part of what a run is.

The older run is kept, not deleted. It is the evidence behind the §2 findings as
they were written, and a run that no longer verifies under current code is still
a record of what the code did on the day.

## Other directories

- `calibration/` — judge calibration results, one file per gate run.
- `discovery/` — discovery runs (sweep, lens candidates, verification verdicts).
- `isolation/` — isolation gate records proving no model judged its own output.
