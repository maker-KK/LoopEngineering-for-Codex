# In-Loop Verification

Use this reference when a loop should catch issues while work is being written, not after a PR or scheduled run has already accumulated more changes.

## Definition

In-Loop Verification means the loop runs CI-equivalent checks inside the work cycle:

1. The agent writes or changes an artifact.
2. The loop immediately runs the relevant checks for that stage.
3. The loop fixes failures before adding more work on top.
4. The loop persists the check result and only advances when the gate passes or escalates.

Out-of-loop review catches defects after the fact. In-loop verification prevents the loop from compounding unverified work.

## Operating Modes

| Mode | Use when | Gate |
| --- | --- | --- |
| Advisory | The task is design-only or cannot be checked automatically. | Human review or written risk note |
| Write-time | Editing code, docs, prompts, specs, configs, or scripts. | Fast checks after each meaningful change |
| PR-repair | A pull request exists and CI or review found issues. | Patch, rerun failed checks, update PR context |
| Merge-gated | The loop can propose merge readiness. | Full required checks pass with recorded evidence |

Do not call a loop In-Loop unless it has a check manifest, a runnable gate, a failure response, and a run log.

## Project Check Manifest

Each project should keep a small manifest near the repo root, usually:

```text
.codex/project-check-manifest.yaml
```

The manifest names checks by phase:

- `write`: fast checks that should run during editing.
- `pr`: checks to run before opening or updating a PR.
- `merge`: checks that must pass before saying the change is clean.

Start from `references/project-check-manifest-template.yaml` and copy it into the project being worked on. Keep the manifest project-local, not inside the global skill folder.

## Gate Runner

Use `scripts/run_in_loop_checks.py` to execute the manifest:

```bash
python <loop-skill>/scripts/run_in_loop_checks.py --manifest .codex/project-check-manifest.yaml --phase write
```

Use `--dry-run` before trusting a new manifest:

```bash
python <loop-skill>/scripts/run_in_loop_checks.py --manifest .codex/project-check-manifest.yaml --phase all --dry-run
```

Write logs when the loop may continue across turns:

```bash
python <loop-skill>/scripts/run_in_loop_checks.py --manifest .codex/project-check-manifest.yaml --phase pr --out .codex/in-loop-run-log.json
```

## Failure Handling

When a check fails:

1. Stop adding unrelated work.
2. Preserve the failing command, exit code, and output.
3. Fix the smallest likely cause.
4. Rerun the failed check first.
5. Rerun the broader phase only after the failed check passes.
6. Escalate after repeated identical failures or when the fix requires business judgment.

Treat repeated failures, unchanged diffs, or the same command failing with the same output as no-progress signals.

## PR Repair Loop

For PR-oriented work, keep the generator and verifier roles separate:

- Generator writes the patch.
- Gate runner executes the required phase.
- Reviewer or checker summarizes failures without inventing fixes.
- Generator patches only the relevant files.
- Gate runner reruns checks.

Do not merge or claim readiness because the code compiles. Claim readiness only when the manifest's required gate passes.

## Minimal Manifest

If a project has no check manifest, create a minimal one before substantial edits. Choose the checks from existing package scripts, CI config, test commands, or project docs. If no reliable command exists, mark the loop advisory and require human review.

## Readiness Checklist

- A project-local manifest exists.
- Checks are split into write, PR, and merge phases.
- Fast checks are cheap enough to run during editing.
- Required checks fail closed.
- Optional checks are clearly marked.
- The run log captures command, exit code, duration, and output excerpt.
- Failures feed back into the loop's eval dataset or project notes.
- The agent does not continue piling changes on top of a known failing gate.
