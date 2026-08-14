import json
import xml.etree.ElementTree as ET
from pathlib import Path

POM_FILE = "pom.xml"
OUTPUT_DIR = "security-governance/outputs"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

tree = ET.parse(POM_FILE)
root = tree.getroot()

namespace = {
    "m": "http://maven.apache.org/POM/4.0.0"
}

analysis = {
    "javaVersion": None,
    "springBootVersion": None,
    "springCloudVersion": None,
    "dependencies": [],
    "migrationRecommendations": []
}

# Java Version
java_version = root.find(".//m:properties/m:java.version", namespace)
if java_version is not None:
    analysis["javaVersion"] = java_version.text

# Spring Cloud Version
spring_cloud = root.find(".//m:properties/m:spring-cloud.version", namespace)
if spring_cloud is not None:
    analysis["springCloudVersion"] = spring_cloud.text

# Spring Boot Parent Version
parent = root.find(".//m:parent", namespace)

if parent is not None:
    artifact = parent.find("m:artifactId", namespace)
    version = parent.find("m:version", namespace)

    if (
        artifact is not None
        and artifact.text == "spring-boot-starter-parent"
    ):
        analysis["springBootVersion"] = version.text

# Dependencies
dependencies = root.findall(".//m:dependency", namespace)

for dep in dependencies:

    group_id = dep.find("m:groupId", namespace)
    artifact_id = dep.find("m:artifactId", namespace)
    version = dep.find("m:version", namespace)

    if group_id is None or artifact_id is None:
        continue

    dependency = {
        "groupId": group_id.text,
        "artifactId": artifact_id.text
    }

    if version is not None:
        dependency["version"] = version.text

    analysis["dependencies"].append(dependency)

    # Migration Rules

    if (
        artifact_id.text
        == "spring-security-oauth2-authorization-server"
    ):
        analysis["migrationRecommendations"].append(
            {
                "dependency":
                    "spring-security-oauth2-authorization-server",
                "issue":
                    "Spring Boot 3 incompatible Authorization Server",
                "recommendedVersion":
                    "1.3.1",
                "reason":
                    "Boot 3 requires Jakarta Servlet APIs"
            }
        )

    if (
        artifact_id.text
        == "spring-cloud-starter-netflix-eureka-client"
    ):
        analysis["migrationRecommendations"].append(
            {
                "dependency":
                    "spring-cloud-starter-netflix-eureka-client",
                "issue":
                    "Verify Spring Cloud release train compatibility",
                "recommendedVersion":
                    "2023.x or later",
                "reason":
                    "Spring Boot 3 requires newer Spring Cloud versions"
            }
        )

output_file = f"{OUTPUT_DIR}/pom-analysis.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(analysis, f, indent=2)

print("Generated:", output_file)
print(json.dumps(analysis, indent=2))