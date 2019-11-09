#!/usr/bin/python
# referenc: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
#   thanks: https://stackoverflow.com/questions/29780123

import numpy as np
import cv2
import sys
import glob
import imutils
import time
import yaml
import glob

try:
    col = int(sys.argv[1])
    row = int(sys.argv[2])
except:
    col, row = 7, 5

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((col*row, 3), np.float32)
objp[:,:2] = np.mgrid[0:col, 0:row].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

#
# read image from camera
#
cap = cv2.VideoCapture(0)
previos_t = None
current_t = None

# remove all files in img folder
files = glob.glob('img/*')
try:
    for f in files:
        os.remove(f)
except:
    print("remove files error!")


while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, 320)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (col, row))

    if ret == True:
        # Draw and display the corners
        cv2.drawChessboardCorners(frame, (col, row), corners, ret)
        current_t = int(time.time())

        if current_t != previos_t:
            objpoints.append(objp)
            imgpoints.append(corners)
            t = "img/" + str(int(time.time())) + ".jpg"
            cv2.imwrite(t, gray)
            print "save " + t

        previos_t = current_t

    cv2.putText(frame, "press 'q' to calibrate", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255))
    cv2.imshow("preview", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()


"""
#
# read image from camera
#
t = None
images = sorted(glob.glob("img/1*.jpg"))
for fname in images:
    frame = cv2.imread(fname)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (col, row))

    if ret == True:
        # Draw and display the corners
        cv2.drawChessboardCorners(frame, (col, row), corners, ret)
        objpoints.append(objp)
        imgpoints.append(corners)
        cv2.imshow('img', frame)
        cv2.waitKey(500)
    t = fname
"""



# calibrate camera
print("Calibrating... ")
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
camera_matrix = mtx.tolist()
print("===================================================")
print("Intrinsic Camera Matrix:")
print(mtx)
print("===================================================")
print("Camera Distortion Coefficients:")
dist =(np.array([dist[0][0], dist[0][1], 0, 0, 0]))
#dist = np.array([dist[0][0], dist[0][1], dist[0][2], dist[0][3], dist[0][4]])
dist_coeff = dist.tolist()
print(dist)
print("===================================================")

data = {"camera_matrix": camera_matrix, "dist_coeff": dist_coeff}
fname = "data.yaml"
with open(fname, "w") as f:
    yaml.dump(data, f)



# show last image
img = cv2.imread(t)
h, w = img.shape[:2]
cv2.imshow("preview", img)
cv2.waitKey(0)

# get undistort matrix and pixel matrix
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
print("===================================================")
print("Valid Pixel ROI:")
print(roi)
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
