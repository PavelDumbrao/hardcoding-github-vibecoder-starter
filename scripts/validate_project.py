from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["README.md", "PROJECT.md", "TASKS.md", "AGENTS.md", ".gitignore"]
SECRET_FILES = [".env", "id_rsa", "id_ed25519"]
SUSPICIOUS_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"]?[A-Za-z0-9_\-]{16,}"),
]

errors: list[str] = []

for name in REQUIRED:
    if not (ROOT / name).exists():
        errors.append(f"missing required file: {name}")

tracked_text_ext = {".md", ".txt", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml"}

for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue
    if path.name in SECRET_FILES:
        errors.append(f"secret-like file must not be committed: {path.relative_to(ROOT)}")
    if path.suffix.lower() not in tracked_text_ext:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern.search(text):
            errors.append(f"possible secret in: {path.relative_to(ROOT)}")

if errors:
    print("VALIDATION FAILED")
    for item in errors:
        print("-", item)
    raise SystemExit(1)

print("VALIDATION OK")
