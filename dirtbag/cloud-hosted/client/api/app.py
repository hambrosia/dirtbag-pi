"""DirtBag Pi is an internet-connected garden and plant monitor.
 """

import manager.schedule_manager as schedule_manager
import manager.request_manager as request_manager
import manager.sensor_manager as sensor_manager

def main() -> None:
    soil_moisture = sensor_manager.get_soil_moisture()
    response = request_manager.post_reading()
    print(response)


if __name__ == "__main__":
    main()
