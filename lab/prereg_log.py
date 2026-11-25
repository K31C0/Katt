"""A tiny pre-registration log: write the pass bar down BEFORE a run, and prove later that nothing changed.

  python prereg_log.py add log.txt "SPEED-1 PREREG: reply time at most 0.85 of today, 35 prompts" plan.md data.json
  python prereg_log.py add log.txt "SPEED-1 RESULT: 0.83, bar held" results.json
  python prereg_log.py check log.txt

Each line holds the time, the text, and the SHA-256 fingerprint of every file it names. `check` re-reads the files and
says which ones no longer match. The log is append-only by habit: a mistake gets a new CORRECTION line, never an edit.
Standard library only.
"""
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

FILE = re.compile(r"\[(.+?) ([0-9a-f]{64})\]")


def fingerprint(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def add(log, text, files):
    if "\n" in text or "\r" in text:
        raise SystemExit("one line of text, please")
    marks = " ".join(f"[{Path(f).as_posix()} {fingerprint(f)}]" for f in files)
    line = f"{datetime.now().astimezone().isoformat(timespec='seconds')} {text} {marks}".rstrip() + "\n"
    with open(log, "a", encoding="utf-8", newline="\n") as f:
        f.write(line)
    print(line.strip())


def check(log):
    ok = changed = missing = 0
    for number, line in enumerate(Path(log).read_text(encoding="utf-8").splitlines(), 1):
        for name, mark in FILE.findall(line):
            if not Path(name).exists():
                missing += 1
                print(f"line {number}: {name} is missing")
            elif fingerprint(name) != mark:
                changed += 1
                print(f"line {number}: {name} changed since this line was written")
            else:
                ok += 1
    print(f"{ok} files match, {changed} changed, {missing} missing")
    return 1 if changed or missing else 0


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "add":
        add(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif len(sys.argv) == 3 and sys.argv[1] == "check":
        sys.exit(check(sys.argv[2]))
    else:
        raise SystemExit(__doc__)
