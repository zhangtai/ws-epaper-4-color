import logging
from io import BytesIO

import requests
from PIL import Image

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def add_web_image(
    base_image: Image.Image, url: str, position: tuple[int, int]
) -> Image.Image:
    logging.info(f"Getting image from {url}")
    response = requests.get(url)
    response.raise_for_status()
    retrieved_image = Image.open(BytesIO(response.content))

    # Ensure the retrieved image has an alpha channel
    if retrieved_image.mode != "RGBA":
        retrieved_image = retrieved_image.convert("RGBA")

    logging.info("Downloaded image, pasting to base image")
    base_image.paste(retrieved_image, position, retrieved_image)
    return base_image
