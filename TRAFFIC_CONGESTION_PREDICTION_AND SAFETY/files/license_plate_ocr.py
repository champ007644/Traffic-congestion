import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import pytesseract

original_image = cv2.imread('image4.jpeg') # Reading image using cv2.read()
original_image_color = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB) # Specify color for image
grayscale_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
b_filter = cv2.bilateralFilter(grayscale_img, 11, 17, 17) # Reduce noise
edged_img = cv2.Canny(b_filter, 30, 450)
keypoints = cv2.findContours(edged_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]



location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour,10, True) #approximate polygon with contour and value
    if len(approx) == 4:
        location = approx
        break




mask = np.zeros(grayscale_img.shape, np.uint8)
# locating and masking the number plate
new_image = cv2.drawContours(mask, [location], 0,255, -1)
new_image = cv2.bitwise_and(original_image, original_image, mask=mask)

res = cv2.rectangle(original_image, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)


(x,y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = grayscale_img[x1:x2+1, y1:y2+1]

reader = easyocr.Reader(['en']) # en indicates english language
result = reader.readtext(cropped_image) # reading english characters from cropped number plate image
print(result)



















