import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from os.path import expanduser


def ocr_process_image(url):
    try:
        image = Image.open(url)
        image.filter(ImageFilter.SHARPEN)
        return pytesseract.image_to_string(image, lang='eng')
    except IOError:
        return None


def isOcrable(address):
    try:
        homefolder = expanduser("~")
        base = '/serverdata/'
        address = homefolder + base + address
        image = Image.open(address)
        if image:
            return True
            # image.close()
    except IOError:
        return False
