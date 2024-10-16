import logging

from PIL import Image
import cv2

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def add_rtsp_capture(
    img: Image.Image, rtsp_url: str, position: tuple[int, int]
) -> Image.Image:
    logging.info("Opening camera")
    cap = cv2.VideoCapture(rtsp_url)

    # Check if the connection was successful
    if not cap.isOpened():
        logging.error("Error: Could not open video stream.")
        exit()

    # Read one frame from the stream
    ret, frame = cap.read()

    if ret:
        logging.info("Captured image, converting to PIL image")
        # Convert the OpenCV frame (BGR format) to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the numpy array to a Pillow Image
        pil_image = Image.fromarray(frame_rgb)
        pil_image_resize = pil_image.resize(
            (int(pil_image.width / 1), int(pil_image.height / 1))
        )

        # Paste the OpenCV image onto the Pillow image (you can specify position)
        img.paste(pil_image_resize, position)
        logging.info("Image with pasted OpenCV frame saved")
    else:
        logging.error("Error: Could not read a frame from the stream.")

    # Release the capture object
    cap.release()
    logging.info("Releasing camera")
    return img
