import yaml

from datetime import datetime

with open('./config/config.yml', 'r') as yml:
    config = yaml.safe_load(yml)

print(config)

experimental_info = config['experimental_info']
signal_info = config['signal_info']
color_01 = config['signal_color_01']


yaml_file_info = config
config[0]

sub = yaml_file_info['experimental_info']['sub']
shedule = yaml_file_info['experimental_info']['shedule']
session = yaml_file_info['experimental_info']['session']
med = yaml_file_info['experimental_info']['med']
now = datetime.now().strftime("%y-%m-%d-%H-%M")
file_name = f"{now}_{sub}_{shedule}_{session}_{med}"
file_path = "./video/"
video_name = f'{file_path}{file_name}.mp4'

signal_name = "signal_info"
color_num ='color_01'

width = yaml_file_info[signal_name]['width']
height = yaml_file_info[signal_name]['height']
coodinate = (width,height)
radius = yaml_file_info[signal_name]['radius']
color_b = yaml_file_info[color_num]['color_B']
color_g = yaml_file_info[color_num]['color_G']
color_r = yaml_file_info[color_num]['color_R']
color_info = (color_b,color_g,color_r)
color_info = (color_b,color_g,color_r )

(experimental_info,signal_info01)