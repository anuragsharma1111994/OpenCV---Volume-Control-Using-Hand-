import cv2
import mediapipe as mp
import numpy as np
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###################################################


wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)

###################################################

cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]
vol = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)

    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 9, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 9, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 9, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2-x1, y2-y1)

        # HandRange 260 - 30
        # volume Range -74 - 0

        vol = np.interp(length, (20, 230), [minVol, maxVol])
        volBar = np.interp(length, (20, 230), [400, 150])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 30:
            cv2.circle(img, (cx, cy), 9, (0, 255, 0), cv2.FILLED)



        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0),  cv2.FILLED)



    cv2.imshow("Volume Control Using Hands", img)
    cv2.waitKey(1)