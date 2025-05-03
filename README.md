# PSynclite
A utility for managing programs and packages in the Arch Linux environment with WM Hyprland

## Installing

Clone the git repository and build using makepkg:

```sh
git clone https://github.com/Synclite-Project/PSynclite
cd PSynclite/psynclite/pslib
makepkg -si
```

## Info

Executing the command:

```sh
pscli [option] [argument 1] [argument 2]
```

Basic commands (1st level):

| Command | Description |
| --- | --- |
| `-h`, `--help` | Show help menu |
| `-sp`, `--system-prop` | Display system properties |
| `-pp`, `--pac-pkg` | Display pacman package information |
| `-wo`, `--wlogout` | Start wlogout menu |
| `-bu`, `--backup` | Utility for backup files and directories |
| `-wp`, `--wallpaper` | Set random wallpaper |
| `-tw`, `--tog-waybar` | Toggle waybar (on/off) |
| `-ps`, `--printscreen` | Make screenshot |
| `-snh`, `--show-notifyhistory` | Display a notification history from pscli |

Commands with second-level parameters:

| Command | Second-level parameter | Description |
| --- | --- | --- |
| `-V` | `inc`, `dec` | Increase or decrease volume by 5% |
| `-B` | `inc`, `dec` | Increase or decrease brightness by 5% |
| `-M` | `duration`, `position`, `player` | Defines the duration of the player. Defines the player's position. Controls the player |
| `-Ai` | `model`, `get-key` | Configuring AI |

Command with third-level parameters:

| Command | Second-level parameter | Third-level parameter | Description |
| --- | --- | --- | --- |
| `-M` | `duration` | `minsec` | Determines the duration of the current track in format min:sec |
| --- | --- | `seconds` | ... in format seconds |
| --- | `position` | `minsec` | Determines the position of the current track in format min:sec |
| --- | --- | `seconds` | ... in format seconds |
| --- | `player` | `toggle` | Toggle player (play/pause) |
| --- | --- | `previous` | Switches to the previous track |
| --- | --- | `next` | Switches to the next track |
