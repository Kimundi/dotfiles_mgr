#!/usr/bin/env python3

import json
from argparse import ArgumentParser
from pathlib import Path


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--home",
        type=Path,
        help="Path to home directory with dotfiles",
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

    home: Path = args.home
    dotfiles_repo: str = args.dotfiles_repo
    dotfiles_branch: str | None = args.dotfiles_branch

    # Prepare dotfiles dir
    dotfiles_cfg_path = home / ".dotfiles"
    dotfiles_cfg_path.mkdir(exist_ok=True)

    # Store config and continue next bootstrap phase
    bootstrap_json = {
        "mgr_checkout": str(Path(__file__).parent.resolve()),
    }
    (dotfiles_cfg_path / "bootstrap.json").write_text(
        json.dumps(bootstrap_json, indent=4)
    )


if __name__ == "__main__":
    main()
