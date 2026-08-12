import json
from pathlib import Path

output = [
    {
        "issue_key": "JAVA17",
        "message": "Upgrade Java 11 to Java 17",
        "file_path": "pom.xml",
        "severity": "HIGH"
    },
    {
        "issue_key": "SPRINGBOOT3",
        "message": "Upgrade Spring Boot 2.7 to Spring Boot 3.0",
        "file_path": "pom.xml",
        "severity": "HIGH"
    }
]

Path("security-governance/outputs").mkdir(parents=True, exist_ok=True)

with open(
    "security-governance/outputs/issues.normalized.json",
    "w"
) as f:
    json.dump(output, f, indent=2)

print("Normalized 2 issues")