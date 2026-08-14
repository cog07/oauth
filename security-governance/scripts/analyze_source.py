import json
from pathlib import Path

SOURCE_DIR = "src/main/java"
OUTPUT_DIR = "security-governance/outputs"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

findings = []

patterns = [
    "javax.persistence",
    "javax.validation",
    "javax.servlet",
    "javax.annotation"
]

for java_file in Path(SOURCE_DIR).rglob("*.java"):

    try:
        content = java_file.read_text(encoding="utf-8")

        for pattern in patterns:
            if pattern in content:
                findings.append({
                    "file": str(java_file),
                    "issue": pattern,
                    "action": pattern.replace("javax", "jakarta")
                })

    except Exception as e:
        print(f"Skipping {java_file}: {e}")

analysis = {
    "jakartaMigrationRequired": len(findings) > 0,
    "totalFindings": len(findings),
    "findings": findings
}

output_file = f"{OUTPUT_DIR}/source-analysis.json"

with open(output_file, "w") as f:
    json.dump(analysis, f, indent=2)

print("Generated:", output_file)
print(json.dumps(analysis, indent=2))