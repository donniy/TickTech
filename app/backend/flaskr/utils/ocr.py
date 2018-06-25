import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter


def ocr_process_image(url):
    image = Image.open(url)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image, lang='eng')
