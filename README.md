# Usage

```sh
curl https://raw.githubusercontent.com/Kimundi/dotfiles_mgr/main/bootstrap.py -o bootstrap_dotfiles.py \
    && python3 bootstrap_dotfiles.py \
    --mgr-repo "git@github.com:Kimundi/dotfiles_mgr.git" \
    --dotfiles-repo "git@github.com:Kimundi/dotfiles2.git" \
    --home ~ \
    && rm bootstrap_dotfiles.py
```
