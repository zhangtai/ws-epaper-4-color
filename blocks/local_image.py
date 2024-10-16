import logging

from PIL import Image


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def add_local_image(
    base_image: Image.Image, local_image_path: str, position: tuple[int, int]
) -> Image.Image:
    local_image = Image.open(local_image_path)

    # Ensure the local image has an alpha channel
    if local_image.mode != "RGBA":
        local_image = local_image.convert("RGBA")

    base_image.paste(local_image, position, local_image)
    return base_image
