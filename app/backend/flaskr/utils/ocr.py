import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO


def process_image(url):
    image = _get_image(url)
    #image.convert('1')
    image.filter(ImageFilter.GaussianBlur(2))
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image, lang='eng')


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))
