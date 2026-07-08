#!/usr/bin/env python3
"""Run project-local in-loop verification checks.

The manifest format intentionally supports a small YAML subset so the tool can
run without external dependencies. JSON manifests are also supported.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


VALID_PHASES = {"write", "pr", "merge", "all"}


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return int(value)
    except ValueError:
        return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    checks: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_checks = False

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()

        if stripped == "checks:":
            in_checks = True
            result["checks"] = checks
            continue

        if not in_checks and ":" in stripped:
            key, value = stripped.split(":", 1)
            result[key.strip()] = parse_scalar(value)
            continue

        if in_checks:
            if stripped.startswith("- "):
                current = {}
                checks.append(current)
                item = stripped[2:]
                if ":" in item:
                    key, value = item.split(":", 1)
                    current[key.strip()] = parse_scalar(value)
                continue
            if current is not None and ":" in stripped:
                key, value = stripped.split(":", 1)
                current[key.strip()] = parse_scalar(value)
                continue

        raise ValueError(f"Unsupported manifest line: {raw}")

    return result


def load_manifest(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
        if not isinstance(loaded, dict):
            raise ValueError("manifest root must be an object")
        return loaded
    except ModuleNotFoundError:
        return parse_simple_yaml(text)


def normalize_check(raw: dict[str, Any], default_timeout: int) -> dict[str, Any]:
    required = bool(raw.get("required", True))
    timeout = int(raw.get("timeout_seconds", default_timeout))
    phase = str(raw.get("phase", "write")).strip().lower()
    command = str(raw.get("command", "")).strip()
    check_id = str(raw.get("id", command[:40] or "unnamed-check")).strip()
    if phase not in {"write", "pr", "merge"}:
        raise ValueError(f"{check_id}: invalid phase {phase!r}")
    if not command:
        raise ValueError(f"{check_id}: command is required")
    return {
        "id": check_id,
        "phase": phase,
        "command": command,
        "required": required,
        "timeout_seconds": timeout,
        "description": str(raw.get("description", "")),
    }


def run_check(check: dict[str, Any], cwd: Path, dry_run: bool) -> dict[str, Any]:
    started = time.time()
    record = {
        "id": check["id"],
        "phase": check["phase"],
        "command": check["command"],
        "required": check["required"],
        "timeout_seconds": check["timeout_seconds"],
        "dry_run": dry_run,
        "exit_code": 0,
        "duration_seconds": 0.0,
        "passed": True,
        "stdout_tail": "",
        "stderr_tail": "",
    }
    if dry_run:
        return record

    try:
        completed = subprocess.run(
            check["command"],
            cwd=str(cwd),
            shell=True,
            text=True,
            capture_output=True,
            timeout=check["timeout_seconds"],
        )
        record["exit_code"] = completed.returncode
        record["stdout_tail"] = completed.stdout[-4000:]
        record["stderr_tail"] = completed.stderr[-4000:]
        record["passed"] = completed.returncode == 0 or not check["required"]
    except subprocess.TimeoutExpired as exc:
        record["exit_code"] = 124
        record["stdout_tail"] = (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else ""
        record["stderr_tail"] = (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else ""
        record["passed"] = not check["required"]
        record["timeout"] = True
    finally:
        record["duration_seconds"] = round(time.time() - started, 3)

    return record


def default_working_directory(manifest_path: Path) -> Path:
    """Use the project root when the manifest lives under a .codex folder."""
    manifest_parent = manifest_path.parent.resolve()
    if manifest_parent.name.lower() == ".codex":
        return manifest_parent.parent.resolve()
    return manifest_parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Run in-loop verification checks.")
    parser.add_argument("--manifest", required=True, help="Path to project-check manifest.")
    parser.add_argument("--phase", choices=sorted(VALID_PHASES), default="write")
    parser.add_argument(
        "--cwd",
        help="Working directory. Defaults to project root for .codex manifests, otherwise manifest parent.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--out", help="Write JSON run log to this path.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest not found: {manifest_path}")

    manifest = load_manifest(manifest_path)
    default_timeout = int(manifest.get("default_timeout_seconds", 120))
    fail_fast = bool(manifest.get("fail_fast", True))
    cwd = Path(args.cwd).resolve() if args.cwd else default_working_directory(manifest_path)

    raw_checks = manifest.get("checks", [])
    if not isinstance(raw_checks, list) or not raw_checks:
        raise ValueError("manifest must include at least one check")

    checks = [normalize_check(item, default_timeout) for item in raw_checks]
    selected = [c for c in checks if args.phase == "all" or c["phase"] == args.phase]
    if not selected:
        raise ValueError(f"no checks selected for phase {args.phase!r}")

    run_log: dict[str, Any] = {
        "manifest": str(manifest_path),
        "project": manifest.get("project", cwd.name),
        "phase": args.phase,
        "cwd": str(cwd),
        "dry_run": args.dry_run,
        "started_at_epoch": int(time.time()),
        "checks": [],
        "passed": True,
    }

    for check in selected:
        print(f"[in-loop] {check['phase']}:{check['id']} :: {check['command']}")
        record = run_check(check, cwd, args.dry_run)
        run_log["checks"].append(record)
        if not record["passed"]:
            run_log["passed"] = False
            print(f"[in-loop] FAILED {check['id']} exit={record['exit_code']}", file=sys.stderr)
            if fail_fast:
                break
        else:
            print(f"[in-loop] passed {check['id']} exit={record['exit_code']}")

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(run_log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"passed": run_log["passed"], "checks": len(run_log["checks"])}, ensure_ascii=False))
    return 0 if run_log["passed"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
