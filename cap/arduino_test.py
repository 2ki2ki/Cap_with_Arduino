import serial



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