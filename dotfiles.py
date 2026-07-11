#!/usr/bin/env python3


from argparse import ArgumentParser
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--home",
        type=Path,
        help="Path to home directory with dotfiles",
        required=True,
    )
    args = parser.parse_args()

    home: Path = args.home.resolve()

    print(home)


if __name__ == "__main__":
    main()
