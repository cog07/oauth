import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "security-governance" / "outputs"

remediation_file = OUTPUT_DIR / "remediation-plan.json"
build_error_file = OUTPUT_DIR / "build-errors.txt"

with open(remediation_file, "r", encoding="utf-8") as f:
    remediation = json.load(f)

build_errors = ""

if build_error_file.exists():
    build_errors = build_error_file.read_text(encoding="utf-8")

task = f"""
# GitHub Copilot Migration Task

## Current State

Java Version: {remediation["currentJavaVersion"]}
Spring Boot Version: {remediation["currentSpringBootVersion"]}

## Target State

Java Version: {remediation["targetJavaVersion"]}
Spring Boot Version: {remediation["targetSpringBootVersion"]}

## Detected Findings

"""

for finding in remediation["findings"]:
    task += f"""
- File: {finding['file']}
- Current: {finding['issue']}
- Target: {finding['action']}
"""

task += f"""

## Build Errors

{build_errors}

## Required Actions

1. Fix compilation errors.
2. Replace deprecated Spring Security APIs.
3. Replace javax.* imports with jakarta.*.
4. Preserve business functionality.
5. Ensure mvn clean test succeeds.
6. Update only migration-related code.
7. Generate a migration summary.

## Success Criteria

- Application compiles successfully.
- All tests pass.
- No business functionality changes.
"""

agent_file = OUTPUT_DIR / "agent-task.md"

agent_file.write_text(task, encoding="utf-8")

print(f"Generated: {agent_file}")