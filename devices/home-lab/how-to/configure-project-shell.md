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

If Delete moves the cursor or does nothing, add these lines at the end of `~/.zshrc`. They bind the terminal's Delete sequence to forward deletion in both Zsh insert keymaps.

```zsh
zmodload zsh/terminfo
for keymap in emacs viins; do
  bindkey -M "$keymap" $'\e[3~' delete-char
  if [[ -n ${terminfo[kdch1]} ]]; then
    bindkey -M "$keymap" "$terminfo[kdch1]" delete-char
  fi
done
unset keymap
```

## Start Zsh in new terminals

Add this near the top of `~/.bashrc`, before Bash-only prompt setup. For an account that already has a Zsh handoff, keep one block and use its existing fallback variable.

```bash
if [[ $- == *i* && ${KEEP_BASH:-} != 1 && -z ${BASH_EXECUTION_STRING:-} &&
      -t 0 && -t 1 && -x "$HOME/.nix-profile/bin/zsh" ]]; then
	exec "$HOME/.nix-profile/bin/zsh"
fi
```

This starts Zsh only for interactive terminal sessions without a supplied command. The account's login shell stays Bash. Codex runs SSH setup commands through an interactive login shell, so checking `$-` alone is insufficient. `BASH_EXECUTION_STRING` preserves commands supplied with `-c`, and `-t` requires terminal input and output.

To bypass the example handoff, run `KEEP_BASH=1 bash -i`. For an existing handoff, use the variable named in your `.bashrc`. To revert the handoff, remove the block or restore your `.bashrc` backup.

## Verify command execution and Codex access

On home-lab, run these checks as the account whose startup files you changed.

```bash
bash -n ~/.bashrc
bash -lic 'printf "command survived\n"' </dev/null
```

The syntax check must pass, and the login-shell check must print `command survived`. Bash may also report that job control is unavailable without a terminal. If the expected text is missing, fix the handoff before continuing.

Open a fresh terminal and run `print -r -- "$ZSH_VERSION"` to confirm that terminal sessions still start Zsh. In the Mac Codex app, reconnect to home-lab and open an existing remote chat. Confirm that the host connects and the chat loads.

If Codex reports `SSH websocket open timed out`, check the handoff even when ordinary SSH works. Replacing Bash with Zsh before the supplied command runs can cause this timeout. A successful `codex remote-control start` or relay health check does not verify the Mac app's SSH connection.

## Verify a project flake

Open a new terminal and run `print -r -- "$ZSH_VERSION"`. Check that the Oh My Posh prompt appears, then enter a trusted project with a `flake.nix` and an `.envrc` containing `use flake`.

If direnv blocks the project, review its `.envrc` and run `direnv allow` from the project root. The approval belongs to the current account. Wait for the build or download on first use, then run `print -r -- "$IN_NIX_SHELL"` and check a tool version provided by the flake. Leave the project to unload its environment.

If Bash opens in a new login terminal, check that its Bash login startup file sources `~/.bashrc`. If Zsh opens but the flake never loads, run `direnv status` in the project root to check which `.envrc` it found and whether approval is pending.

## Fix stale characters after Backspace in Rex

Use this workaround if Backspace removes a character from the command in Rex but leaves it visible on screen. Type `echo abc`, press Backspace once, then press Enter. If Rex still shows `echo abc` before Enter but prints `ab`, the edit worked and the screen failed to redraw. Check that `echo "$TERM"` prints `xterm-rex`.

Rex's terminal description advertises shortcuts for inserting and deleting characters on screen. A per-account override disables those shortcuts so Zsh redraws the edited text. The workaround was verified in a fresh Rex terminal on home-lab with Oh My Posh and a project flake active.

Run this on home-lab as the affected account. It uses the system's Rex terminal description and stops if the account already has an override. Review or back up an existing override before replacing it.

```bash
(
  set -eu
  for entry in "$HOME/.terminfo/x/xterm-rex" "$HOME/.terminfo/78/xterm-rex"; do
    if [ -e "$entry" ] || [ -L "$entry" ]; then
      printf 'Existing override: %s\n' "$entry" >&2
      exit 1
    fi
  done

  source_file=$(mktemp)
  trap 'rm -f "$source_file"' EXIT
  infocmp -x -1 -A /usr/share/terminfo xterm-rex > "$source_file"
  sed -E -i 's/^([[:space:]]*)(dch1?|ich1?)=.*/\1\2@,/' "$source_file"
  tic -x -o "$HOME/.terminfo" "$source_file"
)
```

Open a fresh Rex terminal or run `exec zsh`. Repeat the `echo abc` check. The line should show `echo ab` before Enter, and the command should print `ab`.

To roll back, run `infocmp xterm-rex | head -n 1` to find the active entry. Move the newly installed `xterm-rex` file out of `~/.terminfo` and start a fresh shell to use the system entry again.
