import requests
import logging

from .fonts import fonts

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# WMO Weather Codes and Descriptions
wmo_weather_codes = {
    0: "晴",  # Clear sky
    1: "大部分晴",  # Mainly clear
    2: "局部多云",  # Partly cloudy
    3: "阴天",  # Overcast
    45: "有雾",  # Fog
    48: "沉积雾",  # Depositing rime fog
    51: "毛毛雨: 小",  # Drizzle: Light
    53: "毛毛雨: 中等",  # Drizzle: Moderate
    55: "毛毛雨: 大",  # Drizzle: Dense intensity
    56: "冻毛毛雨: 小",  # Freezing Drizzle: Light
    57: "冻毛毛雨: 大",  # Freezing Drizzle: Dense
    61: "小雨",  # Rain: Slight
    63: "中雨",  # Rain: Moderate
    65: "大雨",  # Rain: Heavy intensity
    66: "冻雨: 小",  # Freezing Rain: Light
    67: "冻雨: 大",  # Freezing Rain: Heavy intensity
    71: "小雪",  # Snow fall: Slight
    73: "中雪",  # Snow fall: Moderate
    75: "大雪",  # Snow fall: Heavy intensity
    77: "雪粒",  # Snow grains
    80: "小阵雨",  # Rain showers: Slight
    81: "中阵雨",  # Rain showers: Moderate
    82: "大阵雨",  # Rain showers: Violent
    85: "小阵雪",  # Snow showers: Slight
    86: "大阵雪",  # Snow showers: Heavy
    95: "雷暴: 小",  # Thunderstorm: Slight
    96: "雷暴: 中等",  # Thunderstorm: Moderate
    99: "雷暴伴有冰雹",  # Thunderstorm with hail
}


# Fetch weather data from the Open-Meteo API
def get_weather_data(coordinates: tuple[float, float]):
    logging.info(f"Getting weather for {coordinates}")
    weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&current_weather=true&daily=temperature_2m_max,temperature_2m_min"
    response = requests.get(weather_api_url)
    if response.status_code == 200:
        data = response.json()
        current_temp = data["current_weather"]["temperature"]
        condition = data["current_weather"]["weathercode"]
        max_temp = data["daily"]["temperature_2m_max"][0]
        min_temp = data["daily"]["temperature_2m_min"][0]
        return current_temp, max_temp, min_temp, condition
    else:
        return None


def add_weather_block(draw, start_x, coordinates, location_name):
    logging.info(f"Drawing weather block for {location_name}")
    draw.text((start_x, 50), location_name, font=fonts.small, fill=(0, 0, 0))

    current_temp, max_temp, min_temp, condition_code = get_weather_data(coordinates)

    # Current temperature
    draw.text(
        (start_x, 50), f"{int(current_temp)}°", font=fonts.x_large, fill=(0, 0, 0)
    )

    # Weather condition (icon placeholder and description)
    condition_text = wmo_weather_codes.get(condition_code, "Unknown")
    draw.text((start_x, 280), condition_text, font=fonts.medium, fill=(0, 0, 0))

    # Min/Max temperatures
    draw.text(
        (start_x, 350),
        f"最高 {int(max_temp)}° 最低 {int(min_temp)}°",
        font=fonts.small,
        fill=(0, 0, 0),
    )
    logging.info(f"Draw weather block for {location_name} completed")
