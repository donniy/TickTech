import pytesseract
import requests
import cv2
from PIL import Image
from os.path import expanduser


def ocr_process_image(url):
    try:
        image = cv2.imread(url)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return pytesseract.image_to_string(gray, lang='eng', nice=1)
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
            image.close()
    except IOError:
        return False
