import pytesseract
from PIL import Image
import cv2

print (pytesseract.image_to_data(Image.open('./img/np1.jpeg')))
print (pytesseract.image_to_data(Image.open('./img/np2.jpeg')))
img = cv2.imread('./img/np1.jpeg')
print (pytesseract.image_to_string(img))