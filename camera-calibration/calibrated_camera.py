import sys 
import yaml
import cv2 
import numpy as np

with open("data.yaml", "r") as stream:
    data = yaml.load(stream)

mtx = data["camera_matrix"]
mtx = np.asarray(mtx)
dist = data["dist_coeff"]
dist = np.asarray(dist)

imagePath = sys.argv[1]
img = cv2.imread(imagePath)
h, w = img.shape[:2]
cv2.imshow("preview", img)
cv2.waitKey(0)

# get undistort matrix and pixel matrix
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h)) 
print("===================================================")
print("Valid Pixel ROI:")
print roi
print("===================================================")

# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imshow("undistort", dst)
cv2.imwrite('img/undistort.jpg', dst)
cv2.waitKey(0)

cv2.destroyAllWindows()


