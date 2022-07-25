#!/usr/bin/env python3
import os
from pathlib import Path
from utils import working_directory, assert_eq

from diff import Difference
from snapshot import DirectorySnapshot, FileSnapshot


if __name__ == '__main__':
    print('\nDirectorySnapshot tests:\n')
    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        snapshot1 = DirectorySnapshot(work_dir)
        assert_eq(
            set(snapshot1.entries),
            {FileSnapshot(work_dir / 'file1.txt', work_dir)},
            'Single file',
        )

    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        (work_dir / 'file2.txt').write_text('hello world')
        snapshot1 = DirectorySnapshot(work_dir)
        assert_eq(
            set(snapshot1.entries),
            {
                FileSnapshot(work_dir / 'file1.txt', work_dir),
                FileSnapshot(work_dir / 'file2.txt', work_dir),
            },
            'Multiple file',
        )

    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        (work_dir / 'dir').mkdir()
        (work_dir / 'dir' / 'file2.txt').write_text('hello world')
        snapshot1 = DirectorySnapshot(work_dir)
        assert_eq(
            set(snapshot1.entries),
            {
                FileSnapshot(work_dir / 'file1.txt', work_dir),
                FileSnapshot(work_dir / 'dir' / 'file2.txt', work_dir),
            },
            'Files and directories',
        )

    print('\n.diff() tests:\n')
    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        snapshot1 = DirectorySnapshot(work_dir)
        snapshot2 = DirectorySnapshot(work_dir)
        assert_eq(
            snapshot1.diff(snapshot2),
            Difference(),
            'No changes',
        )

    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        (work_dir / 'file2.txt').write_text('world')
        snapshot1 = DirectorySnapshot(work_dir)
        (work_dir / 'file3.txt').write_text('new file')
        snapshot2 = DirectorySnapshot(work_dir)
        assert_eq(
            snapshot1.diff(snapshot2),
            Difference(new_files={Path('file3.txt')}),
            'Single new file',
        )

    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        (work_dir / 'file2.txt').write_text('world')
        snapshot1 = DirectorySnapshot(work_dir)
        (work_dir / 'file2.txt').unlink()
        snapshot2 = DirectorySnapshot(work_dir)

        assert_eq(
            snapshot1.diff(snapshot2),
            Difference(deleted_files={Path('file2.txt')}),
            'Single removed file',
        )

    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        (work_dir / 'file2.txt').write_text('world')
        snapshot1 = DirectorySnapshot(work_dir)
        (work_dir / 'file3.txt').write_text('new file')
        (work_dir / 'file2.txt').unlink()
        snapshot2 = DirectorySnapshot(work_dir)

        assert_eq(
            snapshot1.diff(snapshot2),
            Difference(
                new_files={Path('file3.txt')},
                deleted_files={Path('file2.txt')},
            ),
            'Added and removed files',
        )

    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        (work_dir / 'file2.txt').write_text('world')
        snapshot1 = DirectorySnapshot(work_dir)
        (work_dir / 'file2.txt').write_text('new content')
        snapshot2 = DirectorySnapshot(work_dir)

        assert_eq(
            snapshot1.diff(snapshot2),
            Difference(
                changed_files={Path('file2.txt')},
            ),
            'Single changed file',
        )

    with working_directory() as work_dir:
        (work_dir / 'file1.txt').write_text('hello')
        (work_dir / 'file2.txt').write_text('world')
        os.utime((work_dir / 'file2.txt'), (1, 1))
        snapshot1 = DirectorySnapshot(work_dir)
        (work_dir / 'file2.txt').write_text('blurp')
        os.utime((work_dir / 'file2.txt'), (1, 1))
        snapshot2 = DirectorySnapshot(work_dir)

        assert_eq(
            snapshot1.diff(snapshot2),
            Difference(
                changed_files={Path('file2.txt')},
            ),
            'Changed content',
        )
