# Sources used to develop this: 
# opencv.org
# pyimagesearch.com , got in touch with the owner of the site to help develop this to be used
# python.org
# iumtils forums
# openCV forums


# import the necessary packages
# Needs to install numpy,imutils, opencv
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct the argument parse and parse the arguments
# This is what sets the video and also the line that follows the circle
# Buffer default number is length of line
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=35,
	help="max buffer size")
args = vars(ap.parse_args())

# Defines lower and upper levels of color tracked Both are HSV 
# Then you have to initialize those points in the args
whiteLower = (0, 0, 0)
whiteUpper = (180, 255, 255)
pts = deque(maxlen=args["buffer"])

# You can set the video stream manually but if not this helps program find webcam attached
if not args.get("video", False):
	vs = VideoStream(src=0).start()

# If nothing is provided for webcam then this will grab video uploaded from file
else:
	vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to start
time.sleep(2.0)

# This while loop is what grabs the video frame by frame and sets the circle and line
while True:
	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame

	# If there is no webcam attached then when the video is over it will break
	if frame is None:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "black", then perform
	# a series of dilations This will create a second frame that will be able to follow black
	
	mask = cv2.inRange(hsv, whiteLower, whiteUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# Finds the center of object
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	# If no masks are created it cant start.
	if len(cnts) > 0:
		#This is the part of the code which lead us to believe that we can use IR lights. As it would be the biggest contrast of white
		#compute the minimum circle
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# update the points
	pts.appendleft(center)

	#Next part is where it draws the thickness of the circle and also the length of the line set in the buffer
	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are none, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, Draw line and line thickness
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()

# Sources used to develop this: 
# opencv.org
# pyimagesearch.com , contected owner of the site to help develop this to be used
# python.org
# imtuls forums
# openCV forums