import cv2
import numpy as np
from tkinter import filedialog
from tkinter import Tk

root = Tk()
root.withdraw()
file_path = r"wound3.jpg"

image = cv2.imread(file_path)

image = cv2.resize(image, (600, 600))
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

mask1 = cv2.inRange(hsv, lower_red, upper_red)
mask2 = cv2.inRange(hsv, np.array([160,100,100]), np.array([180,255,255]))
mask = mask1 + mask2

kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    area = cv2.contourArea(contour)
    if 500 < area < 50000:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(image, 'Possible Wound', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow('Healthcare Imaging Analyzer', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
