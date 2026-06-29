# Agentic Engineering Toolchain

Use this reference when a loop must move from a prompt-driven demo to an inspectable agent workflow with scaffolding, evaluations, deployment, registration, and observability.

## Problem Pattern

Agent work often crosses editor, terminal, browser, cloud console, and a separate eval framework. Every context switch loses intent, state, and verification evidence. A loop should collapse those handoffs into a versioned manifest, repeatable commands, and artifacts that the next run can inspect.

## Capability Slots

Treat these as pluggable slots. Use local equivalents when Google ADK, Agents CLI, Agent Runtime, or Gemini Enterprise are not part of the system.

| Slot | Purpose | Typical artifact |
| --- | --- | --- |
| Workflow / Spec | Capture goal, tools, constraints, and success criteria before code. | `.loop-spec.yaml`, `.agents-cli-spec.md`, PRD, runbook |
| Scaffold | Create a production-shaped starting point instead of a blank folder. | project skeleton, eval folders, CI, manifest, README |
| Code Patterns | Encode framework-specific agent, tool, callback, state, and orchestration patterns. | skill, reference docs, templates |
| Eval | Generate traces, grade with deterministic and judge metrics, compare, and analyze failures. | dataset, traces, score report, failure clusters |
| Deploy | Ship only after checks pass and a dry-run or preview is understood. | deployment metadata, smoke test result, rollback plan |
| Publish / Registry | Make a deployed agent discoverable and governed. | catalog entry, owner, IAM policy, agent card |
| Observability | Trace requests, model calls, tool spans, latency, errors, cost, and feedback. | trace links, BigQuery/log tables, run log, score trend |
| CI/CD | Make the loop repeatable under source control. | PR checks, deploy workflow, eval gate |

## Lifecycle Verbs

Use these verbs when designing toolchain support:

1. `spec`: write the contract and constraints.
2. `scaffold`: generate the project or runbook structure.
3. `build`: implement the agent, tools, prompts, or workflow body.
4. `orchestrate`: split specialists only when one agent has too much context or tool authority.
5. `evaluate`: generate, grade, compare, analyze, and improve.
6. `deploy`: preview and ship to the target runtime or operational surface.
7. `publish`: register for discovery, ownership, and access control.
8. `observe`: trace real runs and feed failures back into evals.

## Evaluation Shape

For agent loops, prefer a small scenario matrix over a single happy-path test. A RAG-like loop can start with:

| Category | What it tests |
| --- | --- |
| Correct retrieval | Answer is present in allowed sources. |
| Insufficient context | Agent should abstain instead of using general knowledge. |
| Multi-hop | Answer requires combining multiple retrieved facts or tool results. |
| Citation / provenance | Every claim, source ID, diff, or decision points to the right evidence. |

Use deterministic checks for facts that can be parsed, such as citation IDs, forbidden path changes, schema validity, or command exit codes. Use LLM-as-judge only for semantic quality that cannot be reduced to a stable rule. Report per-category means and the top root-cause findings, not only an overall score.

## Deployment And Publish Gate

Deployment is not complete when a command succeeds. Require:

- Dry-run or preview reviewed for infrastructure and permission changes.
- Smoke test against the deployed endpoint or operational surface.
- Deployment metadata saved with runtime, version, region, owner, and rollback path.
- Least-privilege identity or access policy confirmed.
- Registration or catalog entry created when other teams or agents must discover it.
- Observability enabled before broad use.

If the loop only produces drafts, map `deploy` to the draft handoff and map `publish` to the place where reviewers can find it, such as a PR, ticket, or registry page.

## Observability Feedback

Record trace fields that let a reviewer replay the run:

- run ID, loop version, lifecycle stage, and trigger.
- model calls, tool calls, subagent handoffs, retries, latency, and cost.
- eval dataset version, per-category scores, and score deltas.
- failure clusters, root-cause findings, and the prompt/tool/policy line that changed.
- deployment or publish metadata when applicable.
- privacy decision for prompt/response logging.

Convert production or manual-run failures into regression eval cases before raising autonomy.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Treating a successful scaffold as a finished loop. | Run evals and smoke tests before deployment or scheduling. |
| Shipping an isolated endpoint that nobody can discover or govern. | Add publish or registry criteria with owner and access policy. |
| Using only LLM judgment for verifiable facts. | Add deterministic metrics first, then semantic rubrics. |
| Recording traces but no eval feedback loop. | Convert observed failures into dataset cases and compare the next run. |
| Adding tools without a manifest update. | Keep allowed tools, identities, and side effects versioned. |
