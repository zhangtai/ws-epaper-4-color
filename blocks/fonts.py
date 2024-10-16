from PIL import ImageFont


class Fonts:
    def __init__(self, font_path):
        self.x_large = ImageFont.truetype(font_path, 200)
        self.large = ImageFont.truetype(font_path, 100)
        self.medium = ImageFont.truetype(font_path, 50)
        self.small = ImageFont.truetype(font_path, 40)


FONT_PATH = "/usr/local/fonts/Noto_Sans_SC/NotoSansSC-Regular.ttf"
fonts = Fonts(FONT_PATH)

