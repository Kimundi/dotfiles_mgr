#!/usr/bin/env python3

import shlex
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from textwrap import dedent

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

    home: Path = args.home.resolve()
    dotfiles_repo: str = args.dotfiles_repo
    dotfiles_branch: str | None = args.dotfiles_branch

    # Prepare dotfiles dir
    dotfiles_cfg_path = home / DOTFILES_DIR
    dotfiles_cfg_path.mkdir(exist_ok=True)

    dotfiles_git_dir = dotfiles_cfg_path / "dotfiles_git_dir"

    if not dotfiles_git_dir.exists():
        print("Create initial clone of dotfiles...")
        dotfiles_git_dir.parent.mkdir(parents=True, exist_ok=True)

        clone_cmd = ["git", "clone", "--bare"]
        if dotfiles_branch:
            clone_cmd += ["--branch", dotfiles_branch]
        clone_cmd += [dotfiles_repo, str(dotfiles_git_dir)]
        # print(clone_cmd)
        subprocess.run(
            clone_cmd,
            check=True,
            cwd=home,
        )

        dotfiles_git_cmd_prefix = [
            "git",
            "--git-dir",
            str(dotfiles_git_dir),
            "--work-tree",
            str(home),
        ]
        # print(shlex.join(dotfiles_git_cmd_prefix))
        subprocess.run(
            dotfiles_git_cmd_prefix + ["reset"],
            check=True,
            cwd=home,
        )

    dotfiles_cmd = [
        "python3",
        str(SCRIPT_DIR / "dotfiles.py"),
        "--home",
        str(home),
    ]
    launcher = dedent(f"""\
        #!/usr/bin/env bash

        {shlex.join(dotfiles_cmd)} "$@"
    """)

    dotfiles_cli_path = home / "bin" / "dotfiles"
    dotfiles_cli_path.parent.mkdir(exist_ok=True)
    dotfiles_cli_path.write_text(launcher)
    subprocess.run(["chmod", "+x", str(dotfiles_cli_path)], check=True)

    print("Done!")
    print(f"Use this binary for further interactions: {dotfiles_cli_path}")


if __name__ == "__main__":
    main()
