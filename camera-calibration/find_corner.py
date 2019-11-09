#!/usr/bin/python

import numpy as np
import cv2
import sys

try:
    imagePath = sys.argv[1]
    col = int(sys.argv[2])
    row = int(sys.argv[3])
except:
    imagePath = "chessboard.jpg"
    col, row = 9, 6

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((col*row, 3), np.float32)
objp[:,:2] = np.mgrid[0:col, 0:row].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

img = cv2.imread(imagePath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find the chess board corners
cv2.putText(gray, "press 'q'...", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
cv2.imshow('gray', gray)
cv2.waitKey(0)
ret, corners = cv2.findChessboardCorners(gray, (col, row))

# If found, add object points, image points (after refining them)
if ret == True:
    objpoints.append(objp)
    imgpoints.append(corners)
    # Draw and display the corners
    cv2.drawChessboardCorners(img, (col, row), corners, ret)
    cv2.putText(img, "press 'q'...", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
    cv2.imshow('findCorners',img)
    cv2.waitKey(0)

#print(imgpoints)
cv2.destroyAllWindows()
