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

    # Someone else's skill issue
    export PIP_BREAK_SYSTEM_PACKAGES=1

    # https://wiki.archlinux.org/title/Docker#Rootless_Docker_daemon
    set -x DOCKER_HOST unix://$XDG_RUNTIME_DIR/docker.sock

end
