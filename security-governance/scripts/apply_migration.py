from pathlib import Path

SOURCE_DIR = Path("src/main/java")

for file in SOURCE_DIR.rglob("*.java"):
    content = file.read_text(encoding="utf-8")

    content = content.replace(
        ".antMatchers(",
        ".requestMatchers("
    )

    content = content.replace(
        ".ignoringAntMatchers(",
        ".ignoringRequestMatchers("
    )

    file.write_text(content, encoding="utf-8")

print("Spring Security migration applied")