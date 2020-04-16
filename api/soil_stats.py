def get_column_average(soil_readings: list, column: str) -> float:
    sum = 0
    for row in soil_readings:
        sum += row[column]
    avg = sum / len(soil_readings)
    return avg

