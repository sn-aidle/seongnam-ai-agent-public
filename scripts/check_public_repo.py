from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

FORBIDDEN_PATHS = (
    "storage/",
    "data/collectors/",
    "data/loaders/",
    "data/processors/",
    "ml/features/",
    "ml/training/",
    "ml/inference/",
    "backend/src/main/resources/db/",
    "backend/src/main/java/kr/go/seongnam/agent/application/agent/",
    "backend/src/main/java/kr/go/seongnam/agent/infrastructure/ai/",
    "backend/src/main/java/kr/go/seongnam/agent/infrastructure/persistence/",
)

FORBIDDEN_CONTENT = (
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][^'\"]+"),
    re.compile(r"(?i)authorization\s*:\s*bearer\s+\S+"),
    re.compile(r"https://github\.com/sn-aidle/seongnam-ai-agent(?:/|$)"),
    re.compile(r"(?i)jdbc:postgresql://"),
    re.compile(r"\bnx\s*=\s*\d+\b"),
    re.compile(r"\bny\s*=\s*\d+\b"),
)


def repository_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode() for item in result.stdout.split(b"\0") if item]


def text_for_scan(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    return re.sub(r"data:[^\"']+", "data:embedded-asset", text, flags=re.IGNORECASE)


def main() -> int:
    violations: list[str] = []
    for path in repository_files():
        relative = path.relative_to(ROOT).as_posix()
        if relative == ".env" or any(relative.startswith(prefix) for prefix in FORBIDDEN_PATHS):
            violations.append(f"공개 제외 경로: {relative}")
        if path.resolve() == SELF:
            continue
        text = text_for_scan(path)
        if text is None:
            continue
        for pattern in FORBIDDEN_CONTENT:
            if pattern.search(text):
                violations.append(f"공개 금지 내용: {relative} ({pattern.pattern})")

    if violations:
        print("\n".join(violations), file=sys.stderr)
        return 1
    print("저장소 공개 안전 검사를 통과했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
