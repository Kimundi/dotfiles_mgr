#!/usr/bin/env python3

import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--home",
        type=Path,
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
    parser.add_argument(
        "--mgr-path",
        type=Path,
        help="Local branch to check mgr out into",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Continue without asking for confirmation",
    )
    args = parser.parse_args()

    home: Path = args.home.resolve()
    mgr_repo: str = args.mgr_repo
    mgr_path: Path | None = args.mgr_path
    dotfiles_repo: str = args.dotfiles_repo
    dotfiles_branch: str | None = args.dotfiles_branch

    # Check that git and ssh keys are configured
    has_gitconfig = (Path.home() / ".gitconfig").exists()
    has_ssh_key = len(list((Path.home() / ".ssh").glob("*.pub"))) > 0

    if not has_gitconfig:
        print("Set up your local git config first (user and email)")
        sys.exit(1)

    if not has_ssh_key:
        print("Set up your git keys for github first")
        sys.exit(1)

    # Check out and update mgr repo
    if not mgr_path:
        mgr_path = home / ".dotfiles" / "mgr_repo"
    mgr_path = mgr_path.resolve()

    print("Boostrap config:")
    print(f"  Target HOME dir:      {home}")
    print(f"  Mgr checkout path:    {mgr_path}")
    print(f"  Mgr repo URL:         {mgr_repo}")
    print(f"  Dotfiles repo URL:    {dotfiles_repo}")
    print(f"  Dotfiles repo branch: {dotfiles_branch or '<default>'}")
    print()

    if not args.yes:
        input("Continue?")

    if not mgr_path.exists():
        print("Create initial clone of mgr...")
        mgr_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", mgr_repo, mgr_path.name],
            check=True,
            cwd=mgr_path.parent,
        )

    print("Update mgr...")
    subprocess.run(
        ["git", "pull", "--ff-only"],
        check=True,
        cwd=mgr_path,
    )

    # Run updater from repo
    update_cmd = [
        sys.executable,
        mgr_path / "update_mgr.py",
        "--home",
        str(home),
        "--dotfiles-repo",
        str(dotfiles_repo),
    ]
    if dotfiles_branch:
        update_cmd += ["--dotfiles-branch", dotfiles_branch]
    subprocess.run(
        update_cmd,
        check=True,
    )


if __name__ == "__main__":
    main()
