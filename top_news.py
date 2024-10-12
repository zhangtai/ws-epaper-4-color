import os
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
from io import BytesIO
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up your API keys here
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Constants
IMAGE_WIDTH = 1872  # Swap width and height to ensure landscape orientation
IMAGE_HEIGHT = 1404
FONT_PATH = "/usr/share/fonts/NoticiaText/NoticiaText-Regular.ttf"  # Update this with the path to your font file

# Fetch top news from NewsAPI
def fetch_top_news():
    if not NEWS_API_KEY:
        logging.error("NEWS_API_KEY environment variable not set.")
        return []
    logging.info("Fetching top news articles...")
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_API_KEY}&pageSize=10"
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Successfully fetched top news articles.")
        return response.json().get("articles", [])
    else:
        logging.error(f"Failed to fetch news. Status code: {response.status_code}")
        return []

# Generate image with news list
def generate_news_image(news_list):
    logging.info("Generating news image...")
    # Create an empty white image
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load a font
    try:
        font_title = ImageFont.truetype(FONT_PATH, 28)
        font_desc = ImageFont.truetype(FONT_PATH, 20)
        logging.info("Fonts loaded successfully.")
    except IOError:
        logging.error("Font file not found at path: " + FONT_PATH)
        raise Exception("Font file not found at path: " + FONT_PATH)

    # Drawing configurations
    margin = 20
    x_offset = margin
    y_offset = margin
    image_box_width = 200
    text_width = IMAGE_WIDTH - image_box_width - 3 * margin

    for index, news in enumerate(news_list):
        logging.info(f"Processing news item {index + 1}...")
        if 'urlToImage' in news and news['urlToImage']:
            # Load news image
            try:
                news_image_response = requests.get(news['urlToImage'])
                news_image = Image.open(BytesIO(news_image_response.content))
                news_image = news_image.resize((image_box_width, image_box_width))
                img.paste(news_image, (x_offset, y_offset))
                logging.info(f"News image {index + 1} loaded and pasted successfully.")
            except Exception as e:
                logging.warning(f"Failed to load news image {index + 1}. Using placeholder. Error: {e}")
                # Placeholder if image load fails
                draw.rectangle([x_offset, y_offset, x_offset + image_box_width, y_offset + image_box_width], fill=(200, 200, 200))
        else:
            logging.warning(f"No image URL for news item {index + 1}. Using placeholder.")
            # Placeholder if no image is available
            draw.rectangle([x_offset, y_offset, x_offset + image_box_width, y_offset + image_box_width], fill=(200, 200, 200))

        # Draw title and description
        title = news.get('title', 'No Title')
        description = news.get('description', '') or 'No Description Available'

        # Draw title
        draw.text((x_offset + image_box_width + margin, y_offset), title, fill=(0, 0, 0), font=font_title)
        y_offset += font_title.getbbox(title)[3]

        # Wrap the description text
        description_lines = textwrap.wrap(description, width=140)

        # Draw description
        for line in description_lines:
            draw.text((x_offset + image_box_width + margin, y_offset), line, fill=(100, 100, 100), font=font_desc)
            y_offset += font_desc.getbbox(line)[3]

        # Add space before the next news item
        y_offset += margin * 2

        if y_offset > IMAGE_HEIGHT - margin:
            logging.info("Reached the end of the image. Stopping further news items.")
            break

    # Save the image
    img.save('output/top_news.png')
    logging.info("Image saved as 'top_news.png'.")

if __name__ == "__main__":
    # Fetch the top news articles
    news_list = fetch_top_news()
    if news_list:
        generate_news_image(news_list)
        logging.info("Image with top 10 news generated successfully!")
    else:
        logging.error("Failed to fetch news. Please check your API key and internet connection.")
