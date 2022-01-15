import cv2
import numpy as np
import time
from datetime import datetime
import serial
from nptyping import NDArray
from typing import Tuple
import multiprocessing
import yaml

Color = Tuple[int, int, int]

def read_yaml():
    with open('./config/config.yml', 'r') as yml:
        config = yaml.safe_load(yml)
    return(config)

def video_file_name_maker(yaml_file_info):
    sub = yaml_file_info['experimental_info']['sub']
    shedule = yaml_file_info['experimental_info']['shedule']
    session = yaml_file_info['experimental_info']['session']
    med = yaml_file_info['experimental_info']['med']
    now = datetime.now().strftime("%y-%m-%d-%H-%M")
    file_name = f"{now}_{sub}_{shedule}_{session}_{med}"
    file_path = "./video/"
    video_name = f'{file_path}{file_name}.mp4'

    return(video_name)

def circle_info_getter(yaml_file_info):
    width = yaml_file_info['signal_info']['width']
    height = yaml_file_info['signal_info']['height']
    coordinate = (width,height)
    radius = yaml_file_info['signal_info']['radius']
    return(coordinate,radius)

def circle_color_getter(yaml_file_info,color_num):
    color_b = yaml_file_info[color_num]['color_B']
    color_g = yaml_file_info[color_num]['color_G']
    color_r = yaml_file_info[color_num]['color_R']
    color_info = (color_b,color_g,color_r)
    return(color_info)


def draw_circle(frame: NDArray, params, radius, color: Color,
                 thickness: int):
    xc, yc = params
    r = radius
    cv2.circle(frame, (xc, yc),r,color,thickness=thickness)

def capture():
    info = read_yaml()
    video_file_name = video_file_name_maker(info)
    coordinate,radius = circle_info_getter(info)
    color_01 = circle_color_getter(info,'color_01')
    cap = cv2.VideoCapture(0)
    fps = int(cap.get(cv2.CAP_PROP_FPS))                    
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')       
    video = cv2.VideoWriter(video_file_name, fourcc, fps, (w, h))

    while True:

        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        re_color_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

        draw_circle(re_color_frame,coordinate,radius, color_01, -1)

        cv2.imshow('frame',re_color_frame)
        video.write(re_color_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("Wait... starting record...")
    proce01 = multiprocessing.Process(target = capture)
    proce01.start()
    proce01.join()
    print("Recording ended.")