import logging
from .config import COLORS

def log(meslog, code, notify, mes=''):
    """Functions message logging"""
    from .notifications import log_notification
    if code == 0 and notify == True:
        log_notification('Info',mes, 'normal')
        logging.info(meslog)
    elif code == 0 and notify == False:
        logging.info(meslog)
    elif code == 1 and notify == True:
        log_notification('Error', mes, 'critical')
        logging.exception(meslog)
    elif code == 1 and notify == False:
        logging.exception(meslog)
    exit(0)

def helpSynclite():
    """Show help message for PSynclite"""
    help_text = f"""

    {COLORS['yellow']}----------- Synclite is the main control system ----------{COLORS['reset']}

    {COLORS['green']}-h --help         			               Show this message{COLORS['reset']}

    {COLORS['yellow']}---------- System and its properties ----------{COLORS['reset']}

    {COLORS['cyan']}-sp --system-prop{COLORS['reset']}         Display base system indicators
    {COLORS['cyan']}-pp --pac-pkg{COLORS['reset']}             Display Installed pacman packages
    {COLORS['cyan']}-wo --wlogout{COLORS['reset']}             Open wlogout menu
    {COLORS['cyan']}-bu --backup{COLORS['reset']}              Backup system

    {COLORS['cyan']}-snh --show-notifyhistory{COLORS['reset']} Show notification history.

    {COLORS['yellow']}------- Volume and Brightness Control ---------{COLORS['reset']}

    {COLORS['cyan']}-V inc{COLORS['reset']}                    Increment volume (+5%)
    {COLORS['cyan']}   dec{COLORS['reset']}                    Decrement volume (-5%)
    {COLORS['cyan']}-B inc{COLORS['reset']}                    Increment Brightness (+5%)
    {COLORS['cyan']}   dec{COLORS['reset']}                    Decrement Brightness (-5%)

    {COLORS['yellow']}--------- Media and System Control ------------{COLORS['reset']}

    {COLORS['cyan']}-M player toggle{COLORS['reset']}          Control media (play/pause)
    {COLORS['cyan']}-M player next{COLORS['reset']}            Next song
    {COLORS['cyan']}-M player previous{COLORS['reset']}        Previous song
    {COLORS['cyan']}-M duration minsec{COLORS['reset']}        Player's duration in min:sec
    {COLORS['cyan']}-M duration sec{COLORS['reset']}           Player's duration in seconds
    {COLORS['cyan']}-M position minsec{COLORS['reset']}        Player's position in min:sec
    {COLORS['cyan']}-M position sec{COLORS['reset']}           Player's position in seconds

    {COLORS['cyan']}-wp --wallpaper{COLORS['reset']}           Set random wallpaper
    {COLORS['cyan']}-ps --printscreen{COLORS['reset']}         Make screen shot

    {COLORS['yellow']}---------- AI and it`s properties -------------{COLORS['reset']}

    {COLORS['cyan']}"any request"{COLORS['reset']}             Request to AI
    {COLORS['cyan']}-am --ai-mod{COLORS['reset']}              Change the AI model

    """
    print(help_text)
