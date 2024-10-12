#!/usr/bin/python
# -*- coding:utf-8 -*-
import argparse
import io
import sys
import os
from pillow_heif import register_heif_opener
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in0e
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def resize_and_crop(image_path, target_width=600, target_height=400):
    register_heif_opener()
    with Image.open(image_path) as img:
        # Calculate aspect ratios
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height

        if img_ratio > target_ratio:
            # Image is wider, scale based on height
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # Image is taller, scale based on width
            new_width = target_width
            new_height = int(new_width / img_ratio)

        # Resize the image
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Calculate cropping box
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height

        # Crop the image
        img = img.crop((left, top, right, bottom))

        # Convert to RGB mode if it's not already (BMP doesn't support RGBA)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Convert to BMP in memory
        bmp_data = io.BytesIO()
        img.save(bmp_data, format="BMP")
        return img


def main():
    parser = argparse.ArgumentParser(description="Resize and crop an image to 600x400")
    parser.add_argument("-i", "--image", required=True, help="Path to the input image")
    args = parser.parse_args()
    bitmap = resize_and_crop(args.image)
    logging.info("Init")
    epd.init()
    logging.info("Clear")
    epd.Clear()
    logging.info("Display")
    epd.display(epd.getbuffer(bitmap))


if __name__ == "__main__":
    epd = epd4in0e.EPD()   
    logging.info("init and Clear")
    try:
        main()
    
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd4in0e.epdconfig.module_exit(cleanup=True)
        exit()
    logging.info("Goto Sleep...")
    epd.sleep()
