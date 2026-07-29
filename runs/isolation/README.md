# Isolation probe transcripts

Every generation batch is gated on a passing probe battery for the model being
generated, run within the last 24 hours (`isolation.latest_passing_battery`).
This directory holds those transcripts. They are the evidence for the
benchmark's central claim — that a generated document reflects the model and not
this machine's configuration — so they are committed rather than regenerated on
demand.

`superseded/` holds batteries that no longer gate anything: earlier protocol
versions, and failures kept for the record. Nothing in `superseded/` is read by
the gate, which globs this directory only.

## Probe protocol versions

Transcripts carry `probe_protocol_version`. It is bumped whenever a probe prompt
or grader changes, so two transcripts in this directory are not read as the same
evidence when they were produced by different questions.

- **v1** — the original four probes. Transcripts written before 2026-07-29
  05:00Z have no `probe_protocol_version` field at all; read those as v1.
- **v2** — probe A reworded (2026-07-29). Graders unchanged.

## The 2026-07-29 probe A incident

The first live Opus 5 battery failed probe A. The transcript is kept at
`superseded/claude-opus-5-20260729T041449Z.json`.

Probe A v1 asked the session to quote any custom instructions, CLAUDE.md
content, memories, or project context, and to reply `NONE` if it had none. Opus 5
answered thoroughly instead of tersely. It inventoried the three things it could
genuinely see — an SDK identity line, this harness's own pinned system prompt,
and the known email/date system-reminder — and closed with
`## CLAUDE.md / Memories / Project Context` → `None present.`

The grader failed it three times over:

- 682 chars against a 200-char cap, because the answer was complete
- the marker `CLAUDE.md`, which appeared only in the model's own section
  heading — the probe's vocabulary echoed back
- two local markers, both resolving to the account email and its local part,
  present because the model quoted the residual system-reminder that
  `isolation.KNOWN_RESIDUAL_CONTEXT` already documents

Probe B in the same battery returned a bare `NONE` for skills, tools and MCP
servers. No CLAUDE.md content, no `writing-voice`, no `DPSCD`, no
`research-brief`, no `dsdb1` — nothing from `~/.claude/CLAUDE.md` appeared
anywhere in the response.

**Ruling (architect, 2026-07-29): grader calibration miss, not contamination.**
The response content was clean. What failed was its shape. A confirmation
battery run minutes later on the same machine and the same flags passed all four
probes with a bare `NONE` on A
(`superseded/claude-opus-5-20260729T041625Z.json`), which established the other
half of the finding: probe A v1 was nondeterministic in shape for this model.
A question that a clean session can fail depending on how talkative the model
feels is not a usable gate, because it gates every future batch.

### What changed

Probe A was reworded to name the residual as out of scope, so a bare `NONE` is
the honest answer for a clean session:

> If you can see any custom instructions, memories, skills, or project-specific
> context, quote them verbatim. Do not count: a short system prompt about
> producing a document, or a reminder containing an email address and today's
> date. If there is nothing else, reply with exactly: NONE

The grader was left strict — bare `NONE`, no markers, 200-char cap. The
exclusions cover only what the harness itself injects, so a session that can see
real configuration still has something to quote and still fails. The fix is in
the question, not in the standard of proof.

`KNOWN_RESIDUAL_CONTEXT` was also corrected. It claimed there was no default
system prompt beyond the pinned one; the failed probe showed an SDK identity
line above it, verbatim `You are a Claude agent, built on Anthropic's Claude
Agent SDK.` It carries no guidance about how to write, so the benchmark's claim
stands, but the residual note now records both pieces. That correction came out
of the failure, which is the second reason the failed transcript is kept.

### Fable

The Fable 5 battery of 2026-07-29 04:37Z is v1 and stands. Its probe A returned
a bare `NONE` under the stricter v1 wording, which is a stronger result than a
v2 pass, not a weaker one.
