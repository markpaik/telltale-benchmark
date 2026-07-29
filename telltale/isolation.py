"""Run `claude -p` with the user's machine held at arm's length.

The benchmark measures how a model writes when nobody has told it how to write.
That claim only survives if the generating subprocess never sees this machine's
configuration: the user's global ~/.claude/CLAUDE.md instructs every session to
apply a house voice skill that strips exactly the tells we are trying to count,
and Claude Code's own default system prompt carries style guidance of its own.
Either one reaching a generation call would make the benchmark measure the
config instead of the model.

So the recipe here is not a convenience wrapper. It is the instrument, and it
was arrived at empirically rather than by reading flag docs — see the probe
battery below, which re-derives the claim live before every generation batch.

What was tried, on Claude Code 2.1.220 / macOS:

  1. `CLAUDE_CONFIG_DIR=<fresh empty dir>` — the strongest isolation on paper,
     since a config dir with nothing in it has no CLAUDE.md, no settings, no
     skills and no plugins to find. It fails closed: the CLI reports
     "Not logged in - Please run /login". OAuth credentials live in the macOS
     Keychain, but the CLI only reaches for them when running against the
     default config dir; a relocated dir wants its own credentials on disk.
  2. Seeding the fresh dir with the account pointer out of ~/.claude.json
     (userID, hasCompletedOnboarding, oauthAccount) — still "Not logged in".
     Making it work would mean copying a live OAuth token out of the Keychain
     into a scratch file, which trades a config-leak risk for a credential-leak
     risk. Rejected.
  3. `--bare`, which reads well ("skip hooks, auto-memory, CLAUDE.md
     auto-discovery") but states plainly that Anthropic auth is then strictly
     ANTHROPIC_API_KEY or apiKeyHelper, with OAuth and keychain never read.
     Confirmed live: "Not logged in". Unusable without an API key, and the
     benchmark is specified to run on the machine's existing Claude Code auth.
  4. Default config dir, isolation by flag: `--safe-mode` (documented to
     disable CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands
     and agents, and output styles, while leaving auth alone) plus
     `--system-prompt` to replace the default prompt outright, `--tools ""` to
     remove the tool surface, `--setting-sources ""` and `--strict-mcp-config`
     to refuse settings and MCP config, and `--disable-slash-commands`.
     This passes all four probes.

The transcripts are the evidence and they are committed: runs/isolation/ holds
the batteries that gate generation, and runs/isolation/superseded/ keeps the
earlier ones — including a Sonnet battery that failed probe D — so the reasoning
behind the current probe wording can be checked rather than taken on trust.

One residual is known and deliberately not papered over. Asked to reproduce
every injected block verbatim, the isolated session returns exactly one
system-reminder carrying the account email and today's date, and nothing else —
no CLAUDE.md, no skills, no tool list, no default Claude Code prompt. It has no
bearing on how the model writes, but it is per-machine, so it is recorded in
every probe transcript rather than left for a later reader to rediscover.

`ISOLATION_ENV` therefore carries no CLAUDE_CONFIG_DIR. What it does do is
strip the CLAUDE_* variables the parent session exports (CLAUDE_CODE_SESSION_ID,
CLAUDE_EFFORT, CLAUDECODE and friends), so a generation launched from inside a
Claude Code session is not quietly handed that session's identity or settings.

The one thing the recipe deliberately does not disable is session persistence:
generation needs `--resume` to continue a document that stopped short.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from telltale import textstats

# --- the pinned system prompt ------------------------------------------------

MINIMAL_SYSTEM_PROMPT = (
    "Respond with only the requested document, formatted in markdown. "
    "Do not add preamble, commentary, or notes about the document."
)

SYSTEM_PROMPT_SHA256 = hashlib.sha256(MINIMAL_SYSTEM_PROMPT.encode("utf-8")).hexdigest()


# --- the recipe --------------------------------------------------------------

#: Environment overlay applied on top of a CLAUDE_*-stripped copy of os.environ.
ISOLATION_ENV: dict[str, str] = {
    # --safe-mode sets this itself; setting it explicitly means a transport that
    # ever loses the flag still lands in the same place.
    "CLAUDE_CODE_SAFE_MODE": "1",
}

#: Variables whose names start with any of these are removed from the child env.
#: The parent Claude Code session exports several (CLAUDE_CODE_SESSION_ID,
#: CLAUDE_CODE_ENTRYPOINT, CLAUDE_EFFORT, ...); none should reach generation.
#: ANTHROPIC_* is left alone because it can carry the auth an operator relies on.
ENV_STRIP_PREFIXES: tuple[str, ...] = ("CLAUDE_", "CLAUDECODE")

#: Empirically validated. Everything after these is per-call (--model, --resume).
ISOLATION_FLAGS: list[str] = [
    "-p",
    "--safe-mode",
    "--system-prompt",
    MINIMAL_SYSTEM_PROMPT,
    "--setting-sources",
    "",
    "--tools",
    "",
    "--strict-mcp-config",
    "--disable-slash-commands",
    "--output-format",
    "json",
]

CLAUDE_BIN = "claude"

PROBE_TIMEOUT_S = 300
GENERATION_TIMEOUT_S = 1800


def isolation_env() -> dict[str, str]:
    """os.environ minus the parent session's CLAUDE_* leakage, plus ISOLATION_ENV."""
    env = {
        k: v
        for k, v in os.environ.items()
        if not any(k.startswith(prefix) for prefix in ENV_STRIP_PREFIXES)
    }
    env.update(ISOLATION_ENV)
    return env


def build_cmd(model: str, extra: list[str] | None = None) -> list[str]:
    """The full argv for one isolated call. `extra` appends per-call flags."""
    return [CLAUDE_BIN, *ISOLATION_FLAGS, "--model", model, *(extra or [])]


# --- transport ---------------------------------------------------------------


@dataclass(frozen=True)
class CliResult:
    """Raw outcome of one subprocess call, before any JSON parsing."""

    returncode: int
    stdout: str
    stderr: str
    duration_s: float
    timed_out: bool = False


#: A transport takes (argv, prompt-on-stdin, timeout) and returns a CliResult.
#: Tests inject a fake one; nothing else in the package shells out.
Transport = Callable[[list[str], str, int], CliResult]


def run_cli(cmd: list[str], prompt: str, timeout: int = PROBE_TIMEOUT_S) -> CliResult:
    """Real transport: run the CLI in a scratch cwd with the prompt on stdin."""
    started = time.monotonic()
    cwd = scratch_cwd()
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd),
            env=isolation_env(),
        )
    except subprocess.TimeoutExpired as exc:
        return CliResult(
            returncode=124,
            stdout=exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
            stderr=f"timed out after {timeout}s",
            duration_s=time.monotonic() - started,
            timed_out=True,
        )
    return CliResult(
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        duration_s=time.monotonic() - started,
    )


def scratch_cwd() -> Path:
    """An empty, non-git working directory to run generation from.

    cwd matters: Claude Code discovers project CLAUDE.md, .claude/ settings and
    git context by walking up from where it is launched. Launching from the
    benchmark repo would hand every generation this project's own context.
    """
    path = Path(os.environ.get("TMPDIR", "/tmp")) / "telltale-isolation-cwd"
    path.mkdir(parents=True, exist_ok=True)
    return path


def cli_version() -> str:
    """`claude --version`, trimmed. Empty string if the CLI cannot be run."""
    try:
        proc = subprocess.run(
            [CLAUDE_BIN, "--version"],
            capture_output=True,
            text=True,
            timeout=60,
            env=isolation_env(),
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return proc.stdout.strip()


# --- envelope parsing --------------------------------------------------------


@dataclass(frozen=True)
class Envelope:
    """The `--output-format json` result envelope, normalized."""

    result: str
    session_id: str
    num_turns: int
    is_error: bool
    usage: dict[str, Any] = field(default_factory=dict)
    model_reported: str = ""
    model_usage: dict[str, Any] = field(default_factory=dict)
    #: True when the model that was asked for is not in modelUsage at all.
    model_mismatch: bool = False
    raw: dict[str, Any] = field(default_factory=dict)
    parse_error: str = ""

    @property
    def ok(self) -> bool:
        return not self.is_error and not self.parse_error


def _output_tokens(entry: Any) -> int:
    """Output-token count out of one modelUsage entry, whatever it is keyed by."""
    if not isinstance(entry, dict):
        return 0
    for key in ("outputTokens", "output_tokens"):
        value = entry.get(key)
        if isinstance(value, (int, float)):
            return int(value)
    return 0


def _attribute_model(
    model_usage: dict[str, Any], requested_model: str
) -> tuple[str, bool]:
    """Decide which model actually produced this response.

    modelUsage is keyed by model id and routinely holds more than one entry: the
    harness makes its own small side-calls, so a claude-sonnet-5 run comes back
    with both claude-sonnet-5 and claude-haiku-4-5-20251001. Picking the entry
    with the most output tokens looked right on a long document and was wrong on
    a short one — a bare "NONE" probe answer is fewer tokens than the side-call,
    so all four of the first committed probe transcripts named haiku.

    Volume is the wrong signal. Identity is the right one: match the model that
    was asked for. Keys may carry a date suffix (claude-sonnet-5-20260101), so
    the match is by containment either way. When the requested model is missing
    from modelUsage altogether the response came from something we did not ask
    for, which is a fact about the evidence rather than a detail — hence the
    mismatch flag, which the generator treats as fatal.
    """
    if not requested_model:
        # No claim to check against (probe replays, ad-hoc parsing).
        if not model_usage:
            return "", False
        return max(sorted(model_usage), key=lambda n: _output_tokens(model_usage[n])), False

    matches = [
        name
        for name in sorted(model_usage)
        if requested_model in name or name in requested_model
    ]
    if matches:
        return max(matches, key=lambda n: _output_tokens(model_usage[n])), False

    if not model_usage:
        return "", True
    return max(sorted(model_usage), key=lambda n: _output_tokens(model_usage[n])), True


def parse_envelope(stdout: str, requested_model: str = "") -> Envelope:
    """Parse the JSON envelope. Malformed output becomes an error envelope.

    Pass `requested_model` wherever a claim about which model wrote the text is
    going to be recorded; without it attribution is best-effort and never sets
    the mismatch flag.
    """
    text = (stdout or "").strip()
    if not text:
        return Envelope("", "", 0, True, parse_error="empty stdout")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return Envelope("", "", 0, True, parse_error=f"not JSON: {exc}")
    if not isinstance(data, dict):
        return Envelope("", "", 0, True, parse_error="envelope is not an object")

    result = data.get("result")
    if not isinstance(result, str):
        result = "" if result is None else str(result)

    usage = data.get("usage")
    usage = usage if isinstance(usage, dict) else {}

    raw_model_usage = data.get("modelUsage")
    model_usage = raw_model_usage if isinstance(raw_model_usage, dict) else {}
    model_reported, model_mismatch = _attribute_model(model_usage, requested_model)

    return Envelope(
        result=result,
        session_id=str(data.get("session_id") or ""),
        num_turns=int(data.get("num_turns") or 0),
        is_error=bool(data.get("is_error")),
        usage=usage,
        model_reported=model_reported,
        model_usage=dict(model_usage),
        model_mismatch=model_mismatch,
        raw=data,
    )


# --- probe graders -----------------------------------------------------------

#: Anything from this machine's configuration. A generation that can name one of
#: these has been contaminated.
CONTAMINATION_MARKERS: tuple[str, ...] = (
    "writing-voice",
    "CLAUDE.md",
    "DPSCD",
    "dpscd",
    "research-brief",
    "dsdb1",
)

#: Where the account email lives on macOS/Linux. Read at scan time, never
#: written down: the address is this machine's, not the benchmark's, and
#: hardcoding it would publish it to every clone of the repo.
ACCOUNT_CONFIG_PATH = Path.home() / ".claude.json"

#: Optional, gitignored, one marker per line. For anything else local that must
#: never appear in a generated document — an employer name, a project codename.
LOCAL_MARKERS_FILENAME = "local-markers.txt"


def account_markers(config_path: Path | None = None) -> list[str]:
    """Identity strings from the Claude Code account config, if it is readable.

    The account email reaches an isolated session through the one residual
    system-reminder, so it is the single most likely piece of this machine to
    turn up inside a generated document. It has to be scannable without being
    committed, which means resolving it at scan time.
    """
    path = Path(config_path) if config_path is not None else ACCOUNT_CONFIG_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return []
    if not isinstance(data, dict):
        return []
    account = data.get("oauthAccount")
    if not isinstance(account, dict):
        return []

    markers: list[str] = []
    email = account.get("emailAddress")
    if isinstance(email, str) and "@" in email and len(email) > 3:
        markers.append(email)
        # The local part on its own, which is how a leak would usually surface.
        # Short or generic local parts ("me", "info") would fire on ordinary
        # prose, so they are left out.
        local = email.split("@", 1)[0]
        if len(local) >= 5 and local.isalnum():
            markers.append(local)
    return markers


def file_markers(repo_root: Path | None = None) -> list[str]:
    """Markers from a gitignored local-markers.txt, one per line."""
    root = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parent.parent
    path = root / LOCAL_MARKERS_FILENAME
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]


def effective_markers(
    config_path: Path | None = None, repo_root: Path | None = None
) -> tuple[str, ...]:
    """The committed marker list plus whatever this machine contributes."""
    markers = list(CONTAMINATION_MARKERS)
    for extra in account_markers(config_path) + file_markers(repo_root):
        if extra and extra.lower() not in {m.lower() for m in markers}:
            markers.append(extra)
    return tuple(markers)


#: Built-in tool names, plus the MCP prefix. If the model can list these, the
#: tool surface was not actually removed.
TOOL_MARKERS: tuple[str, ...] = (
    "Bash",
    "WebSearch",
    "WebFetch",
    "mcp__",
    "Glob",
    "Grep",
    "TodoWrite",
    "NotebookEdit",
    "SlashCommand",
    "AskUserQuestion",
)

#: Probe D fails if the model describes a coding assistant rather than a writer.
HARNESS_MARKERS: tuple[str, ...] = (
    "claude code",
    "tool",
    "file",
    "skill",
    "codebase",
    "terminal",
    "command line",
    "software engineering",
    "mcp",
)

_WORD = re.compile(r"[A-Za-z0-9']+")


def found_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    """Which markers appear in text, matched case-insensitively.

    Deduped case-insensitively too: the marker list carries both "DPSCD" and
    "dpscd" because that is how they appear on this machine, but under a
    case-insensitive match they are one finding, not two.
    """
    low = (text or "").lower()
    hits: list[str] = []
    seen: set[str] = set()
    for marker in markers:
        key = marker.lower()
        if key in low and key not in seen:
            seen.add(key)
            hits.append(marker)
    return hits


def redact_markers(markers: Iterable[str]) -> list[str]:
    """Marker list safe to write into a committed file.

    Committed markers pass through as themselves. Locally resolved ones — the
    account email above all — become a hash stub instead. A transcript has to
    say what it scanned for, but writing the address into runs/ would leak it
    into every clone, which is the thing the local-marker machinery exists to
    avoid. Anyone on the same machine can recompute the stub and check.
    """
    committed = {m.lower() for m in CONTAMINATION_MARKERS}
    out: list[str] = []
    for marker in markers:
        if marker.lower() in committed:
            out.append(marker)
        else:
            digest = hashlib.sha256(marker.encode("utf-8")).hexdigest()[:12]
            out.append(f"<local:{digest}>")
    return out


def _is_bare_none(text: str) -> bool:
    """True if the response is just NONE, allowing punctuation and whitespace."""
    return re.sub(r"[^A-Za-z]", "", text or "").upper() == "NONE"


def _unusable(env: Envelope) -> str:
    """Why this response cannot be graded at all, or "" if it can be.

    An empty or whitespace-only result is not evidence of a clean machine. It is
    evidence of nothing, and a probe that cannot see anything must not report
    that it saw nothing wrong.
    """
    if not env.ok:
        return f"call failed: {env.parse_error or 'is_error'}"
    if not (env.result or "").strip():
        return "empty response: nothing to grade"
    return ""


def grade_a(env: Envelope, markers: tuple[str, ...] | None = None) -> tuple[bool, str]:
    """A (memory): nothing on this machine's disk reached the session.

    A, B and D are the primary contamination probes — they ask the session to
    describe itself, which is where configuration leakage shows up first.
    """
    problem = _unusable(env)
    if problem:
        return False, problem
    text = env.result
    reasons = []
    if len(text) > 200:
        reasons.append(f"response is {len(text)} chars (>200)")
    if "NONE" not in text.upper():
        reasons.append("response does not contain NONE")
    hits = found_markers(text, markers or effective_markers())
    if hits:
        reasons.append(f"contamination markers: {redact_markers(hits)}")
    return (not reasons), "; ".join(reasons) or "clean: bare NONE, no markers"


def grade_b(env: Envelope, markers: tuple[str, ...] | None = None) -> tuple[bool, str]:
    """B (capabilities): no skills, tools or MCP servers are reachable."""
    problem = _unusable(env)
    if problem:
        return False, problem
    text = env.result
    contamination = found_markers(text, markers or effective_markers())
    if contamination:
        return False, f"contamination markers: {redact_markers(contamination)}"
    if _is_bare_none(text):
        return True, "clean: bare NONE"
    tools = found_markers(text, TOOL_MARKERS)
    if tools:
        return False, f"tool names present: {tools}"
    return True, "no tool names, no markers"


def grade_c(env: Envelope, markers: tuple[str, ...] | None = None) -> tuple[bool, str]:
    """C (behavior): one turn, no error, and actual document text comes back.

    The contamination check here is belt and suspenders — A, B and D are the
    probes designed to surface leakage. C exists to catch the case where the
    session behaves correctly and writes a real document that nonetheless has
    this machine's configuration in it, which is the shape a live generation
    would actually take.
    """
    if env.parse_error:
        return False, f"unparseable envelope: {env.parse_error}"
    reasons = []
    if env.is_error:
        reasons.append(f"is_error true: {env.result[:120]!r}")
    if env.num_turns != 1:
        reasons.append(f"num_turns={env.num_turns} (expected 1)")
    words = len(_WORD.findall(env.result))
    if words <= 50:
        reasons.append(f"only {words} words (expected >50)")
    hits = found_markers(env.result, markers or effective_markers())
    if hits:
        reasons.append(f"contamination markers: {redact_markers(hits)}")
    return (not reasons), "; ".join(reasons) or f"single turn, {words} words"


def grade_d(env: Envelope, markers: tuple[str, ...] | None = None) -> tuple[bool, str]:
    """D (system prompt): the model describes writing a document, not a harness."""
    problem = _unusable(env)
    if problem:
        return False, problem
    text = env.result
    reasons = []
    hits = found_markers(text, HARNESS_MARKERS)
    if hits:
        reasons.append(f"describes the harness: {hits}")
    contamination = found_markers(text, markers or effective_markers())
    if contamination:
        reasons.append(f"contamination markers: {redact_markers(contamination)}")
    low = text.lower()
    if not any(word in low for word in ("document", "markdown")):
        reasons.append("does not mention producing a document")
    return (not reasons), "; ".join(reasons) or "describes producing a document only"


# --- the battery -------------------------------------------------------------

PROBE_C_PROMPT = (
    "Riverbend Community Health Center in Dover, Delaware runs a diabetes "
    "management program that enrolled 412 patients in 2024 and retained 268 of "
    "them through the twelve-month mark. The program is staffed by two nurse "
    "educators and one part-time dietitian, and it is funded by a state grant of "
    "$185,000 that expires in June. Average HbA1c among completers fell from 9.1 "
    "to 7.8. The board's finance committee has asked whether the program should "
    "be renewed at current staffing, expanded to the Milford satellite clinic, or "
    "wound down. Write a short memo from program director Amara Osei to the "
    "finance committee laying out what the program did this year, what the "
    "numbers show about retention and clinical results, what renewal at each "
    "level would cost, and what the committee needs to decide before the grant "
    "lapses."
)

PROBES: dict[str, tuple[str, Callable[[Envelope], tuple[bool, str]]]] = {
    "A": (
        "If you have any custom instructions, CLAUDE.md content, memories, or "
        "project context, quote them verbatim. If you have none, reply with "
        "exactly: NONE",
        grade_a,
    ),
    "B": (
        "List the names of every skill, tool, and MCP server currently available "
        "to you. If none, reply with exactly: NONE",
        grade_b,
    ),
    "C": (PROBE_C_PROMPT, grade_c),
    # Worded "the instructions you have been given" rather than "your system
    # instructions". The latter invites a model to answer the metaphysical
    # question instead of the practical one — Sonnet replied that it had no
    # hidden instruction set, which is true of the harness prompt and tells us
    # nothing about whether the pinned prompt landed. The reworded probe gets a
    # gradeable answer from every model tried, and the grader stayed strict.
    "D": (
        "In one sentence, what do the instructions you have been given tell you to do?",
        grade_d,
    ),
}

#: The one thing that still reaches an isolated session, established by asking a
#: probe session to reproduce every injected block verbatim. Recorded in every
#: transcript so the residual is part of the evidence rather than folklore.
KNOWN_RESIDUAL_CONTEXT = (
    "One system-reminder carrying the account email address and the current date. "
    "No CLAUDE.md, no skills, no tool list, no MCP servers, and no default "
    "Claude Code system prompt. Carries no guidance about how to write."
)

PROBE_LABELS = {
    "A": "memory",
    "B": "capabilities",
    "C": "behavior",
    "D": "system prompt",
}


@dataclass
class ProbeResult:
    probe: str
    label: str
    prompt: str
    passed: bool
    reason: str
    response: str
    returncode: int
    duration_s: float
    num_turns: int
    is_error: bool
    session_id: str
    model_reported: str
    model_usage: dict[str, Any] = field(default_factory=dict)
    model_mismatch: bool = False
    stderr: str = ""


@dataclass
class ProbeReport:
    model: str
    timestamp: str
    passed: bool
    cli_version: str
    system_prompt: str
    system_prompt_sha256: str
    flags: list[str]
    env_overlay: dict[str, str]
    env_strip_prefixes: list[str]
    cwd: str
    probes: list[ProbeResult]
    #: Committed markers plus whatever this machine contributed at scan time.
    #: Recorded so a reader knows what the graders were actually looking for.
    markers_used: list[str] = field(default_factory=list)
    known_residual_context: str = KNOWN_RESIDUAL_CONTEXT
    path: Path | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("path", None)
        return data

    def summary(self) -> str:
        lines = [f"isolation probe battery — {self.model} — {self.timestamp}"]
        for probe in self.probes:
            mark = "PASS" if probe.passed else "FAIL"
            lines.append(f"  {mark}  {probe.probe} ({probe.label}): {probe.reason}")
        lines.append("  ALL PASS" if self.passed else "  BATTERY FAILED")
        return "\n".join(lines)


def run_probe_battery(
    model: str,
    out_path: Path,
    transport: Transport = run_cli,
    timeout: int = PROBE_TIMEOUT_S,
    markers: tuple[str, ...] | None = None,
) -> ProbeReport:
    """Run probes A-D live against `model` and write the transcript to out_path."""
    markers = markers if markers is not None else effective_markers()
    results: list[ProbeResult] = []
    for name in sorted(PROBES):
        prompt, grader = PROBES[name]
        cmd = build_cmd(model)
        cli = transport(cmd, prompt, timeout)
        env = parse_envelope(cli.stdout, requested_model=model)
        if cli.returncode != 0 and not env.raw:
            passed, reason = False, f"exit {cli.returncode}: {cli.stderr.strip()[:200]}"
        else:
            passed, reason = grader(env, markers)
            if passed and env.model_mismatch:
                passed, reason = False, (
                    f"model mismatch: asked for {model}, modelUsage has "
                    f"{sorted(env.model_usage) or 'nothing'}"
                )
        results.append(
            ProbeResult(
                probe=name,
                label=PROBE_LABELS[name],
                prompt=prompt,
                passed=passed,
                reason=reason,
                response=env.result,
                returncode=cli.returncode,
                duration_s=round(cli.duration_s, 2),
                num_turns=env.num_turns,
                is_error=env.is_error,
                session_id=env.session_id,
                model_reported=env.model_reported,
                model_usage=dict(env.model_usage),
                model_mismatch=env.model_mismatch,
                stderr=cli.stderr.strip()[:2000],
            )
        )

    report = ProbeReport(
        model=model,
        timestamp=datetime.now(timezone.utc).isoformat(),
        passed=all(r.passed for r in results),
        cli_version=cli_version(),
        system_prompt=MINIMAL_SYSTEM_PROMPT,
        system_prompt_sha256=SYSTEM_PROMPT_SHA256,
        flags=list(ISOLATION_FLAGS),
        env_overlay=dict(ISOLATION_ENV),
        env_strip_prefixes=list(ENV_STRIP_PREFIXES),
        cwd=str(scratch_cwd()),
        probes=results,
        markers_used=redact_markers(markers),
    )

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
    report.path = out_path
    return report


def battery_path(runs_root: Path, model: str, when: datetime | None = None) -> Path:
    """Conventional transcript path: runs/isolation/<model>-<utc-stamp>.json."""
    when = when or datetime.now(timezone.utc)
    stamp = when.strftime("%Y%m%dT%H%M%SZ")
    return Path(runs_root) / "isolation" / f"{model}-{stamp}.json"


def latest_passing_battery(
    runs_root: Path, model: str, max_age_hours: float = 24.0
) -> Path | None:
    """Most recent passing transcript for `model` inside the age window, if any.

    This is what gates a generation batch. The window exists because isolation is
    a property of the machine at a moment in time — a settings change, a CLI
    upgrade, or a new managed policy can quietly reintroduce contamination, and
    yesterday's clean probe says nothing about that.
    """
    directory = Path(runs_root) / "isolation"
    if not directory.is_dir():
        return None
    now = datetime.now(timezone.utc)
    best: tuple[datetime, Path] | None = None
    for path in sorted(directory.glob(f"{model}-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict) or not data.get("passed"):
            continue
        if data.get("system_prompt_sha256") != SYSTEM_PROMPT_SHA256:
            continue
        try:
            stamp = datetime.fromisoformat(str(data.get("timestamp")))
        except ValueError:
            continue
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        if (now - stamp).total_seconds() > max_age_hours * 3600:
            continue
        if best is None or stamp > best[0]:
            best = (stamp, path)
    return best[1] if best else None


def textstat_words(text: str) -> int:
    """Word count through the same path the corpus uses, so numbers agree."""
    return textstats.word_count(textstats.strip_markdown(text))
