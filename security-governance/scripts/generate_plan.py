import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "security-governance" / "outputs"

pom_file = OUTPUT_DIR / "pom-analysis.json"
source_file = OUTPUT_DIR / "source-analysis.json"

with open(pom_file, "r", encoding="utf-8") as f:
    pom = json.load(f)

with open(source_file, "r", encoding="utf-8") as f:
    source = json.load(f)

target_java = "17"
target_spring_boot = "3.3.13"

remediation_json = {
    "currentJavaVersion": pom["javaVersion"],
    "targetJavaVersion": target_java,
    "currentSpringBootVersion": pom["springBootVersion"],
    "targetSpringBootVersion": target_spring_boot,
    "jakartaMigrationRequired": source["jakartaMigrationRequired"],
    "findings": source["findings"]
}

with open(
    OUTPUT_DIR / "remediation-plan.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(remediation_json, f, indent=2)

md_content = f"""
# Migration Plan

## Current State

- Java Version: {pom["javaVersion"]}
- Spring Boot Version: {pom["springBootVersion"]}
- Spring Cloud Version: {pom["springCloudVersion"]}

## Target State

- Java Version: {target_java}
- Spring Boot Version: {target_spring_boot}

## Findings

Total Jakarta Migration Findings: {source["totalFindings"]}

"""

for finding in source["findings"]:
    md_content += (
        f"- {finding['file']} : "
        f"{finding["total']} -> {finding['action']}\n"
    )

md_content += """

## Planned Activities

1. Upgrade Java version
2. Upgrade Maven compiler plugin
3. Upgrade Spring Boot version
4. Replace javax.* imports with jakarta.*
5. Run Maven compile
6. Run Maven tests
7. Create Pull Request

## Approval Required

Human approval required before migration.
"""

with open(
    OUTPUT_DIR / "remediation-plan.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(md_content)

assessment = {
    "status": "ready-for-approval",
    "migrationType": "java17-springboot3",
    "riskLevel": "medium",
    "jakartaMigrationRequired": source["jakartaMigrationRequired"]
}

with open(
    OUTPUT_DIR / "migration-assessment.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(assessment, f, indent=2)

print("Generated:")
print(" - remediation-plan.json")
print(" - remediation-plan.md")
print(" - migration-assessment.json")