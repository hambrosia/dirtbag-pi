def get_average_soil_moisture(soil_readings: list) -> double:
    sum_soil = 0
    for row in readings_last_24_hr:
        sum_soil += row['soilmoisture']
    avg_soil_raw = sum_soil / len(readings_last_24_hr)
    avg_soil_percent = sensor_manager.get_soil_moisture_percent(avg_soil_raw)
    return avg_soil_percent
