import cv2
from datetime import datetime
import serial
from nptyping import NDArray
from typing import Tuple
from multiprocessing import Value, Process
import yaml

Color = Tuple[int, int, int]

def read_yaml():
    with open('./config/config.yml', 'r') as yml:
        config = yaml.safe_load(yml)
    return(config)

def video_file_name_maker(yaml_file_info:dict):
    sub = yaml_file_info['experimental_info']['sub']
    shedule = yaml_file_info['experimental_info']['shedule']
    session = yaml_file_info['experimental_info']['session']
    med = yaml_file_info['experimental_info']['med']
    now = datetime.now().strftime("%y-%m-%d-%H-%M")
    file_name = f"{now}_{sub}_{shedule}_{session}_{med}"
    file_path = "./video/"
    video_name = f'{file_path}{file_name}.mp4'

    return(video_name)

def circle_info_getter(yaml_file_info:dict):
    width = yaml_file_info['signal_info']['width']
    height = yaml_file_info['signal_info']['height']
    coordinate = (width,height)
    radius = yaml_file_info['signal_info']['radius']
    return(coordinate,radius)

def circle_color_getter(yaml_file_info,color_num:dict):
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

def capture(sn:int,task:int):
    info = read_yaml()
    video_file_name = video_file_name_maker(info)
    coordinate,radius = circle_info_getter(info)
    color_01 = circle_color_getter(info,'color_01')
    color_02 = circle_color_getter(info,'color_02')
    color_03 = circle_color_getter(info,'color_03')
    color_04 = circle_color_getter(info,'color_04')
    circle_colors = (color_01,color_02,color_03,color_04)

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

        if sn.value > -1:
            print(sn.value)
            draw_circle(re_color_frame,coordinate,radius, circle_colors[sn.value], -1)

        cv2.imshow('frame',re_color_frame)
        video.write(re_color_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    task.value = 0
    video.release()
    cap.release()
    cv2.destroyAllWindows()


def get_serial(sn:int,task:int):

    info = read_yaml()
    port = info["arduino"]["port"]
    serial_baudrate = info["arduino"]["serial_baudrate"]
    pin_01 = info["arduino"]["pin_01"]
    #pin_02 = info["arduino"]["pin_02"]
    #pin_03 = info["arduino"]["pin_03"]
    #pin_04 = info["arduino"]["pin_04"]

    print("Open port!")
    ser = serial.Serial(port,serial_baudrate)

    while task.value == 1:
        pin_num = ser.readline()
        pin_num_int = int(pin_num.strip().decode("UTF-8"))
        #print(pin_num_int)
        sn.value = pin_num_int - pin_01

    ser.close()
    print("Close port!")


if __name__ == '__main__':
    print("Wait... starting record...")
    serial_num = Value('i',-1)
    task_state = Value('i',1)
    cap_p = Process(target = capture, args=(serial_num,task_state))
    ser_p = Process(target = get_serial, args=(serial_num,task_state))
    cap_p.start()
    ser_p.start()
    cap_p.join()
    ser_p.join()
    print("Recording ended.")