#!/usr/bin/env python3
"""Check publication-source integrity and rerun the bounded illustration.

This is a content-integrity check, not a novelty, safety, peer-review, licensing,
or external-link verification. It needs only the Python standard library.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REFERENCES = set(range(1, 29))
REQUIRED = (
    "README.md",
    "paper.md",
    "references.md",
    "LICENSE.md",
    "CITATION.cff",
    "examples/semantic_drift.py",
    "examples/change-admission.yaml",
    "examples/semantic-drift-result.json",
    "scripts/build_paper.py",
    "scripts/check_references.py",
    "scripts/test_check_references.py",
    "requirements-refchecker.txt",
    "scripts/package_release.py",
    "release/license-notice.txt",
    "release/supplement-README.md",
    "release/zenodo-upload.md",
    "release/zenodo-upload-metadata.json",
)
# Bibliography links identify primary publishers, authors, or official projects.
# Host recognition alone does not verify a page's claims.
PRIMARY_HOSTS = {
    "doi.org", "arxiv.org", "www.w3.org", "www.usenix.org",
    "www.openpolicyagent.org", "cdn.aaai.org", "www.cs.cornell.edu",
    "ontology.ihmc.us", "ontology.inferal.com", "userpages.cs.umbc.edu",
}


def numeric_ids(group: str) -> set[int]:
    result = set()
    for part in group.split(","):
        endpoints = re.split(r"\s*[-–]\s*", part.strip())
        if len(endpoints) == 1:
            result.add(int(endpoints[0]))
        elif len(endpoints) == 2:
            start, end = map(int, endpoints)
            if start > end:
                raise ValueError(f"reversed citation range: {part}")
            result.update(range(start, end + 1))
        else:
            raise ValueError(f"invalid citation range: {part}")
    return result


def strip_code_and_check_fences(text: str) -> tuple[str, list[str]]:
    remaining, problems = [], []
    opened = None
    for number, line in enumerate(text.splitlines(), 1):
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if opened is None:
            if fence:
                opened = (fence.group(1)[0], len(fence.group(1)), number)
            else:
                remaining.append(re.sub(r"(`+).*?\1", "", line))
        elif fence and fence.group(1)[0] == opened[0] and len(fence.group(1)) >= opened[1] and not fence.group(2).strip():
            opened = None
    if opened:
        problems.append(f"unclosed code fence at line {opened[2]}")
    return "\n".join(remaining), problems


def math_problems(text: str) -> list[str]:
    # Dollar math only: the manuscript is authored in Pandoc dollar syntax.
    # Ignore escaped dollars; fenced and inline code have already been removed.
    tokens = list(re.finditer(r"(?<!\\)(?:\$\$|\$)", text))
    opened = None
    problems = []
    for token in tokens:
        if opened is None:
            opened = token
        elif token.group() == opened.group():
            opened = None
        else:
            problems.append("mixed inline/display dollar delimiters")
    if opened is not None:
        line = text[:opened.start()].count("\n") + 1
        problems.append(f"unclosed {opened.group()} math delimiter near line {line}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable results")
    args = parser.parse_args()
    checks = []

    def record(name: str, problems: list[str], detail: str) -> None:
        checks.append({"name": name, "passed": not problems, "detail": detail, "problems": problems})

    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    empty = [path for path in REQUIRED if (ROOT / path).is_file() and not (ROOT / path).read_text().strip()]
    record("required source artifacts", [f"missing: {path}" for path in missing] + [f"empty: {path}" for path in empty], f"{len(REQUIRED)} required source artifacts")

    documents = {str(path.relative_to(ROOT)): path.read_text() for path in ROOT.rglob("*.md") if not any(part in {".git", "output"} or part.startswith('.venv') for part in path.relative_to(ROOT).parts)}
    bibliography = documents.get("references.md", "")
    records = re.findall(r"^\[(\d+)\]\s+(.+?)(?=\n\n\[\d+\]|\Z)", bibliography, flags=re.M | re.S)
    numbers = [int(number) for number, _ in records]
    problems = []
    if len(numbers) != len(set(numbers)):
        problems.append("duplicate bibliography numbers")
    if set(numbers) != EXPECTED_REFERENCES:
        problems.append(f"expected IDs 1–28; missing {sorted(EXPECTED_REFERENCES - set(numbers))}, unexpected {sorted(set(numbers) - EXPECTED_REFERENCES)}")
    paper = documents.get("paper.md", "")
    cited = set()
    for match in re.finditer(r"\[([0-9]+(?:\s*[-–,]\s*[0-9]+)*)\]", paper):
        try:
            cited.update(numeric_ids(match.group(1)))
        except ValueError as error:
            problems.append(str(error))
    if cited - set(numbers):
        problems.append(f"citations without bibliography records: {sorted(cited - set(numbers))}")
    if set(numbers) - cited:
        problems.append(f"selected records never cited in manuscript: {sorted(set(numbers) - cited)}")
    record("manuscript and selected bibliography", problems, f"{len(cited)} cited IDs; {len(numbers)} selected records")

    problems = []
    for number, record_text in records:
        urls = re.findall(r"\]\((https://[^\s)]+)\)", record_text)
        if not any(urlparse(url).hostname in PRIMARY_HOSTS for url in urls):
            problems.append(f"reference [{number}] lacks a selected primary-source URL")
        titles = re.findall(r"“([^”]+)”|\*([^*]+)\*", record_text)
        title = next((left or right for left, right in titles), "")
        if len(title.strip()) < 5 or re.search(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER)\b|citation needed|insert title", title, re.I):
            problems.append(f"reference [{number}] has missing or placeholder title metadata")
    record("primary links and bibliography titles", problems, f"{len(records)} selected bibliography records")

    problems = []
    for path, text in documents.items():
        for target in re.findall(r"\]\(([^\s)]+)\)", text):
            parsed = urlparse(target)
            if parsed.scheme or not parsed.path:
                continue
            local_path = (ROOT / path).parent / parsed.path
            if not local_path.exists():
                problems.append(f"{path}: missing linked file {target}")
    record("local documentation links", problems, f"{len(documents)} Markdown source files")

    problems = []
    marker = re.compile(r"|||<\|[^>]+\|>|\bturn\d+(?:search|view|fetch)\d+\b|^<<<<<<< |^>>>>>>> |^=======$|\b(?:TODO|TBD|FIXME)\b|\[citation needed\]", re.M)
    for path, text in documents.items():
        no_code, fence_errors = strip_code_and_check_fences(text)
        problems.extend(f"{path}: {error}" for error in fence_errors + math_problems(no_code))
        for match in marker.finditer(text):
            line = text[:match.start()].count("\n") + 1
            problems.append(f"{path}:{line}: unresolved or tool-only marker {match.group()!r}")
    record("Markdown, math, and publication markers", problems, f"{len(documents)} source Markdown files; generated output excluded")

    problems = []
    example = ROOT / "examples/semantic_drift.py"
    saved = ROOT / "examples/semantic-drift-result.json"
    if example.is_file() and saved.is_file():
        try:
            execution = subprocess.run([sys.executable, str(example)], cwd=ROOT, text=True, capture_output=True, check=True, timeout=30)
            actual = json.loads(execution.stdout)
            expected = json.loads(saved.read_text())
            if actual != expected:
                problems.append("saved example result differs from fresh execution")
            schema = (ROOT / "examples/change-admission.yaml").read_text()
            match = re.search(r"^  expansion_witnesses: \[(.*?)\]$", schema, re.M)
            witnesses = [part.strip() for part in match.group(1).split(",") if part.strip()] if match else None
            if witnesses != actual.get("expansion_witnesses"):
                problems.append("schema expansion witness IDs differ from executable result")
            if "illustration only" not in actual.get("limitations", "") or not actual.get("scope"):
                problems.append("example output lacks explicit bounded scope and illustration limitation")
            if execution.stderr.strip():
                problems.append(f"example wrote stderr: {execution.stderr.strip()}")
        except (subprocess.SubprocessError, json.JSONDecodeError, OSError) as error:
            problems.append(f"example execution/result check failed: {error}")
    else:
        problems.append("example source or saved result missing")
    declarations = paper.partition("# Declarations")[2]
    if "synthetic thought experiments" not in declarations or "No human-subject study" not in declarations or "agent-performance experiment" not in declarations:
        problems.append("manuscript declarations lack explicit synthetic-case and no-experiment scope")
    record("finite illustrative example and reporting scope", problems, "fresh subprocess execution and saved JSON agreement; explicit illustrative scope")

    report = {"passed": all(check["passed"] for check in checks), "checks": checks, "limitations": [
        "No external links are fetched; source identity and claim support must be assessed from the primary sources.",
        "Balanced delimiters do not establish valid LaTeX compilation or PDF layout.",
        "The finite example does not establish general entailment, operational mediation, safety, or performance.",
        "The checker cannot certify novelty, legal legitimacy, rights, author approval, or Zenodo publication readiness.",
    ]}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for check in checks:
            print(f"{'PASS' if check['passed'] else 'FAIL'} {check['name']}: {check['detail']}")
            for problem in check["problems"]:
                print(f"  {problem}")
        print(f"{'PASS' if report['passed'] else 'FAIL'} publication-source integrity; see --json for limitations")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
