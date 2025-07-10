import subprocess
from .data import COLORS
from .notifications import log_notification
from .helpers import log

def vol_inc():
    """Increase volume by 5% with help of pactl"""
    try:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '+5%'])
        volume = subprocess.getoutput("pactl get-sink-volume @DEFAULT_SINK@ | grep 'Volume:' | awk '{print $5}'")
        log_notification('Sound', f'Volume increase: {volume}', 'low')
    except Exception:
        log("Error volume increase", 1, True, "Error volume increase")
    log("Volume increased", 0, False)

def vol_dec():
    """Decrease volume by 5% with help of pactl"""
    try:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '-5%'])
        volume = subprocess.getoutput("pactl get-sink-volume @DEFAULT_SINK@ | grep 'Volume:' | awk '{print $5}'")
        log_notification('Sound', f'Volume decrease: {volume}', 'low')
    except Exception:
        log("Error volume decrease", 1, True, "Error volume decrease")
    log("Volume decreased", 0, False)

def duration_minsec():
    """Get duration in minutes and seconds"""
    try:
        microseconds = int(subprocess.getoutput(
            "playerctl metadata --player io.bassi.Amberol | grep 'length' | awk '{print $3}'"
        ))
        seconds = microseconds // 1000000
        print(f"{seconds // 60}:{seconds % 60:02d}")
    except ValueError as e:
        print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
        print(f"{COLORS['yellow']}Maybe you not use media player?{COLORS['reset']}")
        log("Maybe not used media player", 1, False)
    log("Duration in minutes and seconds", 0, False)

def duration_sec():
    """Get duration in seconds"""
    try:
        microseconds = int(subprocess.getoutput(
            "playerctl metadata --player io.bassi.Amberol | grep 'length' | awk '{print $3}'"
        ))
        print(microseconds // 1000000)
    except ValueError as e:
        print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
        print(f"{COLORS['yellow']}Maybe you not use media player?{COLORS['reset']}")
        log("Maybe not used media player", 1, False)
    log("Duration in seconds", 0, False)

def position_minsec():
    """Get position in minutes and seconds of current media"""
    try:
        microseconds = int(subprocess.getoutput("playerctl metadata --format '{{ position }}'"))
        seconds = microseconds // 1000000
        print(f"{seconds // 60}:{seconds % 60:02d}")
    except ValueError as e:
        print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
        print(f"{COLORS['yellow']}Maybe you not use media player?{COLORS['reset']}")
        log("Maybe not used media player", 1, False)
    log("Position in minutes and seconds", 0, False)

def position_sec():
    """Get position in seconds of current media"""
    try:
        microseconds = int(subprocess.getoutput("playerctl metadata --format '{{ position }}'"))
        print(microseconds // 1000000)
    except ValueError as e:
        print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
        print(f"{COLORS['yellow']}Maybe you not use media player?{COLORS['reset']}")
        log("Maybe not used media player", 1, False)
    log("Position in seconds", 0, False)

def playpause():
    """Toggle play/pause of current media"""
    try:
        subprocess.run(['playerctl', 'play-pause'])
    except ValueError as e:
        print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
        print(f"{COLORS['yellow']}Maybe you not use media player?{COLORS['reset']}")
        log("Maybe not used media player", 1, False)
    log("Play/Pause", 0, False)

def playernext():
    """Skip to next media"""
    try:
        subprocess.run(['playerctl', 'next'])
    except ValueError as e:
        print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
        print(f"{COLORS['yellow']}Maybe you not use media player?{COLORS['reset']}")
        log("Maybe not used media player", 1, False)
    log("Next", 0, False)

def playerprevious():
    """Skip to previous media"""
    try:
        subprocess.run(['playerctl', 'previous'])
    except ValueError as e:
        print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
        print(f"{COLORS['yellow']}Maybe you not use media player?{COLORS['reset']}")
        log("Maybe not used media player", 1, False)
    log("Previous", 0, False)
