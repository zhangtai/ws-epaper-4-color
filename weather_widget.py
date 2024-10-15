import datetime
import os
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont
from lunarcalendar import Converter


# Fetch weather data from the Open-Meteo API
def get_weather_data(lat, lon):
    weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min"
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


FONT_PATH = "/usr/local/fonts/Noto_Sans_SC/NotoSansSC-Regular.ttf"
x_large_font = ImageFont.truetype(FONT_PATH, 200)
large_font = ImageFont.truetype(FONT_PATH, 100)
medium_font = ImageFont.truetype(FONT_PATH, 50)
small_font = ImageFont.truetype(FONT_PATH, 40)

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


# Chinese number mapping
chinese_numbers = {
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
    10: "十",
    11: "十一",
    12: "十二",
    13: "十三",
    14: "十四",
    15: "十五",
    16: "十六",
    17: "十七",
    18: "十八",
    19: "十九",
    20: "二十",
    21: "二十一",
    22: "二十二",
    23: "二十三",
    24: "二十四",
    25: "二十五",
    26: "二十六",
    27: "二十七",
    28: "二十八",
    29: "二十九",
    30: "三十",
}


# Get Lunar date and convert to Chinese characters
def get_lunar_date():
    today = datetime.datetime.now()
    lunar_date = Converter.Solar2Lunar(today)

    lunar_month = chinese_numbers[lunar_date.month] + "月"  # Convert month to Chinese
    lunar_day = chinese_numbers[lunar_date.day]  # Convert day to Chinese

    return lunar_month, lunar_day


def add_weather_block(draw, start_x, lat, lon, location_name):
    draw.text((start_x, 50), location_name, font=small_font, fill=(0, 0, 0))

    current_temp, max_temp, min_temp, condition_code = get_weather_data(lat, lon)

    # Current temperature
    draw.text((start_x, 50), f"{int(current_temp)}°", font=x_large_font, fill=(0, 0, 0))

    # Weather condition (icon placeholder and description)
    condition_text = wmo_weather_codes.get(condition_code, "Unknown")
    draw.text((start_x, 280), condition_text, font=medium_font, fill=(0, 0, 0))

    # Min/Max temperatures
    draw.text(
        (start_x, 350),
        f"最高 {int(max_temp)}° 最低 {int(min_temp)}°",
        font=small_font,
        fill=(0, 0, 0),
    )


def retrieve_and_paste_image(base_image, url, position):
    response = requests.get(url)
    response.raise_for_status()
    retrieved_image = Image.open(BytesIO(response.content))

    # Ensure the retrieved image has an alpha channel
    if retrieved_image.mode != "RGBA":
        retrieved_image = retrieved_image.convert("RGBA")

    base_image.paste(retrieved_image, position, retrieved_image)
    return base_image


def read_and_paste_local_image(base_image, local_image_path, position):
    local_image = Image.open(local_image_path)

    # Ensure the local image has an alpha channel
    if local_image.mode != "RGBA":
        local_image = local_image.convert("RGBA")

    base_image.paste(local_image, position, local_image)
    return base_image


# Create the lock screen image
def add_calendar_block(draw):
    # lunar data
    lunar_month, lunar_day = get_lunar_date()

    # Get current date info in Chinese
    now = datetime.datetime.now()
    weekday_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekday_map[now.weekday()]
    month = f"{now.month}月"
    day = f"{now.day}"

    # Draw the left side
    draw.text((100, 50), weekday, font=large_font, fill=(255, 0, 0))
    draw.text((300, 50), month, font=large_font, fill=(192, 192, 192))

    draw.text((100, 150), day, font=x_large_font, fill=(0, 0, 0))

    # Lunar date vertically
    lunar_date_str = f"{lunar_month}\n{lunar_day}"
    draw.text((350, 230), lunar_date_str, font=medium_font, fill=(0, 0, 0), spacing=10)


if __name__ == "__main__":
    # Create the blank image
    img = Image.new("RGB", (1872, 1404), color=(255, 255, 255))
    img = read_and_paste_local_image(img, "local/yuyu.jpg", (1150, 180))
    draw = ImageDraw.Draw(img)

    add_calendar_block(draw)
    # Call the new function
    add_weather_block(draw, 580, 23.157, 113.264, "广州市白云区")
    add_weather_block(draw, 980, 46.3162, 129.5546, "黑龙江依兰县")

    # img = retrieve_and_paste_image(
    #     img,
    #     "https://webquotepic.eastmoney.com/GetPic.aspx?nid=1.000001&imageType=r",
    #     (1250, 80),
    # )

    # Save the image
    OUTPUT_PATH = "output/weather.jpg"
    img.save(OUTPUT_PATH)
    os.system(f"eframe {OUTPUT_PATH} fill")
