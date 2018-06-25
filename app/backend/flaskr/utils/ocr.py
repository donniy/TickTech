import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter


def process_image(url):
    print("Getting image")
    image = _get_image(url)
    print("got image")
    # image.convert('1')
    # image.filter(ImageFilter.GaussianBlur(2))
    image.filter(ImageFilter.SHARPEN)
    print("filtered")
    return pytesseract.image_to_string(image, lang='eng')


def _get_image(url):
    return Image.open(url)
