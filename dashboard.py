import logging
import os
import time

from PIL import Image, ImageDraw
from blocks import (
    add_calendar_block,
    add_local_image,
    add_weather_block,
    draw_stock,
    draw_room_temperature,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    # Create the blank image
    logging.info("Create base image")
    img = Image.new("RGB", (1872, 1404), color=(255, 255, 255))

    logging.info("Adding local image")
    img = add_local_image(img, "local/yuyu.jpg", (1150, 180))

    logging.info("Create image draw")
    draw = ImageDraw.Draw(img)

    logging.info("Adding calendar")
    add_calendar_block(draw, (80, 50))
    # Call the new function
    add_weather_block(draw, 580, (23.157, 113.264), "广州市白云区")
    add_weather_block(draw, 980, (46.3162, 129.5546), "黑龙江依兰县")

    # img = retrieve_and_paste_image(
    #     img,
    #     "https://webquotepic.eastmoney.com/GetPic.aspx?nid=1.000001&imageType=r",
    #     (1250, 80),
    # )

    # img = add_rtsp_capture(img, "rtsp://admin:123456@10.0.0.210/video2", (50, 500))
    draw_stock(draw, (80, 460))
    draw_room_temperature(draw, (80, 700))

    # Save the image
    OUTPUT_PATH = "output/dashboard.jpg"
    img.save(OUTPUT_PATH)

    logging.info("Sending to epaper display")
    rc = os.system(f"eframe {OUTPUT_PATH} fill")
    if rc != 0:
        logging.error(rc)
        time.sleep(5)
        rc2 = os.system(f"eframe {OUTPUT_PATH} fill")
    logging.info("Sent to epaper display")
