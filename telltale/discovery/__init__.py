"""M7 discovery: find candidate tells the seed registry does not have.

Four stages, and the split between them is the design:

    sweep.py     arithmetic over the corpus — where to look, no model involved
    auditor.py   four LLM lenses — what to propose, one strict output contract
    verify.py    five gates — what survives contact with the whole corpus
    dedup.py     gate 5's machinery — is this already a tell under another name

`pipeline.py` sequences them with per-stage resumability, and the CLI's
`discover` group drives it. Nothing here promotes a tell: everything that passes
enters the registry with `status: candidate`, which the default scoring path
ignores, and a human decides the rest.
"""

__all__ = ["auditor", "dedup", "pipeline", "sweep", "verify"]
