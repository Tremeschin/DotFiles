if status is-interactive
    set fish_greeting "Saba 🐟"

    # https://starship.rs/
    if type -q starship
        starship init fish | source
    end

    # https://crates.io/crates/zoxide
    if type -q zoxide
        zoxide init --cmd cd fish | source
    end
end
