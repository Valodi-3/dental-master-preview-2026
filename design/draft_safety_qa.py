from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAIN = "9a99dc7baa6484bbec8b1823152f60a59bdbae2e"
EXPECTED_TECH = "72ad9a3de2668eb2fa7e3f3034a844f0d085fe69"
BRANCH = "design/manus-dental-master-2026"
REPO = "Valodi-3/dental-master-preview-2026"


def run(args: list[str]) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8").strip()


def remote_sha(ref: str) -> str:
    result = run(["git", "ls-remote", "--heads", "origin", ref])
    fields = result.split()
    if len(fields) != 2 or fields[1] != f"refs/heads/{ref}" or len(fields[0]) != 40:
        raise AssertionError(f"Cannot verify remote ref {ref}: {result!r}")
    return fields[0]


def main() -> None:
    if run(["git", "branch", "--show-current"]) != BRANCH:
        raise AssertionError("Working branch is not the isolated design branch")
    head = run(["git", "rev-parse", "HEAD"])
    if remote_sha(BRANCH) != head:
        raise AssertionError("Remote design branch does not match local commit")
    if remote_sha("main") != EXPECTED_MAIN:
        raise AssertionError("Remote main changed from the recorded original")
    if remote_sha("tech/dental-master-foundation-2026") != EXPECTED_TECH:
        raise AssertionError("Remote technical foundation changed from the recorded original")
    pr = json.loads(run(["gh", "pr", "view", "2", "--repo", REPO, "--json", "state,isDraft,baseRefName,headRefName,mergedAt"]))
    if not (
        pr["state"] == "OPEN"
        and pr["isDraft"] is True
        and pr["baseRefName"] == "main"
        and pr["headRefName"] == BRANCH
        and pr["mergedAt"] is None
    ):
        raise AssertionError(f"PR #2 is not an open, unmerged draft against main: {pr}")
    changed = run(["git", "diff", "origin/main...HEAD", "--name-only"]).splitlines()
    protected = [
        name for name in changed
        if name == "app.js"
        or name.startswith("tech-root-qa")
        or name.endswith("_test.py")
        or "/tests/" in name.replace("\\", "/")
        or name.startswith("tests/")
    ]
    if protected:
        raise AssertionError("Protected/shared/test files appear in the design diff: " + ", ".join(protected))
    if run(["git", "status", "--porcelain"]):
        raise AssertionError("Worktree must be committed and clean before final draft-safety verification")
    print(f"DRAFT_SAFETY_PASS branch={BRANCH} pr=2 openDraft=true mainUnchanged=true techUnchanged=true protectedFiles=0 head={head[:12]}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"DRAFT_SAFETY_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
