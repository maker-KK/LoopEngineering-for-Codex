#!/usr/bin/env python3
"""Validate a Loop Engineering spec YAML or JSON file."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


REQUIRED_SECTIONS = [
    "loop",
    "trigger",
    "scope",
    "context",
    "implementation_toolchain",
    "execution",
    "brakes",
    "context_management",
    "tool_design",
    "evaluation",
    "observability",
    "verification",
    "human_gate",
    "persistence",
    "stop",
]


def load_spec(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        if yaml is None:
            raise RuntimeError("PyYAML is required for YAML files. Install pyyaml or use JSON.")
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("Spec root must be a mapping/object.")
    return data


def has_nonempty_list(obj: dict[str, Any], key: str) -> bool:
    value = obj.get(key)
    return isinstance(value, list) and len(value) > 0


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in data or not isinstance(data[section], dict):
            errors.append(f"Missing required section: {section}")

    if errors:
        return errors

    loop = data["loop"]
    implementation_toolchain = data["implementation_toolchain"]
    execution = data["execution"]
    brakes = data["brakes"]
    context_management = data["context_management"]
    tool_design = data["tool_design"]
    evaluation = data["evaluation"]
    observability = data["observability"]
    verification = data["verification"]
    persistence = data["persistence"]
    stop = data["stop"]
    human_gate = data["human_gate"]

    for key in ["name", "goal", "owner"]:
        if not loop.get(key):
            errors.append(f"loop.{key} is required")

    for key in ["max_iterations", "max_runtime_minutes", "max_cost_usd"]:
        value = execution.get(key)
        if not isinstance(value, (int, float)) or value <= 0:
            errors.append(f"execution.{key} must be a positive number")

    for key in ["lifecycle_verbs_enabled", "capability_slots", "scaffold_outputs", "deployment", "publish_or_register", "observability_exports"]:
        if implementation_toolchain.get(key) in (None, "", [], {}):
            errors.append(f"implementation_toolchain.{key} is required")

    lifecycle_verbs = implementation_toolchain.get("lifecycle_verbs_enabled")
    if isinstance(lifecycle_verbs, dict):
        for key in ["spec", "scaffold", "build", "evaluate", "deploy", "publish", "observe"]:
            if key not in lifecycle_verbs or not isinstance(lifecycle_verbs.get(key), bool):
                errors.append(f"implementation_toolchain.lifecycle_verbs_enabled.{key} must be true or false")

    if not has_nonempty_list(implementation_toolchain, "scaffold_outputs"):
        errors.append("implementation_toolchain.scaffold_outputs must list generated or maintained artifacts")

    if not has_nonempty_list(implementation_toolchain, "observability_exports"):
        errors.append("implementation_toolchain.observability_exports must list trace, log, score, or metadata outputs")

    deployment = implementation_toolchain.get("deployment")
    if isinstance(deployment, dict):
        for key in ["target", "dry_run_required", "smoke_test_required", "deployment_metadata"]:
            if deployment.get(key) in (None, "", []):
                errors.append(f"implementation_toolchain.deployment.{key} is required")

    publish_or_register = implementation_toolchain.get("publish_or_register")
    if isinstance(publish_or_register, dict):
        for key in ["required", "surface", "owner_visible", "access_policy"]:
            if publish_or_register.get(key) in (None, "", []):
                errors.append(f"implementation_toolchain.publish_or_register.{key} is required")

    if not has_nonempty_list(verification, "required_checks"):
        errors.append("verification.required_checks must contain at least one independent check")

    if verification.get("self_grade_allowed") is True:
        errors.append("verification.self_grade_allowed should be false for operational loops")

    for key in ["completion_check", "timeout_policy", "budget_policy", "no_progress_detection"]:
        if brakes.get(key) in (None, "", [], {}):
            errors.append(f"brakes.{key} is required")

    no_progress = brakes.get("no_progress_detection")
    if isinstance(no_progress, dict):
        for key in ["repeated_tool_call_limit", "identical_failure_limit", "action"]:
            if no_progress.get(key) in (None, "", []):
                errors.append(f"brakes.no_progress_detection.{key} is required")

    for key in ["max_active_context", "compaction_trigger", "offload_targets", "return_to_context"]:
        if context_management.get(key) in (None, "", [], {}):
            errors.append(f"context_management.{key} is required")

    if not has_nonempty_list(context_management, "offload_targets"):
        errors.append("context_management.offload_targets must contain at least one durable artifact target")

    if not has_nonempty_list(context_management, "return_to_context"):
        errors.append("context_management.return_to_context must list the small evidence slice returned to active context")

    for key in ["duplicate_guard", "actionable_error_contract"]:
        if tool_design.get(key) in (None, "", []):
            errors.append(f"tool_design.{key} is required")

    for key in ["focused_tool_count", "non_overlapping_tools", "idempotent_writes_required"]:
        if tool_design.get(key) is not True:
            errors.append(f"tool_design.{key} must be true for operational loops")

    for key in ["dataset", "minimum_score", "required_case_types", "metrics", "failure_taxonomy"]:
        if evaluation.get(key) in (None, "", [], {}):
            errors.append(f"evaluation.{key} is required")

    scenario_generation = evaluation.get("scenario_generation")
    if isinstance(scenario_generation, dict):
        target_case_count = scenario_generation.get("target_case_count")
        if not isinstance(target_case_count, int) or target_case_count <= 0:
            errors.append("evaluation.scenario_generation.target_case_count must be a positive integer")
        categories = scenario_generation.get("categories")
        if not isinstance(categories, dict) or not categories:
            errors.append("evaluation.scenario_generation.categories must list scenario categories and counts")

    score_report = evaluation.get("score_report")
    if isinstance(score_report, dict):
        for key in ["require_per_category_means", "require_top_findings", "require_baseline_candidate_compare", "require_failure_cluster_analysis"]:
            if score_report.get(key) is not True:
                errors.append(f"evaluation.score_report.{key} must be true")

    if not has_nonempty_list(evaluation, "required_case_types"):
        errors.append("evaluation.required_case_types must list core, edge, regression, human_gate, or adversarial cases")

    minimum_score = evaluation.get("minimum_score")
    if not isinstance(minimum_score, (int, float)) or not (0 < minimum_score <= 1):
        errors.append("evaluation.minimum_score must be a number between 0 and 1")

    for key in ["run_log_schema", "trace_tool_calls", "trace_costs", "trace_retries", "prompt_response_logging", "sensitive_content_policy", "feedback_to_evals"]:
        if observability.get(key) in (None, "", []):
            errors.append(f"observability.{key} is required")

    for key in ["trace_tool_calls", "trace_costs", "trace_retries"]:
        if observability.get(key) is not True:
            errors.append(f"observability.{key} must be true for operational loops")

    if observability.get("prompt_response_logging") is True:
        errors.append("observability.prompt_response_logging should default to false unless a privacy policy explicitly allows it")

    if not has_nonempty_list(persistence, "write"):
        errors.append("persistence.write must contain at least one state artifact")

    if not has_nonempty_list(human_gate, "required_when"):
        errors.append("human_gate.required_when must list escalation conditions")

    for key in ["on_success", "on_failure", "max_same_failure_count"]:
        if stop.get(key) in (None, "", []):
            errors.append(f"stop.{key} is required")

    same_failure_count = stop.get("max_same_failure_count")
    if isinstance(same_failure_count, (int, float)) and same_failure_count > execution.get("max_iterations", 0):
        errors.append("stop.max_same_failure_count should not exceed execution.max_iterations")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_loop_spec.py <loop-spec.yaml|json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Spec not found: {path}", file=sys.stderr)
        return 2

    try:
        errors = validate(load_spec(path))
    except Exception as exc:
        print(f"Invalid spec: {exc}", file=sys.stderr)
        return 1

    if errors:
        print("Loop spec validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Loop spec validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
