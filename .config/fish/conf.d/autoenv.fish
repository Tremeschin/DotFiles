#!/bin/fish
# (c) Tremeschin, MIT License
# Automatically source cwd python venvs

function _autoenv --on-variable PWD
    status --is-command-substitution; and return
    source .venv/bin/activate.fish 2> /dev/null
end

_autoenv
