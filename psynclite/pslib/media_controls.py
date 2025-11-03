import subprocess
from .data import COLORS
from .notifications import log_notification
from .helpers import log

def _handle_media_error(e: Exception):
    print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
    print(f"{COLORS['yellow']}Maybe no media player is active?{COLORS['reset']}")
    log(f"Media error: {e}", 1, False)

def vol_inc() -> None:
    """Increase volume by 5% with help of pactl"""
    try:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '+5%'])
        volume = subprocess.getoutput("pactl get-sink-volume @DEFAULT_SINK@ | grep 'Volume:' | awk '{print $5}'")
        log_notification('Sound', f'Volume increase: {volume}', 'low')
        log("Volume increased", 0, False)
    except Exception as e:
        _handle_media_error(e)
    

def vol_dec() -> None:
    """Decrease volume by 5% with help of pactl"""
    try:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '-5%'])
        volume = subprocess.getoutput("pactl get-sink-volume @DEFAULT_SINK@ | grep 'Volume:' | awk '{print $5}'")
        log_notification('Sound', f'Volume decrease: {volume}', 'low')
        log("Volume decreased", 0, False)
    except Exception as e:
        _handle_media_error(e)

def duration_minsec() -> None:
    """Get duration in minutes and seconds"""
    try:
        microseconds = int(subprocess.getoutput(
            "playerctl metadata --player io.bassi.Amberol | grep 'length' | awk '{print $3}'"
        ))
        seconds = microseconds // 1000000
        print(f"{seconds // 60}:{seconds % 60:02d}")
        log("Duration in minutes and seconds", 0, False)
    except Exception as e:
        _handle_media_error(e)
    

def duration_sec() -> None:
    """Get duration in seconds"""
    try:
        microseconds = int(subprocess.getoutput(
            "playerctl metadata --player io.bassi.Amberol | grep 'length' | awk '{print $3}'"
        ))
        print(microseconds // 1000000)
        log("Duration in seconds", 0, False)
    except Exception as e:
        _handle_media_error(e)
    

def position_minsec() -> None:
    """Get position in minutes and seconds of current media"""
    try:
        microseconds = int(subprocess.getoutput("playerctl metadata --format '{{ position }}'"))
        seconds = microseconds // 1000000
        print(f"{seconds // 60}:{seconds % 60:02d}")
        log("Position in minutes and seconds", 0, False)
    except Exception as e:
        _handle_media_error(e)
    

def position_sec() -> None:
    """Get position in seconds of current media"""
    try:
        microseconds = int(subprocess.getoutput("playerctl metadata --format '{{ position }}'"))
        print(microseconds // 1000000)
        log("Position in seconds", 0, False)
    except Exception as e:
        _handle_media_error(e)
    

def playpause() -> None:
    """Toggle play/pause of current media"""
    try:
        subprocess.run(['playerctl', 'play-pause'])
        log("Play/Pause", 0, False)
    except Exception as e:
        _handle_media_error(e)
    

def playernext() -> None:
    """Skip to next media"""
    try:
        subprocess.run(['playerctl', 'next'])
        log("Next", 0, False)
    except Exception as e:
        _handle_media_error(e)
    

def playerprevious() -> None:
    """Skip to previous media"""
    try:
        subprocess.run(['playerctl', 'previous'])
        log("Previous", 0, False)
    except Exception as e:
        _handle_media_error(e)
    
