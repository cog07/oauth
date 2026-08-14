from pathlib import Path

SOURCE_DIR = Path("src/main/java")

BUILD_ERROR_FILES = [
    Path("security-governance/outputs/build-errors.txt"),
    Path("security-governance/outputs/rebuild-errors.txt")
]

errors = ""

for file in BUILD_ERROR_FILES:
    if file.exists():
        errors += file.read_text(encoding="utf-8")

for java_file in SOURCE_DIR.rglob("*.java"):
    content = java_file.read_text(encoding="utf-8")

    # Spring Security 6
    if "antMatchers" in errors:
        content = content.replace(
            ".antMatchers(",
            ".requestMatchers("
        )

    if "ignoringAntMatchers" in errors:
        content = content.replace(
            ".ignoringAntMatchers(",
            ".ignoringRequestMatchers("
        )

    # Jakarta migration
    content = content.replace(
        "import javax.persistence",
        "import jakarta.persistence"
    )

    content = content.replace(
        "import javax.validation",
        "import jakarta.validation"
    )

    content = content.replace(
        "import javax.servlet",
        "import jakarta.servlet"
    )

    content = content.replace(
        "import javax.annotation",
        "import jakarta.annotation"
    )

    java_file.write_text(content, encoding="utf-8")

# Detect dependency-level issue
if "javax/servlet/http/HttpServletRequest" in errors:
    print(
        "WARNING: Detected incompatible Spring Authorization Server dependency."
    )
    print(
        "Upgrade spring-security-oauth2-authorization-server "
        "from 0.4.x to 1.3.x"
    )

print("Migration fixes applied.")