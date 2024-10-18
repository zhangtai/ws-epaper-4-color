import requests
from PIL import ImageDraw

from .fonts import fonts


def draw_stock(draw: ImageDraw, position: tuple[int, int]):
    response = requests.get("https://yunhq.sse.com.cn:32042/v1/sh1/snap/000001")
    results = response.json()

    stock_name = results["snap"][0]
    last_value = results["snap"][5]
    change = results["snap"][7]
    change_prefix = "↓" if change < 0 else "↑"

    draw.text(position, stock_name, font=fonts.medium, fill=(255, 0, 0))
    draw.text(
        (position[0] + 240, position[1]),
        f"{last_value:.0f}",
        font=fonts.medium,
        fill=(255, 0, 0),
    )
    draw.text(
        (position[0], position[1] + 50),
        f"{change_prefix}{change:.2f}%",
        font=fonts.large,
        fill=(255, 0, 0),
    )
