import subprocess
import os
import random
from .data import COLORS
from .notifications import log_notification
from .ai_module import load_ai_model
from .helpers import log

def version() -> None:
    ver = subprocess.getoutput('pacman -Q psynclite')
    print(ver)

def system() -> None:
    """Get system information

    Display system information on the screen:
        - Current OS
        - Current Static OS
        - Current GTK theme
        - Uptime
        - Window Manager
        - Current CPU usage
        - Current Memory usage
        - Current Disk usage
        - Local IP Address
        - Info swap file
        - Current AI model
        etc
    """
    output = []
    with open('/etc/os-release') as f:
        os_name = next(line.split('"')[1] for line in f if 'PRETTY_NAME' in line)
    try:
        uptime = subprocess.getoutput("uptime -p").replace("up ", "")
        acpi_output = subprocess.getoutput("acpi")
        volume = subprocess.getoutput("pactl get-sink-volume @DEFAULT_SINK@ | grep 'Volume:' | awk '{print $5}'")
        brightness = subprocess.getoutput("brightnessctl | awk -F'[()%]' '/Current brightness/{print $2}'")
        staticos = subprocess.getoutput("hostnamectl | grep 'Static hostname: ' | awk '{print $3}'")
        pacman_count = subprocess.getoutput("pacman -Qq | wc -l").strip()
        flatpak_count = subprocess.getoutput("flatpak list | wc -l").strip()
        theme = subprocess.getoutput("gsettings get org.gnome.desktop.interface gtk-theme").strip()

        output.append(f"{COLORS['yellow']}------ System -----{COLORS['reset']}\n")
        output.append(f"{COLORS['green']}Current OS: {COLORS['reset']}{os_name}")
        output.append(f"{COLORS['green']}Current Static OS: {COLORS['reset']}{staticos}")
        output.append(f"{COLORS['green']}Current GTK theme: {COLORS['reset']}{theme}")
        output.append(f"{COLORS['green']}Uptime: {COLORS['reset']}{uptime}")
        output.append(f"{COLORS['green']}Window Manager: {COLORS['reset']}{os.environ.get('XDG_CURRENT_DESKTOP', '')} (Wayland)")
        output.append(f"{COLORS['green']}Battery: {COLORS['reset']}{acpi_output.split(': ')[1] if acpi_output else 'Unknown'}")
        output.append(f"{COLORS['green']}Shell: {COLORS['reset']}{os.path.basename(os.getenv('SHELL', ''))}")
        output.append(f"{COLORS['green']}Local time: {COLORS['reset']}{subprocess.getoutput('date +%H:%M:%S')}")
        output.append(f"{COLORS['green']}Local IP: {COLORS['reset']}{subprocess.getoutput('ip route get 1 | awk \'{print $7}\'')}")
        output.append(f"\n{COLORS['green']}Volume: {COLORS['reset']}{volume}")
        output.append(f"{COLORS['green']}Brightness: {COLORS['reset']}{brightness}%")
        output.append(f"\n{COLORS['green']}Packages: {COLORS['reset']}{pacman_count} (pacman), {flatpak_count} (flatpak)")
        output.append(f"\n{COLORS['green']}Info swap file: {COLORS['reset']}")
        output.append(subprocess.getoutput('sudo swapon --show'))

        output.append(f"\n{COLORS['green']}Output fastfetch: {COLORS['reset']}")
        output.append(subprocess.getoutput('fastfetch --logo none'))

        output.append(f"{COLORS['yellow']}------ PSynclite -----{COLORS['reset']}\n")
        output.append(f"{COLORS['green']}Current AI model: {COLORS['reset']}{load_ai_model()}")

        print('\n'.join(output))
        log("System information fetched successfully", 0, False)
    except Exception as e:
        print(f"Error occurred while fetching system information: {e}")
        log("Error getting system information", 1, False)

def pacman_pkg() -> None:
    """Fetch package information using pacman"""
    try:
        subprocess.run(['pacman', '-Qq'])
        log("Package information fetched successfully", 0, False)
    except Exception as e:
        print(f"Error occurred while fetching package information: {e}")
        log("Error getting package information", 1, False)

def wlogout() -> None:
    """Open the logout menu"""
    try:
        os.execvp('wlogout', [
            'wlogout', '-m', '100', '-b', '6', '-c', '0', '-r', '0',
            '-c', os.path.expanduser('~/.config/wlogout/style_3.css'),
            '--protocol', 'layer-shell'
        ])
        log("wlogout started successfully", 0, False)
    except Exception as e:
        print(f"Error starting wlogout: {e}")
        log("Error starting wlogout", 1, False)

def toggleWaybar() -> None:
    """Toggle the waybar (on/off)"""
    try:
        if subprocess.run(['pgrep', '-x', 'waybar']).returncode == 0:
            subprocess.run(['pkill', '-x', 'waybar'])
        else:
            subprocess.Popen(['waybar'])
        log("Waybar toggled successfully", 0, False)
    except Exception as e:
        print(f"Error toggling waybar: {e}")
        log("Error toggling waybar", 1, False)

def bri_inc() -> None:
    """Increase brightness by 5%"""
    try:
        subprocess.run(['brightnessctl', 's', '5%+'])
        brightness = subprocess.getoutput("brightnessctl | awk -F'[()%]' '/Current brightness/{print $2}'")
        log_notification('Brightness', f'Brightness increase: {brightness}', 'low')
        log("Brightness increased successfully", 0, False)
    except Exception as e:
        print(f"Error increasing brightness: {e}")
        log("Error increasing brightness", 1, False)

def bri_dec() -> None:
    """Decrease brightness by 5%"""
    try:
        subprocess.run(['brightnessctl', 's', '5%-'])
        brightness = subprocess.getoutput("brightnessctl | awk -F'[()%]' '/Current brightness/{print $2}'")
        log_notification('Brightness', f'Brightness decrease: {brightness}', 'low')
        log("Brightness decreased successfully", 0, False)
    except Exception as e:
        print(f"Error decreasing brightness: {e}")
        log("Error decreasing brightness", 1, False)

def wallpaper() -> None:
    """Set a random wallpaper using swww"""
    try:
        image_dir = os.path.expanduser('~/Images')
        random_image = random.randint(1, 372)
        subprocess.run(['swww', 'img', '-t', 'wipe', '--transition-step', '90',
                   os.path.join(image_dir, f"{random_image}.jpg")])
        log("Wallpaper set successfully", 0, False)
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        log("Error setting wallpaper", 1, False)

def printscreen() -> None:
    """Take a screenshot using grimblast"""
    try:
        subprocess.run(['grimblast', 'copysave', 'area'])
        subprocess.run(['notify-send', '-u', 'low', 'Grimblas screenshot', 'Screenshot captured'])
        log("Screenshot taken successfully", 0, False)
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        log("Error taking screenshot", 1, False)

def ask_zen(type: str, text: str, title: str = "Synclite") -> bool:
    try:
        result = subprocess.run(
            ["zenity", f"--{type}", "--text", text, "--title", title], 
            capture_output=True,
            text=True,
            timeout=30)
        if type == "entry":
            return result.stdout.strip()
        else:
            return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    
def inc_productivity() -> None:
    killeww = ask_zen("question", "Kill eww?", "Synclite: increased productivity")
    if killeww:
        subprocess.run(["killall", "eww"])
    gifpaper = ask_zen("question", "Turn off animated wallpapers?", "Synclite: increased productivity")
    if gifpaper:
        wallpaper()
    
def chTheme():
    """Change Eww theme and optionally wallpaper"""
    try:
        file_path = os.path.expanduser('~/.config/psynclite/output.txt')
        dir_themes = os.path.expanduser('~/.config/eww/css/themes/')
        dir_images = os.path.expanduser('~/ImagesF')

        subprocess.run(['touch', file_path])

        subprocess.run([
            'kitty', 'sh', '-c',
            f'cd "{dir_themes}" && ls -1v | gum choose --header "Themes:" > "{file_path}"'
        ])

        if not os.path.exists(file_path):
            print(f"{COLORS['red']}Error: File not found!{COLORS['reset']}")
            log("Theme change failed: missing output.txt", 1, False)
            return 1

        with open(file_path, 'r') as f:
            result = f.read().strip()

        if not result:
            print(f"{COLORS['red']}Error: You haven't chosen a theme!{COLORS['reset']}")
            log("Theme change cancelled (no selection)", 1, False)
            return 1

        source_file = os.path.join(dir_themes, result)
        target_file = os.path.expanduser('~/.config/eww/css/colors.scss')

        if not os.path.exists(source_file):
            print(f"{COLORS['red']}Error: Theme file not found!{COLORS['reset']}")
            log(f"Theme file not found: {source_file}", 1, False)
            return 1

        subprocess.run(['cp', source_file, target_file])
        theme_name = result.removesuffix('.scss')

        if theme_name == 'default':
            wallpaper()
            log("Theme changed to default", 0, False)
            return 0

        wallpaper_path = os.path.join(dir_images, f"{theme_name}.jpg")
        if not os.path.exists(wallpaper_path):
            print(f"{COLORS['yellow']}Warning: Wallpaper not found for theme '{theme_name}'{COLORS['reset']}")
        else:
            subprocess.run([
                'swww', 'img', wallpaper_path,
                '-t', 'wipe', '--transition-step', '180', '--transition-angle', '45'
            ])

        log(f"Theme changed successfully to '{theme_name}'", 0, False)
        return 0

    except Exception as e:
        print(f"{COLORS['red']}Error changing theme: {e}{COLORS['reset']}")
        log(f"Error changing theme: {e}", 1, False)
        return 1