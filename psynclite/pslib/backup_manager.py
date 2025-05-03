import shutil
import os
import time
from .config import COLORS, CONFIG_DIR
from .helpers import log

def backup():
    """Backup utility in PSynclite for system"""
    print(f"\n{COLORS['yellow']}=== PSynclite Backup Utility ==={COLORS['reset']}")

    backup_dir = os.path.join(CONFIG_DIR, "backups", time.strftime("%Y-%m-%d_%H-%M-%S"))
    os.makedirs(backup_dir, exist_ok=True)

    try:
        paths_input = input(f"{COLORS['cyan']}Input paths to backup (space separated): {COLORS['reset']}")
        paths = [os.path.expanduser(p.strip()) for p in paths_input.split()]

        success = []
        errors = []

        for path in paths:
            try:
                    # Check exist path
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Path not found: {path}")

                dest = os.path.join(backup_dir, os.path.basename(path))

                    # Coping
                if os.path.isdir(path):
                    shutil.copytree(path, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(path, dest)

                success.append(f"{path} → {dest}")

            except Exception as e:
                errors.append(f"{path}: {str(e)}")

        print(f"\n{COLORS['green']}=== Backup Report ==={COLORS['reset']}")
        print(f"{COLORS['bold']}Backup location:{COLORS['reset']} {backup_dir}")

        if success:
            print(f"\n{COLORS['green']}Successfully copied:{COLORS['reset']}")
            for item in success:
                print(f"  • {item}")

        if errors:
            print(f"\n{COLORS['red']}Errors occurred:{COLORS['reset']}")
            for error in errors:
                print(f"  • {error}")

        print(f"\n{COLORS['cyan']}Backup {'completed successfully' if not errors else 'finished with errors'}{COLORS['reset']}")

    except KeyboardInterrupt:
        print(f"\n{COLORS['red']}Backup cancelled by user!{COLORS['reset']}")
        log("Backup cancelled by user", 1, False)
    except Exception as e:
        print(f"{COLORS['red']}Critical backup error: {str(e)}{COLORS['reset']}")
        log("Critical backup error", 1, True, "Backup is failed")
    log("Backup finished", 0, True, "Backup is completed")
