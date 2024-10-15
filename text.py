import os
from PIL import Image, ImageDraw, ImageFont

# Set the image size
width, height = 1872, 1404

# Create a blank white image
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Load a TrueType or OpenType font file
# You can use a system font, or provide the path to a .ttf file
try:
    font = ImageFont.truetype("/usr/local/fonts/Noto_Sans_SC/NotoSansSC-Regular.ttf", 200)  # Replace 'arial.ttf' with an appropriate font if necessary
except IOError:
    # If the system doesn't have arial, use a default font
    font = ImageFont.load_default()

# Find the maximum font size that fits the entire image with "Hello World!"
text = "周一\n10月14"
font_size = 10
while True:
    # Create a new font with the current size
    temp_font = ImageFont.truetype("/usr/local/fonts/Noto_Sans_SC/NotoSansSC-Regular.ttf", font_size)
    text_width, text_height = draw.textbbox((0, 0), text, font=temp_font)[2:]  # Use textbbox instead of textsize

    # Break if the text dimensions exceed the image size
    if text_width > width or text_height > height:
        break

    # Otherwise, increment the font size and continue
    font = temp_font
    font_size += 10

# Calculate the position to center the text
x = (width - text_width) / 2
y = (height - text_height) / 2

# Draw the text onto the image
draw.text((x, y), text, fill="black", font=font)

# Save the image
OUTPUT_PATH = "output/text.png"
image.save(OUTPUT_PATH)
os.system(f'eframe {OUTPUT_PATH} fill')

