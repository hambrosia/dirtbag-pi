"""DirtBag Pi is an internet-connected garden and plant monitor.
 """

import manager.schedule_manager as schedule_manager
import manager.request_manager as request_manager
import manager.sensor_manager as sensor_manager

def main() -> None:
    """Start scheduler"""
    schedule_manager.on_startup()

if __name__ == "__main__":
    main()
