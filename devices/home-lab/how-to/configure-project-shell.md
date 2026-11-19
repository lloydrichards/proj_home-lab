# Configure Zsh and project flakes

Set up Zsh, Oh My Posh, and direnv for one account on home-lab. Repeat the steps while signed in to each account that needs the setup. The Nix profile and startup files belong to the current account.

## Install the shell and prompt

From Bash on home-lab, check that `nix` and `direnv` are available, then install Zsh and Oh My Posh in the current account's Nix profile.

```bash
command -v nix direnv
nix profile add nixpkgs#zsh nixpkgs#oh-my-posh
```

Review the [Oh My Posh theme](https://github.com/lloydrichards/.config/blob/main/shell/ohmyposh/theme.toml) before saving it as `~/.config/ohmyposh/home-lab.toml`. If you already have a copy, use its path below.

Back up any existing `~/.zshrc` and `~/.bashrc` before editing. Add this to `~/.zshrc`. If you already initialize direnv or a prompt there, update the existing initialization so each runs once.

```zsh
[[ -r /usr/share/omarchy/default/bash/env-bootstrap ]] &&
  source /usr/share/omarchy/default/bash/env-bootstrap

typeset -U path
path=("$HOME/.nix-profile/bin" /nix/var/nix/profiles/default/bin "${path[@]}")

eval "$(direnv hook zsh)"
eval "$(oh-my-posh init zsh --config "$HOME/.config/ohmyposh/home-lab.toml")"
```

Run `~/.nix-profile/bin/zsh -i` to test the prompt. Type `exit` to return to Bash.

## Start Zsh in new terminals

Add this near the top of `~/.bashrc`, before Bash-only prompt setup. For an account that already has a Zsh handoff, keep one block and use its existing fallback variable.

```bash
if [[ $- == *i* && ${KEEP_BASH:-} != 1 && -x "$HOME/.nix-profile/bin/zsh" ]]; then
  exec "$HOME/.nix-profile/bin/zsh"
fi
```

This starts Zsh for interactive Bash sessions. The account's login shell stays Bash, and the handoff skips non-interactive SSH commands. To bypass the example handoff, run `KEEP_BASH=1 bash -i`. For an existing handoff, use the variable named in your `.bashrc`. To revert the handoff, remove the block or restore your `.bashrc` backup.

## Verify a project flake

Open a new terminal and run `print -r -- "$ZSH_VERSION"`. Check that the Oh My Posh prompt appears, then enter a trusted project with a `flake.nix` and an `.envrc` containing `use flake`.

If direnv blocks the project, review its `.envrc` and run `direnv allow` from the project root. The approval belongs to the current account. Wait for the build or download on first use, then run `print -r -- "$IN_NIX_SHELL"` and check a tool version provided by the flake. Leave the project to unload its environment.

If Bash opens in a new login terminal, check that its Bash login startup file sources `~/.bashrc`. If Zsh opens but the flake never loads, run `direnv status` in the project root to check which `.envrc` it found and whether approval is pending.
