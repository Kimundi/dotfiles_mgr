#!/usr/bin/env python3

import json
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
    args = parser.parse_args()

    home: Path = args.home
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

    # Prepare dotfiles dir
    dotfiles_cfg_path = home / ".dotfiles"
    dotfiles_cfg_path.mkdir(exist_ok=True)

    # Check out and update mgr repo
    if not mgr_path:
        mgr_path = dotfiles_cfg_path / "mgr_repo"
    mgr_path = mgr_path.resolve()

    print("(Re)using the git checkout of the dotfile manager at:")
    print(mgr_path)
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

    # Store config and continue next bootstrap phase
    bootstrap_json = {
        "mgr_checkout": str(mgr_path),
    }
    (dotfiles_cfg_path / "bootstrap.json").write_text(
        json.dumps(bootstrap_json, indent=4)
    )


if __name__ == "__main__":
    main()
