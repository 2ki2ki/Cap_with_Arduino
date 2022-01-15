import cv2
import numpy as np
import time
from datetime import datetime
import serial
from nptyping import NDArray
from typing import Tuple


Color = Tuple[int, int, int]




def draw_circle(frame: NDArray, params, radius, color: Color,
                 thickness: int):
    xc, yc = params
    r = radius
    cv2.circle(frame, (xc, yc),r,color,thickness=thickness)


if __name__ == '__main__':
    
    sub, shedule, session, med = "a","b","c","d"
    now = datetime.now().strftime("%y-%m-%d-%H-%M")
    file_name = f"{now}_{sub}_{shedule}_{session}_{med}"
    file_path = "C:/Users/Yasuyuki.Niki/cap/cap/"
    
    cap = cv2.VideoCapture(0)
    fps = int(cap.get(cv2.CAP_PROP_FPS))                    
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')       
    video = cv2.VideoWriter(f'{file_path}{file_name}.mp4', fourcc, fps, (w, h))

    while True:

        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        re_color_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

        draw_circle(re_color_frame,(500,100),30, (0,255,0), -1)

        cv2.imshow('frame',re_color_frame)
        video.write(re_color_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cap.release()
    cv2.destroyAllWindows()



print("Open port")

ser = serial.Serial("COM3",9600)

flag_decoded = "None"
print(flag_decoded)
task_on = True
count = 0

while task_on == True:
    flag = ser.readline()
    flag_decoded = flag.strip().decode("UTF-8")
    print(flag_decoded)
    count += 1
    print(count)

    if flag_decoded == "type01":
        print("FT "+flag_decoded)
    
    if flag_decoded == "type02":
        print("peak "+flag_decoded)

    if flag_decoded == "trigger":
       break

ser.close()