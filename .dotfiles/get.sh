#!/bin/bash
git clone https://github.com/Tremeschin/DotFiles ~/.dotfiles
cd ~/.dotfiles

# Trick: Repo at ~/.dotfiles, root at home
git config core.worktree $HOME
git checkout -f main
