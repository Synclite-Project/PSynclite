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

The full list of options for PSynclite:

| Options | Description |
| --- | --- |
| **Synclite is the main control system** | --- |
| `-h` `--help` | Displays a message about all possible options |
| **System and its properties** | --- |
| `-sp` `--system-prop` | *[fastfetch](https://github.com/fastfetch-cli/fastfetch)* alternative + fastfetch |
| `-pp` `--pac-pkg` | Display installed pacman packages |
| `-wo` `--wlogout` | Open wlogout menu with style 3 |
| `-bu` `--backup` | Make backup paths system |
| `-snh` `--show-notifyhistory` | Show notification history |
| **Volume and Brightness Control** | --- |
| `-vi` `--vol-inc` | Increament volume in 5% |
| `-vd` `--vol-dec` | Decreament volume in 5% |
| `-bi` `--bri-inc` | Increament brightness in 5% |
| `-bd` `--bri-dec` | Increament brightness in 5% |
| **Media and System Control** | --- |
| `-mpp` `--media-pp` | Manage media - play\pause |
| `-mpn` `--media-pn` | Manage media - next song |
| `-mppr` `--media-ppr` | Manage media - previous song |
| `-wp` `--wallpaper` | Set random wallpaper from ~/Images |
| `-ps` `--printscreen` | Make screen shot |
| **AI and its properties** | --- |
| `"any request"` | Make request to AI with curent model |
| `-am` `--ai-model` | Set AI model |
| `-agk` `--ai-get-key` | Set AI API key |
