# Omarchy without a permanently attached monitor

Researched 2026-11-07 against upstream documentation and source. No remote desktop software or headless boot has been tested on the HP. Hardware details remain [user-reported](../../reference/inventory.md).

## Recommendation

Keep Omarchy's desktop available, establish SSH first, then trial Sunshine on the HP with Moonlight on the Mac. This is the first candidate for a responsive shared desktop. Try `hypr-rdp` next if clipboard integration, resizing, and desktop work matter more than streaming smoothness. Keep a monitor and keyboard available for installation and recovery; a permanently connected monitor is not inherently required.

This is a proposal, not a change to the accepted access setup. All upcoming HP work stays in the [preparation checklist](../preparation.md). Existing [private access choices](../../.okf/decisions/home-lab/private-development.md) still apply.

There are two different needs. SSH lets builds and agents run without a graphical login. Remote desktop lets the Mac show and control Linux applications, but adds a running desktop, screen capture, encoding, and client decoding. For terminal work, local Mac applications with SSH remain the simpler route. Full remote desktop earns its extra setup when we want the actual Omarchy environment, Linux GUI applications, or the same desktop at a physical monitor and on the Mac.

## Options worth considering

| Option | Fit for this Mac-to-HP setup | Main qualification |
|---|---|---|
| SSH and tmux | Baseline for coding, maintenance, and persistent jobs | Does not show the Omarchy desktop. Existing [setup guide](../setup.md) owns this recipe. |
| Sunshine host and Moonlight Mac client | First trial for smooth full-desktop streaming | Capture, Intel encoding, keyboard shortcuts, lock screen, and disconnected-display behavior need a real trial. |
| Native `hypr-rdp` and a Mac RDP client | Promising desktop-focused alternative | Separate project, not ordinary xrdp. Version compatibility and authentication need checking. |
| WayVNC and a VNC viewer | Direct screen sharing; useful fallback | Viewer authentication, shortcuts, and responsiveness vary. |
| WayVNC and noVNC in a browser | Convenient occasional access without installing a Mac viewer | Browser and macOS shortcuts can block Omarchy shortcuts. |
| Gliff | Interesting for another Hyprland client | Upstream currently requires Hyprland at both ends, so it does not fit a native macOS client. |
| RustDesk | Possible experiment later | Its own docs still describe experimental Wayland support and no Wayland login-screen access. |

### Sunshine and Moonlight

Omarchy documents `omarchy install service sunshine` to make an Omarchy machine a streaming host. Moonlight has a native macOS client. Sunshine supports Intel hardware encoding and Wayland capture, so a dedicated NVIDIA GPU is not a prerequisite. The HP's actual driver and encoder availability must still be checked. [Omarchy gaming manual](https://github.com/omacom/omarchy/blob/master/manual/26-gaming.md), [Moonlight downloads](https://moonlight-stream.org/), [Sunshine capability tables](https://docs.lizardbyte.dev/projects/sunshine/latest/)

Sunshine's Desktop entry streams an existing desktop; it does not create a fresh user login. Its published SSH headless instructions target X11 and NVIDIA, so they are not a ready-made recipe for this Intel Hyprland machine. [Sunshine getting started](https://docs.lizardbyte.dev/projects/sunshine/master/md_docs_2getting__started.html)

The Omarchy helper currently enables a user service, adds desktop autostart, and allows streaming traffic from private LAN address ranges plus `tailscale0` if that interface exists. This is broader than the notebook's private-only access baseline. Review its effective rules during setup. A reported service-alias failure also remains relevant because the inspected script still uses `systemctl --user enable --now sunshine`; verify the installed package's real unit before relying on the helper. [Installer source](https://raw.githubusercontent.com/omacom/omarchy/master/bin/omarchy-install-service-sunshine), [upstream issue #13877](https://github.com/omacom/omarchy/issues/13877)

### Native RDP is now a real alternative

`hypr-rdp` directly supports Hyprland, H.264 with VA-API or software encoding, audio, and clipboard transfer. It requires Hyprland 0.54 or newer and normally creates a virtual output sized for its client. Its README requires running under the same user as the desktop. Configure authentication explicitly: omitting credentials in its default authentication mode permits unauthenticated access. Default binding is loopback, which suits an SSH tunnel for an initial trial. AVC444, useful for colored text fidelity, is experimental and currently software-encoded. [hypr-rdp README](https://github.com/MuNeNICK/hypr-rdp)

DigitalOcean's Omarchy marketplace image uses this server and lists Windows App on macOS as a client. That demonstrates a documented cloud integration, not support already installed by the bare-metal Omarchy ISO. Its cloud image includes its own software rendering, services, firewall configuration, and shortcut adaptations. Do not copy the cloud image's public-port setup onto the HP. [DigitalOcean image documentation](https://docs.digitalocean.com/products/marketplace/catalog/omarchy/)

Installing ordinary `xrdp` alone is a different proposition. Its normal desktop backend uses Xorg; it can also proxy VNC. An xrdp-to-WayVNC bridge adds components compared with direct WayVNC or native `hypr-rdp`. [xrdp README](https://github.com/neutrinolabs/xrdp)

### VNC, browser access, and other tools

WayVNC attaches to an existing Wayland session and supports headless sessions. It defaults to localhost and recommends SSH tunneling. The built-in macOS Screen Sharing client's legacy authentication needs compatibility settings in WayVNC; avoid treating a VNC password as modern transport encryption. Test a suitable viewer over SSH instead. [WayVNC README](https://github.com/any1/wayvnc)

The community `second-state/omarchy-remote` packages WayVNC plus noVNC and offers private Tailscale browser access. Its normal desktop services start with the graphical session, and its troubleshooting guide warns about the login dependency after reboot. The README also documents macOS and browser shortcut interception. Its optional additional-user mode changes accounts, firewall rules, and screen locking, so it deserves separate review rather than adopting the whole tool for a simple viewer. This is a community project, not proof of an upstream default or a tested HP setup. [Project README](https://github.com/second-state/omarchy-remote)

Gliff is an Omacom project with SSH transport, full-color text rendering, clipboard sharing, and a private virtual-output mode. It still requires a running remote Hyprland session and Hyprland on the client. Its README and release packaging information are evolving, so check the installed release rather than assuming availability from a newer announcement. [Gliff README](https://github.com/omacom/gliff)

RustDesk's Linux docs still call Wayland experimental and require X11 for remote access to the login screen. That makes it a poor first choice for unattended Omarchy recovery. [RustDesk Linux documentation](https://rustdesk.com/docs/en/client/linux/)

## What headless actually requires

A machine can boot and accept SSH while no graphical session is running. Streaming that desktop requires more: a compositor, an output to capture, a remote server with the correct session environment, and a usable input path.

Current Hyprland documentation says it creates `HEADLESS-0` at 1920×1080, 60 Hz when starting without display outputs, and lists Sunshine and WayVNC as supported access servers. It also stresses launching the server within the compositor's environment. This supports trying a software virtual display before buying a dummy plug. The documentation is current upstream behavior, not proof that the Omarchy version installed on the HP includes it. [Hyprland virtual GPU guide](https://wiki.hypr.land/configuring/extra/virtual-gpu/)

A display dummy plug makes the GPU detect a monitor. It cannot log in, start a missing compositor, unlock storage, repair networking, or show a failed boot over the network. Do not purchase one until an actual capture/output problem justifies it. Likewise, user-service persistence alone does not establish a usable graphical session after reboot.

The existing unencrypted-boot preference removes one possible boot prompt. It does not resolve graphical login, lock-screen control, or reconnection. Keep local screen locking enabled. If desktop autologin or a separate unattended graphical session is needed, review that as an explicit setup choice. Keep coding under the planned unprivileged account; controlling the maintenance desktop gives the remote operator that desktop's authority.

## How responsive should we expect it to be?

These are engineering expectations, not HP measurements:

| Connection | Expected experience |
|---|---|
| HP on Ethernet, Mac on Ethernet, hardware encoding | Best prospect for a desktop that feels close to local for ordinary work. Direct display still has fewer processing steps. |
| HP on Ethernet, Mac on good nearby Wi-Fi | Often suitable for desktop work; interference and delay variation can cause visible hitches. |
| Remote internet connection | Browsing and occasional GUI use may be comfortable, but typing, dragging, and scrolling increasingly expose network delay. |
| Congested Wi-Fi, lossy mobile link, or relay path | More likely to feel uneven; use SSH and local Mac applications when interaction suffers. |

Tailscale says direct connections generally offer lower delay and higher throughput than relay connections. Check the actual path with `tailscale status` and `tailscale ping <host>`; being on a tailnet does not guarantee a direct connection. [Tailscale connection types](https://tailscale.com/docs/reference/connection-types)

Network round-trip delay is only part of input-to-picture delay. Capture, encoding, decoding, frame queues, and displays also contribute. At 60 Hz a frame lasts about 16.7 ms; a measured 50 ms round trip consumes roughly three frame intervals before those other costs. Moonlight's statistics separate several components, but its docs warn that the overlay does not measure every source of delay. Start a trial at 1920×1080 and 60 FPS before trying Retina-sized resolutions. [Moonlight performance statistics](https://github.com/moonlight-stream/moonlight-docs/wiki/Frequently-Asked-Questions)

For coding, judge small colored text and shortcut handling as well as frame rate. A smooth video stream can still be less pleasant than a locally rendered editor. Test representative work rather than infer quality from gaming claims.

## Evidence needed before removing the monitor

Use the single [preparation checklist](../preparation.md) to schedule a trial. During that trial, record the installed versions, actual capture and encoder path, and client settings. Compare SSH, Sunshine/Moonlight, and optionally `hypr-rdp` with ordinary typing, scrolling, workspace changes, copy/paste, and a browser.

Repeat with the display unplugged, after a cold boot, after locking, and after a client disconnect. Check whether switching between local and remote use preserves the intended session and resolution. Test SSH recovery when the graphical server is stopped. A brief Wi-Fi and off-site comparison should record network path and delay alongside subjective usability.

If these checks pass, rack the HP without a permanent display and keep a monitor available for recovery. If direct Omarchy desktop use becomes the daily workflow and feels better locally, use a monitor's spare input or an appropriate KVM. Ordinary remote desktop does not replace access to firmware, bootloader recovery, or a machine whose network is down.
