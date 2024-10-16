import datetime
import logging
from PIL import ImageDraw
from lunarcalendar import Converter

from .fonts import fonts


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

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
def get_lunar_date() -> tuple[str, str]:
    today = datetime.datetime.now()
    lunar_date = Converter.Solar2Lunar(today)

    lunar_month = chinese_numbers[lunar_date.month] + "月"
    lunar_day = chinese_numbers[lunar_date.day]

    return lunar_month, lunar_day


def add_calendar_block(draw: ImageDraw.Draw):
    logging.info("Drawing date block start")
    # lunar data
    lunar_month, lunar_day = get_lunar_date()

    # Get current date info in Chinese
    now = datetime.datetime.now()
    weekday_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekday_map[now.weekday()]
    month = f"{now.month}月"
    day = f"{now.day}"

    # Draw the left side
    draw.text((100, 50), weekday, font=fonts.large, fill=(255, 0, 0))
    draw.text((300, 50), month, font=fonts.large, fill=(192, 192, 192))

    draw.text((100, 150), day, font=fonts.x_large, fill=(0, 0, 0))

    # Lunar date vertically
    lunar_date_str = f"{lunar_month}\n{lunar_day}"
    draw.text((350, 230), lunar_date_str, font=fonts.medium, fill=(0, 0, 0), spacing=10)
    logging.info("Drawing date block completed")
