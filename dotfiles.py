#!/usr/bin/env python3


import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

DOTFILES_DIR = ".dotfiles2"


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--home",
        type=Path,
        help="Path to home directory with dotfiles",
        required=True,
    )
    sub_parsers = parser.add_subparsers(required=True, dest="cmd")
    sub_parsers.add_parser(
        "git",
        add_help=False,
        help="Execute git command on dotfiles",
    )

    args, extra_args = parser.parse_known_args()

    home: Path = args.home.resolve()
    dotfiles_cfg = home / DOTFILES_DIR

    if args.cmd == "git":
        out = subprocess.run(
            [
                "git",
                "--git-dir",
                str(dotfiles_cfg / "dotfiles_git_dir"),
                "--work-tree",
                str(home),
                *extra_args,
            ],
            check=False,
        )
        sys.exit(out.returncode)


if __name__ == "__main__":
    main()
