import subprocess
from .data import COLORS
from .notifications import log_notification
from .helpers import log

# Используем %any, чтобы управлять последним активным плеером, а не конкретным
PLAYER_ARGS = ["playerctl", "--player=%any,chromium,firefox"] 

def _handle_media_error(e: Exception):
    print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
    print(f"{COLORS['yellow']}Maybe no media player is active?{COLORS['reset']}")
    log(f"Media error: {e}", 1, False)

def _get_metadata(fmt):
    """Helper to get metadata safely"""
    cmd = PLAYER_ARGS + ["metadata", "--format", fmt]
    return subprocess.check_output(cmd, text=True).strip()

def vol_inc() -> None:
    """Increase volume by 5%"""
    try:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '+5%'])
        # Оптимизация: получаем громкость одной командой без лишних пайпов
        volume = subprocess.getoutput("pactl get-sink-volume @DEFAULT_SINK@ | head -n1 | cut -d / -f 2 | tr -d ' '")
        log_notification('Sound', f'Volume: {volume}', 'low')
        log("Volume increased", 0, False)
    except Exception as e:
        _handle_media_error(e)

def vol_dec() -> None:
    """Decrease volume by 5%"""
    try:
        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '-5%'])
        volume = subprocess.getoutput("pactl get-sink-volume @DEFAULT_SINK@ | head -n1 | cut -d / -f 2 | tr -d ' '")
        log_notification('Sound', f'Volume: {volume}', 'low')
        log("Volume decreased", 0, False)
    except Exception as e:
        _handle_media_error(e)

def duration_minsec() -> None:
    try:
        # Получаем длину в микросекундах (mpris:length)
        micro = int(_get_metadata("{{ mpris:length }}"))
        seconds = micro // 1000000
        print(f"{seconds // 60}:{seconds % 60:02d}")
        log("Duration (min:sec) fetched", 0, False)
    except Exception as e:
        _handle_media_error(e)

def duration_sec() -> None:
    try:
        micro = int(_get_metadata("{{ mpris:length }}"))
        print(micro // 1000000)
        log("Duration (sec) fetched", 0, False)
    except Exception as e:
        _handle_media_error(e)

def position_minsec() -> None:
    try:
        micro = int(_get_metadata("{{ position }}"))
        seconds = micro // 1000000
        print(f"{seconds // 60}:{seconds % 60:02d}")
        log("Position (min:sec) fetched", 0, False)
    except Exception as e:
        _handle_media_error(e)

def position_sec() -> None:
    try:
        micro = int(_get_metadata("{{ position }}"))
        print(micro // 1000000)
        log("Position (sec) fetched", 0, False)
    except Exception as e:
        _handle_media_error(e)

def playpause() -> None:
    try:
        subprocess.run(PLAYER_ARGS + ['play-pause'])
        log("Play/Pause toggled", 0, False)
    except Exception as e:
        _handle_media_error(e)

def playernext() -> None:
    try:
        subprocess.run(PLAYER_ARGS + ['next'])
        log("Next track", 0, False)
    except Exception as e:
        _handle_media_error(e)

def playerprevious() -> None:
    try:
        subprocess.run(PLAYER_ARGS + ['previous'])
        log("Previous track", 0, False)
    except Exception as e:
        _handle_media_error(e)