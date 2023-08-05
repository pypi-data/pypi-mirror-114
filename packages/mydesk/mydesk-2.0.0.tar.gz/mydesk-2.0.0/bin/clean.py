#!/usr/bin/python3

import glob
import shutil
import pathlib

[shutil.rmtree(d) for d in [
    ".eggs",
    "build",
    "dist"
] if pathlib.Path(d).exists()]
[shutil.rmtree(d) for d in glob.glob("*.egg-info", recursive=False)]

[f.unlink() for f in glob.glob("*.pyc")]
[f.unlink() for f in glob.glob("*.pyo")]
