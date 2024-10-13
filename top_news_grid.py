import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your News API key here
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Fetch top 6 global news headlines
def get_top_news(api_key, count=6):
    logging.info("Fetching top news headlines...")
    # url = f'https://newsapi.org/v2/everything?q=openai&apiKey={api_key}&language=zh&pageSize={count}&sortBy=publishedAt'
    url = f'https://newsapi.org/v2/top-headlines?apiKey={api_key}&language=en&pageSize={count}&sortBy=publishedAt'
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Successfully fetched news articles.")
        return response.json()['articles']
    else:
        logging.error(f"Failed to fetch news articles. Status code: {response.status_code}")
        raise Exception("Failed to fetch news articles")

# Download an image from a URL
def download_image(url):
    if not url:
        logging.warning("No URL provided for image. Using placeholder image.")
        return Image.new('RGB', (500, 300), color=(200, 200, 200))  # Placeholder image
    logging.info(f"Downloading image from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Image downloaded successfully.")
        return Image.open(BytesIO(response.content))
    else:
        logging.warning(f"Failed to download image from {url}. Status code: {response.status_code}. Using placeholder image.")
        return Image.new('RGB', (500, 300), color=(200, 200, 200))  # Placeholder image

# Create a 2x3 grid image for news
def create_news_grid(news_articles, output_image_path):
    logging.info("Creating news grid image...")
    # Define image dimensions
    grid_width, grid_height = 1872, 1404
    single_width, single_height = grid_width // 2, grid_height // 3

    # Create a blank image
    grid_image = Image.new('RGB', (grid_width, grid_height), color=(255, 255, 255))

    # Load a font
    try:
        font = ImageFont.truetype("/usr/local/fonts/Noto_Sans_SC/NotoSansSC-Regular.ttf", 45)
    except IOError:
        logging.warning("Failed to load 'arial.ttf'. Using default font.")
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(grid_image)

    # Loop through the articles and create each grid item
    for idx, article in enumerate(news_articles):
        # Download the image for the news article
        img = download_image(article['urlToImage'])
        if img is not None:
            # Resize the image to fit in a single grid cell
            img = img.resize((single_width, single_height))

            # Calculate position for the image
            x = (idx % 2) * single_width
            y = (idx // 2) * single_height

            # Paste the image onto the grid
            grid_image.paste(img, (x, y))

            # Draw the headline (overlay at bottom of image)
            headline = article['title']
            wrapped_headline = textwrap.fill(headline, width=45)
            text_x = x + 10
            text_y = y + single_height - (55 * len(wrapped_headline.splitlines())) - 10

            # Ensure the text stays within the image boundary
            if text_y < y:
                text_y = y + 10

            # Draw a semi-transparent white rectangle as the background for the text
            text_width = single_width - 20
            text_height = 55 * len(wrapped_headline.splitlines())
            overlay = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 218))
            grid_image.paste(overlay, (text_x, text_y), overlay)

            # Draw the text on top of the background
            for line in wrapped_headline.splitlines():
                draw.text((text_x, text_y), line, fill="black", font=font)
                text_y += 55

    # Save the final grid image
    grid_image.save(output_image_path)
    logging.info(f"News grid image saved as {output_image_path}")

# Main function to fetch news and create the grid image
def main():
    try:
        # Get the top news articles
        news_articles = get_top_news(NEWS_API_KEY)
        
        # Create the grid image
        output_image_path = 'output/top_6_global_news.jpg'
        create_news_grid(news_articles, output_image_path)
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
