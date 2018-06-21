# import the necessary packages
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
import pytesseract
import argparse
import requests
import cv2
import os

def ocr_file(image_path):
    # load the example image and convert it to grayscale
    img = cv2.imread(image_path)
    #image = cv2.resize(img, (0,0), fx=2, fy=2) 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply gausian blur to remove noise
    gray = cv2.GaussianBlur(gray,(5,5),0)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # create textfile, load the image as a PIL/Pillow image, apply OCR, 
    # write to created textfile,and then delete the temporary file
    textfile = open("{}.txt".format(os.getpid()), 'w')
    # -load_freq_dawg=False -load_system_dawg=False -preserve_interword_spaces=1 -psm=5
    # config='--preserve_interword_spaces 1',
    text = pytesseract.image_to_string(Image.open(filename),lang='eng', nice=1)
    os.remove(filename)
    textfile.write(text)
    textfile.close()