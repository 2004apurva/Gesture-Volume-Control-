import cv2 
import time
import numpy as np
import HandTrackingmodule as HTM
import math

# This library is by andre miras to control the volume of your device

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Setting the variable for video frame Height and width

wCam , hCam = 640 , 480



Video = cv2.VideoCapture(0)
Video.set(3,wCam)
Video.set(4,hCam)

current_Time = 0
past_Time = 0

# From hand detection module to detect the hand

detector = HTM.handdetector(detectionCon=0.7)



# Code from pycaw to connect to device audio

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()




# Initializing the variable 

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer=0





while True:
    success , img = Video.read()

    # This will give us the hand

    img = detector.findHands(img)

    # This will give the list of poition of all 21 point in hand for every action 

    lmList = detector.findPosition(img, draw = False)

    # By using this line we get list of position of perticular points
    # This will return no value if there is no hands

    if len(lmList) != 0:
        # print(lmList[4],lmList[8]) # We are using the position that are needed to change the volume


        # This gives the 1st and 2nd value of points to particular variable or this are the points

        x1 , y1 = lmList[4][1],lmList[4][2]
        x2 , y2 = lmList[8][1],lmList[8][2]

        # To find center of line between the particular points

        cx , cy = (x1+x2) // 2 , (y1+y2) // 2

        # Creating Circle on the particular points

        cv2.circle(img,(x1,y1),8,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),8,(255,0,255),cv2.FILLED)

        # This display the  connection of the two hand point with a line

        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        # To display the meddle point

        cv2.circle(img, (cx,cy),15,(255,0,255), cv2.FILLED)

        # Gives the distance between the points

        length = math.hypot(x2-x1,y2-y1)
        

        # Hand Range 50 - 300
        # Volume Range -65 - 0

        vol = np.interp(length,[50,300],[minVol,maxVol])
        volBar = np.interp(length,[50,300],[400,150])
        volPer = np.interp(length,[50,300],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)




        # Changing the color of the center points According to disqtance

        if length<40:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)


        # Adding the Voume Bar in the display 

        cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
        cv2.putText(img,f'{(int(volPer))}%',(40,450),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),3)

        
    

    # Defining the FPS

    current_Time = time.time()
    fps = 1/(current_Time-past_Time)
    past_Time = current_Time

    # Displaying the fps on Screen And font,size ETC

    cv2.putText(img,f'FPS:{(int(fps))}',(40,50),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),3)


    cv2.imshow("IMG", img)

    if cv2.waitKey(1) & 0xFF ==ord("q"):
        
        break


Video.release()
cv2.destroyAllWindows()