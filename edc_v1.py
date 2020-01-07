black_threshold = (0, 43, -19, 18, -24, 20)

import sensor, image, math ,struct,time
from pyb import LED
from pyb import UART
from struct import pack, unpack
import json
import lcd
sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
sensor.set_auto_whitebal(False) # must be turned off for color tracking
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 200)     # WARNING: If you use QQVGA it may take seconds
               # to process a frame sometimes.
uart = UART(3, 115200)
lcd.init()
clock = time.clock()
red_led   = LED(1)
green_led = LED(2)

GREEN = (0,255,0)
countBar=0
countQR=0

def send(theta_err,rho_err):
    sumA = 0
    sumB = 0
    data = bytearray([0x41,0x43])
    uart.write(data)

    data = bytearray([0x02,8])
    for b in data:
        sumB = sumB + b
        sumA = sumA + sumB
    uart.write(data)

    float_value = theta_err
    float_bytes = pack('f', float_value)
    for b in float_bytes:
        sumB = sumB + b
        sumA = sumA + sumB
    uart.write(float_bytes)
    #print("linetheta=",line.theta())
    #print("theta=",float_value)

    float_value = rho_err*0.1
    float_bytes = pack('f', float_value)
    for b in float_bytes:
        sumB = sumB + b
        sumA = sumA + sumB
    uart.write(float_bytes)

    data = bytearray([sumA, sumB])
    uart.write(data)


while(True):
    clock.tick()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QQQVGA)
    img = sensor.snapshot()

    img.binary([black_threshold])
    img.rotation_corr(x_rotation=0,y_rotation=0,z_rotation=-90)
    line = img.get_regression([(100,100,0,0,0,0)], robust = True)

    #blobs = img.find_blobs([black_threshold],roi=[int(img.width()/2),int(img_binary.height()*(i+1)/5),200,25],y_stride=3,pixels_threshold=5
    if (line):
        rho_err = abs(line.rho())-img.width()/2 #计算一条直线与图像中央的距离
        #print(line.rho())
        #坐标变换  xy轴的角度
        if line.theta()>90:
            theta_err = line.theta()-180
        else:
            theta_err = line.theta()

        img.draw_line(line.line(), color = GREEN)

        lcd.display(img)

        send(theta_err,rho_err)

    else:
        send(200,0)

    #sensor.set_pixformat(sensor.GRAYSCALE)
    #sensor.set_framesize(sensor.VGA)
    #sensor.set_windowing((320, 240))
    #img = sensor.snapshot()

    #bar = img.find_barcodes()
    #if bar:
        ##print(bar)
        #if countBar==0:
            #img.save("bar0.jpg",quality=100)
        #elif countBar==1:
            #img.save("bar1.jpg",quality=100)
        #elif countBar==2:
            #img.save("bar2.jpg",quality=100)
        #countBar+=1
        #green_led.on()
    #else:
        #green_led.off()

    #qr = img.find_qrcodes()
    #if qr:
       ##print(qr)
       #if countQR==0:
           #img.save("qr0.jpg",quality=100)
       #elif countQR==1:
           #img.save("qr1.jpg",quality=100)
       #elif countQR==2:
           #img.save("qr2.jpg",quality=100)
       #countQR+=1
       #red_led.on()
    #else:
        #red_led.off()



    #lcd.display(img)
    #print("fps=",clock.fps())
