# PSynclite
A utility for managing programs and packages in the Arch Linux environment with WM Hyprland

## Installing

Clone the git repository and build using makepkg:

```sh
git clone git@github.com:<yourName>/<repo>.git
```

## Info

The full list of options for PSynclite:

| Options | Description |
| --- | --- |
| **Synclite is the main control system** | --- |
| `-h` `--help` | Displays a message about all possible options |
| `-i` `--init` | Initialization |
| **Dash and Widgets** | --- |
| `-od` `--open-dash` | Open system dash (if you have *[eww](https://github.com/elkowar/eww)*) |
| `-cd` `--close-dash` | Close system dash (if you have *[eww](https://github.com/elkowar/eww)*) |
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
| `-wp` `--wallpaper` | Set random wallpaper |
| `-ps` `--printscreen` | Make screen shot |
| `-bg` `--battery-guard` | Service for monitoring battery |
| **AI and its properties** | --- |
| `"any request"` | Make request to AI with curent model |
| **Optional funclions** | --- |
| `-T "any text"` | In development |
