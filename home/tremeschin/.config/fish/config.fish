if status is-interactive
    set fish_greeting "Saba 🐟"

    set missing

    # https://starship.rs/
    if type -q starship
        starship init fish | source
    else
        set missing $missing starship
    end

    # https://crates.io/crates/zoxide
    if type -q zoxide
        zoxide init --cmd cd fish | source
    else
        set missing $missing zoxide
    end

    # https://crates.io/crates/bat
    if type -q bat
        function cat
            bat \
            --style plain \
            --paging=never \
            $argv
        end
    else
        set missing $missing bat
    end

    # https://crates.io/crates/ripgrep
    if type -q rg
        function grep
            rg $argv
        end
    else
        set missing $missing ripgrep
    end

    # https://crates.io/crates/eza
    if type -q exa
        function ls
            exa \
            --group-directories-first \
            --time-style=long-iso \
            --long \
            --header \
            --icons \
            $argv
        end
    else
        set missing $missing eza
    end

    # https://crates.io/crates/du-dust
    if type -q dust
        function du
            dust $argv
        end
    else
        set missing $missing dust
    end

    # https://crates.io/crates/fd
    if type -q fd
        function find
            fd \
            --hidden \
            --no-ignore \
            --absolute-path \
            --follow \
            $argv
        end
    else
        set missing $missing fd
    end

    # https://github.com/zyedidia/micro
    if type -q micro
        function nano
            micro $argv
        end
    else
        set missing $missing micro
    end

    if test -n "$missing"
        set_color brblack
        echo "Missing: yay -S $missing"
        set_color normal
    end


    # Someone else's skill issue
    export PIP_BREAK_SYSTEM_PACKAGES=1

    # https://wiki.archlinux.org/title/Docker#Rootless_Docker_daemon
    # set -x DOCKER_HOST unix://$XDG_RUNTIME_DIR/docker.sock

    # Disable annoying .python-history (https://stackoverflow.com/a/63653039)
    set -x PYTHONSTARTUP "$HOME/.config/python/startup.py"

end
