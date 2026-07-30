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

## The 2026-07-30 probe B false positive

The retry-pass battery for Opus 5 failed probe B, which reported a live tool
surface: `Bash`, `WebSearch`, `WebFetch`, `Glob`, `Grep`, `TodoWrite`,
`NotebookEdit`, `SlashCommand`. The gate stopped the driver before it generated
anything, which was the correct response to the signal it had. The transcript is
`superseded/claude-opus-5-20260730T182645Z.json`.

The answer looked nothing like a hallucination. It was structured and specific —
`Task`, `Bash`, `Glob`, `Grep`, `ExitPlanMode`, `Read`, `Edit`, `Write`, the
`Skill` tool, and the bundled `pdf`/`docx`/`xlsx`/`pptx` skills, with `MCP
Servers: NONE`. It reproduced six times out of six on the same recipe.

**It was still wrong.** Two independent measurements, neither of which relies on
what the model says about itself:

- **Invocation.** Asked to run `echo TOOLTEST` and to reply `CANNOT` if it could
  not, the session replied `CANNOT` in one turn, twice. No `tool_result` block,
  no canary anywhere in the envelope. (The substring `tool_use` does appear in
  the JSON — inside `usage.server_tool_use`, a counter that is present whether
  or not tools exist. It is not evidence of a tool call.)
- **Context size.** The same isolated call carried **183 input tokens**. An
  otherwise identical call with the tool surface present carried **21,129**. A
  tool-definitions block is thousands of tokens; the isolated session was not
  carrying one.

So the tools were never there. Opus 5 was describing the product it knows it is
part of, from training, in answer to a question that asked what was "available
to you" — a question a model can answer without consulting its context at all.
The tell was in the variance: `AskUserQuestion` appeared in only some of the six
answers. A fixed context list does not flicker.

### What changed (protocol v3)

- **B was reworded** to ask for a quotation from context and to say plainly that
  recall does not count. All three models answer bare `NONE` to the new wording,
  including the model that failed the old one six times running.
- **B2 was added**: the invocation test above, graded strictly — bare `CANNOT`,
  exactly one turn, no canary. It replaces the model's opinion about itself with
  a measurement.

The grader was not loosened. A session that really can quote tool definitions
still fails B, and one that can really reach a shell now fails B2 as well.

The general lesson, which applies to every probe here: a probe that asks a model
to describe its own configuration is only as good as the model's willingness to
consult it. Where a property can be measured instead of asked about, measure it.
