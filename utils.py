import shutil
import sys
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def working_directory():
    work_dir = Path.cwd() / 'workdir'
    work_dir.mkdir(exist_ok=True)
    try:
        yield work_dir
    finally:
        shutil.rmtree(work_dir)


def assert_eq(a, b, test_name):
    if a != b:
        print(f'F: Test "{test_name}" failed:\n    Expected: {b}\n    Got: {a}')
        sys.exit(1)
    else:
        print(f'P: Test "{test_name}" passed.')
