#!/usr/bin/python
import cv2
import numpy as np

i = 0
ix, iy = -1, -1
pts = [None] * 4

img = cv2.imread("lane.png")
cv2.putText(img, "press 'q' to exit", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
h, w = img.shape[:2]

# mouse callback function
def draw_circle(event, x, y, flags, param):
    global i, ix, iy, pts, M, processed
    if event == cv2.EVENT_LBUTTONDOWN:

        if i < 4:
            cv2.circle(img, (x,y), 5, (0,0,255),-1)
            ix,iy = x,y
            pts[i] = [ix, iy]
            i = i+1
            print(ix, iy)
        else:
            points1 = np.float32([pts[0], pts[1], pts[3], pts[2]])
            points2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
            M = cv2.getPerspectiveTransform(points1, points2)
            processed = cv2.warpPerspective(img, M, (640, 480))
            cv2.imshow("processed",processed)

cv2.namedWindow("projection")
cv2.setMouseCallback("projection", draw_circle)


while True:
    cv2.imshow("projection", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()


