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
        "--dotfiles-repo",
        help="Git repo of dotfiles",
        required=True,
    )
    args = parser.parse_args()

    home: Path = args.home.resolve()
    mgr_repo: str = args.mgr_repo
    dotfiles_repo: str = args.dotfiles_repo


if __name__ == "__main__":
    main()
