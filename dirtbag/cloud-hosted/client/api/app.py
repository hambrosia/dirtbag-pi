"""DirtBag Pi is an internet-connected garden and plant monitor.
 """

import manager.schedule_manager as schedule_manager


def main() -> None:
    """Start scheduler"""
    schedule_manager.on_startup()

if __name__ == "__main__":
    main()
