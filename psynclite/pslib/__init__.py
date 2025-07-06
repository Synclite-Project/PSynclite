import logging
from .ai_module import aimodel, aiapi, get_api_key
from .backup_manager import backup
from .helpers import helpSynclite, log
from .media_controls import vol_inc, vol_dec, playpause, playernext, playerprevious, duration_minsec, duration_sec, position_minsec, position_sec
from .system_utils import system, pacman_pkg, wlogout, toggleWaybar, bri_inc, bri_dec, wallpaper, printscreen, verison
from .notifications import show_notification_history
from .config import COLORS, LOG_FILE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s', handlers=[logging.FileHandler(LOG_FILE)])

__all__ = [
    "aimodel",
    "aiapi",
    "backup",
    "helpSynclite",
    "vol_inc",
    "vol_dec",
    "playpause",
    "playernext",
    "playerprevious",
    "duration_minsec",
    "duration_sec",
    "position_minsec",
    "position_sec",
    "system",
    "pacman_pkg",
    "wlogout",
    "toggleWaybar",
    "bri_inc",
    "bri_dec",
    "wallpaper",
    "printscreen",
    "show_notification_history",
    "COLORS",
    "log",
    "get_api_key",
    "version"
]
