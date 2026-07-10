#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
from pathlib import Path


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--home",
        help="Path to home directory to bootstrap dotfiles into (can be a test directory for a dry-run)",
        required=True,
    )
    parser.add_argument(
        "--mgr-repo",
        help="Git repo of dotfiles manager",
        required=True,
    )
    parser.add_argument(
        "--dotfiles-repo",
        help="Git repo of dotfiles",
        required=True,
    )
    parser.add_argument(
        "--dotfiles-branch",
        help="Branch of dotfiles repo",
    )
    args = parser.parse_args()

    home: str = args.home
    mgr_repo: str = args.mgr_repo
    dotfiles_repo: str = args.dotfiles_repo
    dotfiles_branch: str | None = args.dotfiles_branch

    has_gitconfig = (Path.home() / ".gitconfig").exists()
    has_ssh_key = len(list((Path.home() / ".ssh").glob("*.pub"))) > 0

    if not has_gitconfig:
        print("Set up your local git config first (user and email)")
        sys.exit(1)

    if not has_ssh_key:
        print("Set up your git keys for github first")
        sys.exit(1)


if __name__ == "__main__":
    main()
