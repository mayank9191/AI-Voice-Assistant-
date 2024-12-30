import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


def volume_adjuster():
    cap = cv2.VideoCapture(0)  # Checks for camera

    mpHands = mp.solutions.hands  # Detects hand/finger
    hands = mpHands.Hands()  # Complete the initialization configuration of hands
    mpDraw = mp.solutions.drawing_utils

    # To access speaker through the library pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volbar = 400
    volper = 0
    volMin, volMax = volume.GetVolumeRange()[:2]

    while True:
        success, img = cap.read()  # If camera works capture an image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB

        # Collection of gesture information
        results = hands.process(imgRGB)  # Complete the image processing

        lmList = []  # Empty list
        if results.multi_hand_landmarks:  # List of all hands detected
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):
                    # Get finger joint points
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # Adding to the empty list 'lmList'
                    lmList.append([id, cx, cy])
                mpDraw.draw_landmarks(
                    img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:
            # Getting the value at a point
            x1, y1 = lmList[4][1], lmList[4][2]  # Thumb
            x2, y2 = lmList[8][1], lmList[8][2]  # Index finger
            # Creating circle at the tips of thumb and index finger
            cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
            # Create a line between tips of index finger and thumb
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # Distance between tips using hypotenuse
            length = hypot(x2 - x1, y2 - y1)
            # Convert hand range to volume range
            vol = np.interp(length, [30, 350], [volMin, volMax])
            volbar = np.interp(length, [30, 350], [400, 150])
            volper = np.interp(length, [30, 350], [0, 100])

            print(vol, int(length))
            volume.SetMasterVolumeLevel(vol, None)

            # Creating volume bar for volume level
            cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 4)
            cv2.rectangle(img, (50, int(volbar)), (85, 400),
                          (0, 0, 255), cv2.FILLED)
            cv2.putText(img, f"{int(volper)}%", (10, 40),
                        cv2.FONT_ITALIC, 1, (0, 255, 98), 3)

        # Show the video
        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xff == ord(' '):  # By using spacebar delay will stop
            break

    cap.release()  # Stop cam
    cv2.destroyAllWindows()  # Close window


if __name__ == "__main__":
    volume_adjuster()
