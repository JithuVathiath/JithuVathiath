#!/usr/bin/env python3
"""Compatibility entry point for the current professional blue palette."""
import runpy
from pathlib import Path
if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('apply_blue_palette.py')), run_name='__main__')
