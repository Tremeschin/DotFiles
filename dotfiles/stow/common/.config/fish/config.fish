if status is-interactive
    set fish_greeting "Saba 🐟"

    # https://starship.rs/
    if type -q starship
        starship init fish | source
    else
        echo "Missing starship"
    end

    # https://crates.io/crates/zoxide
    if type -q zoxide
        zoxide init --cmd cd fish | source
    else
        echo "Missing zoxide"
    end

    # Automatically source python venvs
    function autoenv --on-variable PWD
        source .venv/bin/activate.fish 2> /dev/null
    end

    autoenv
end
