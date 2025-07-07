import subprocess
import os
import random
from .data import COLORS
from .notifications import log_notification
from .ai_module import load_ai_model
from .helpers import log

def verison():
    ver = subprocess.getoutput('pacman -Q psynclite')
    print(ver)

def system():
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
    except Exception as e:
        print(f"Error occurred while fetching system information: {e}")
        log("Error getting system information", 1, False)
    log("System information fetched successfully", 0, False)

def pacman_pkg():
    """Fetch package information using pacman"""
    try:
        subprocess.run(['pacman', '-Qq'])
    except Exception as e:
        print(f"Error occurred while fetching package information: {e}")
        log("Error getting package information", 1, False)
    log("Package information fetched successfully", 0, False)

def wlogout():
    """Open the logout menu"""
    try:
        os.execvp('wlogout', [
            'wlogout', '-m', '100', '-b', '6', '-c', '0', '-r', '0',
            '-c', os.path.expanduser('~/.config/wlogout/style_3.css'),
            '--protocol', 'layer-shell'
        ])
    except Exception as e:
        print(f"Error starting wlogout: {e}")
        log("Error starting wlogout", 1, False)
    log("wlogout started successfully", 0, False)

def toggleWaybar():
    """Toggle the waybar (on/off)"""
    try:
        if subprocess.run(['pgrep', '-x', 'waybar']).returncode == 0:
            subprocess.run(['pkill', '-x', 'waybar'])
        else:
            subprocess.Popen(['waybar'])
    except Exception as e:
        print(f"Error toggling waybar: {e}")
        log("Error toggling waybar", 1, False)
    log("Waybar toggled successfully", 0, False)

def bri_inc():
    """Increase brightness by 5%"""
    try:
        subprocess.run(['brightnessctl', 's', '5%+'])
        brightness = subprocess.getoutput("brightnessctl | awk -F'[()%]' '/Current brightness/{print $2}'")
        log_notification('Brightness', f'Brightness increase: {brightness}', 'low')
    except Exception as e:
        print(f"Error increasing brightness: {e}")
        log("Error increasing brightness", 1, False)
    log("Brightness increased successfully", 0, False)

def bri_dec():
    """Decrease brightness by 5%"""
    try:
        subprocess.run(['brightnessctl', 's', '5%-'])
        brightness = subprocess.getoutput("brightnessctl | awk -F'[()%]' '/Current brightness/{print $2}'")
        log_notification('Brightness', f'Brightness decrease: {brightness}', 'low')
    except Exception as e:
        print(f"Error decreasing brightness: {e}")
        log("Error decreasing brightness", 1, False)
    log("Brightness decreased successfully", 0, False)

def wallpaper():
    """Set a random wallpaper using swww"""
    try:
        image_dir = os.path.expanduser('~/Images')
        random_image = random.randint(1, 372)
        subprocess.run(['swww', 'img', '-t', 'grow', '--transition-step', '90',
                   os.path.join(image_dir, f"{random_image}.jpg")])
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        log("Error setting wallpaper", 1, False)
    log("Wallpaper set successfully", 0, False)

def printscreen():
    """Take a screenshot using grimblast"""
    try:
        subprocess.run(['grimblast', 'copysave', 'area'])
        subprocess.run(['notify-send', '-u', 'low', 'Grimblas screenshot', 'Screenshot captured'])
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        log("Error taking screenshot", 1, False)
    log("Screenshot taken successfully", 0, False)
