"""make.fun news-image-20261126 entry (Python 3.13, standard library only).

Copies the pre-drawn front page (entry.png, drawn by draw.py from the
headlines of Thursday 26 November 2026) to the grader's output
directory. No network, no extra dependencies; the same bytes every run.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        raise SystemExit("entry.png missing from repository")
    # /output is the grader's directory; local runs can point elsewhere.
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # Deterministic: the same bytes are copied on every run, twice in grading.
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
