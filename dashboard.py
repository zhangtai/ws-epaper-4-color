import os
from io import BytesIO

import requests
from PIL import Image, ImageDraw
from blocks import add_rtsp_capture, add_calendar_block, add_weather_block


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


if __name__ == "__main__":
    # Create the blank image
    img = Image.new("RGB", (1872, 1404), color=(255, 255, 255))
    img = read_and_paste_local_image(img, "local/yuyu.jpg", (1150, 180))
    draw = ImageDraw.Draw(img)

    add_calendar_block(draw)
    # Call the new function
    add_weather_block(draw, 580, (23.157, 113.264), "广州市白云区")
    add_weather_block(draw, 980, (46.3162, 129.5546), "黑龙江依兰县")

    # img = retrieve_and_paste_image(
    #     img,
    #     "https://webquotepic.eastmoney.com/GetPic.aspx?nid=1.000001&imageType=r",
    #     (1250, 80),
    # )

    img = add_rtsp_capture(img, "rtsp://admin:123456@10.0.0.210/video2", (50, 500))

    # Save the image
    OUTPUT_PATH = "output/weather.jpg"
    img.save(OUTPUT_PATH)
    os.system(f"eframe {OUTPUT_PATH} fill")
