import cv2 
import time
import numpy as np
import HandTrackingmodule as HTM


# Setting the variable for video frame Height and width
wCam , hCam = 640 , 480



Video = cv2.VideoCapture(0)
Video.set(3,wCam)
Video.set(4,hCam)

current_Time = 0
past_Time = 0

#
detector = HTM.handdetector(detectionCon=0.7)

while True:
    success , img = Video.read()

    # This will give us the hand
    img = detector.findHands(img)

    # This will give the list of poition of all 21 point in hand for every action 
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) != 0:
        print(lmList[2])

    
    # Defining the FPS

    current_Time = time.time()
    fps = 1/(current_Time-past_Time)
    past_Time = current_Time

    # Displaying the fps on Screen And font,size ETC

    cv2.putText(img,f'FPS:{(int(fps))}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)








    cv2.imshow("IMG", img)

    if cv2.waitKey(1) & 0xFF ==ord("q"):
        
        break


Video.release()
cv2.destroyAllWindows()