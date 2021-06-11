from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (50, 100, 100)
greenUpper = (70, 255, 255)
#pts = deque(maxlen=args["buffer"])
pts = []
#print(pts)
clr = (0,0,0)
th_yl= 1
th_bl=1
th_rd=1
th_wh=1
th_er=1
th_s=1
th_m=1
th_l= 1

def th_reset():    
    th_yl= 1
    th_bl=1
    th_rd=1
    th_wh=1
    th_er=1
    th_s=1
    th_m=1
    th_l= 1

thick_ness = 5


# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)
# keep looping
th_reset()
while True:
    # grab the current frame
    # print("th_yl",th_yl)
    # print("th_rd",th_rd)
    # print("th_wh",th_wh)
    # print("th_bl",th_bl)
    # print("th_er",th_er)
    # print("th_s",th_s)
    # print("th_m",th_m)
    # print("th_l",th_l)

    frame = vs.read()
    height,width, ch = frame.shape
    frame = cv2.flip(frame,1)
    #width  = vs.get(cv2.CAP_PROP_FRAME_WIDTH) # float
    #print(width)
    #height = vs.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
    #print(height)
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = cv2.rectangle(frame, (5,5), (80,79), (0,255,255), th_yl) 
    frame = cv2.rectangle(frame, (85,5), (160,79), (0,0,255), th_rd)
    frame = cv2.rectangle(frame, (165,5), (240,79), (255,0,0), th_bl)
    frame = cv2.rectangle(frame, (245,5), (320,79), (255,255,255), th_wh)
    frame = cv2.rectangle(frame, (325,5), (460,79), (0,0,0), th_er)
    frame = cv2.putText(frame, 'Eraser', (340,50), cv2.FONT_HERSHEY_SIMPLEX ,  
                   1, (0,0,0), 2, cv2.LINE_AA) 
    frame = cv2.rectangle(frame, (465,5), (520,79), (0,0,0), th_s)
    frame = cv2.putText(frame, 'S', (480,50), cv2.FONT_HERSHEY_SIMPLEX ,  
                   1, (0,0,0), 2, cv2.LINE_AA) 
    frame = cv2.rectangle(frame, (525,5), (580,79), (0,0,0), th_m) 
    frame = cv2.putText(frame, 'M', (540,50), cv2.FONT_HERSHEY_SIMPLEX ,  
                   1, (0,0,0), 2, cv2.LINE_AA) 
    frame = cv2.rectangle(frame, (585,5), (639,79), (0,0,0), th_l) 
    frame = cv2.putText(frame, 'L', (600,50), cv2.FONT_HERSHEY_SIMPLEX ,  
                   1, (0,0,0), 2, cv2.LINE_AA) 
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                clr, 2)
            cv2.circle(frame, center, 5, clr, -1)
    # update the points queue
        
    if center is not None:    
        if(center[1]>(height/6)):         
            pts.append([center,thick_ness,clr])             
        else:     
            if(5<center[0]<80):
                th_yl= 1
                th_bl=1
                th_rd=1
                th_wh=1
                th_er=1
                th_s=1
                th_m=1
                th_l= 1
                th_yl = 2
                clr = (0,255,255)
            elif(85<center[0]<160):    
                th_yl= 1
                th_bl=1
                th_rd=1
                th_wh=1
                th_er=1
                th_s=1
                th_m=1
                th_l= 1
                th_rd = 2
                clr = (0,0,255)
            elif(165<center[0]<240):    
                th_yl= 1
                th_bl=1
                th_rd=1
                th_wh=1
                th_er=1
                th_s=1
                th_m=1
                th_l= 1
                th_bl = 2
                clr = (255,0,0)
            elif(245<center[0]<320):    
                th_yl= 1
                th_bl=1
                th_rd=1
                th_wh=1
                th_er=1
                th_s=1  
                th_m=1
                th_l= 1
                th_wh = 2
                clr = (255,255,255)
            elif(325<center[0]<460):    
                th_yl= 1
                th_bl=1
                th_rd=1
                th_wh=1
                th_er=1
                th_s=1
                th_m=1
                th_l= 1
                th_er = 2
                pts = []
                clr = (0,0,0)
                #thick_ness = 5
            elif(465<center[0]<520):    
                th_yl= 1
                th_bl=1
                th_rd=1
                th_wh=1 
                th_er=1
                th_s=1
                th_m=1
                th_l= 1
                th_s = 2
                thick_ness = 1
            elif(525<center[0]<580):    
                th_yl= 1
                th_bl=1
                th_rd=1
                th_wh=1
                th_er=1
                th_s=1
                th_m=1
                th_l= 1
                th_m = 2
                thick_ness = 5
            elif(585<center[0]<640):    
                th_yl= 1
                th_bl=1
                th_rd=1
                th_wh=1
                th_er=1
                th_s=1
                th_m=1
                th_l= 1                
                th_l = 2   
                thick_ness = 10                     
            pts.append(None) 
    #print(pts)
    # loop over the set of tracked points
    else:
            pts.append(None) 
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        # thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        # print(pts[i][1])
        # print(pts[i][2])
        # print(pts[i - 1][0])
        # print(pts[i][0])
        cv2.line(frame, pts[i - 1][0], pts[i][0], pts[i][2], pts[i][1])
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