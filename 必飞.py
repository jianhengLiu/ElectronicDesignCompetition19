import sensor, image, pyb,math
from pyb import UART
from pyb import LED
from struct import pack, unpack
import json
import lcd

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)  # 关闭自动白平衡调整

uart = UART(3, 115200)
lcd.init()
red_led   = LED(1)
green_led = LED(2)

black_threshold = (0, 43, -19, 18, -24, 20)

threshold_min = 3
threshold_max = 35

countBar=0
countQR=0

#与飞控通信协议
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
    sensor.set_framesize(sensor.QQVGA)
    img = sensor.snapshot()
    #进行镜头畸变矫正
    img.lens_corr(1.8)
    #利用Canny算法进行边缘检测
    img.find_edges(image.EDGE_CANNY,threshold = (0,160))

    tempY = [0,0]
    deltaY=[0,0,0,0]
    avgY=[0,0,0,0]
    #从图像中均匀获取四列进行取样
    for i in range(4):
        temp=0
        #对每一列的像素进行遍历，获取绳子的坐标
        for height in range(img.height()):
            pix=img.get_pixel(int(img.width()*(i+1)/5),height)

            if(pix==255):
                temp+=1
                if temp == 1:
                    tempY[0]=height
                if temp == 2:
                    tempY[1]=height
                    deltaY[i]=tempY[1]-tempY[0]
                    tempY[0]=tempY[1]

                    if(deltaY[i]>threshold_min and deltaY[i]<threshold_max):
                        avgY[i]=(tempY[1]+tempY[0])/2
                        img.draw_cross(int(img.width()*(i+1)/5),int(avgY[i]),thickness=3)
                        break
                    else:
                        temp=1
                        deltaY[i]=0
                height+=1

    #对获取的黑线坐标进行检验
    sumY=0
    tempI = [0,0,0]
    for i in range(4-1):
        #检验相邻的坐标是否处于相似的水平面上
        if(abs(avgY[i]-avgY[i+1])<10):
            if tempI[2]==0:
                tempI[0]=i
                tempI[1]=i+1
                tempI[2]=1
            if tempI[1]<=i+1:
                tempI[1]=i+1

            img.draw_line(int(img.width()*(i+1)/5),int(avgY[i]),int(img.width()*(i+2)/5),int(avgY[i+1]),thickness=3)

    #对获取的黑线坐标进行匹配并返回识别到的线段的霍夫表达
    thetaR = 0
    thetaD = 0
    rho = 0
    if tempI[2]==1:
        thetaR = math.atan2((avgY[tempI[1]]-avgY[tempI[0]]),(img.width()*(tempI[1]+1)/5-img.width()*(tempI[0]+1)/5))
        thetaD = 180/math.pi*thetaR
        rho = img.height()/2-((img.height()-avgY[tempI[0]])-((img.width()/2-img.width()*(tempI[0]+1)/5)*math.tan(thetaR)))
        #print(thetaD)
        print(rho)

        #计算直线与图像中央的距离
        rho_err = (abs(rho)-img.width()/2)/2
        #坐标变换  xy轴的角度
        if thetaD>90:
            theta_err = thetaD-180
        else:
            theta_err = thetaD

        send(theta_err,rho_err)

        img.draw_line(int(img.width()*(tempI[0]+1)/5),int(avgY[tempI[0]]),int(img.width()*(tempI[1]+1)/5),int(avgY[tempI[1]]),thickness=3)

    lcd.display(img)

    sensor.set_framesize(sensor.VGA)
    sensor.set_windowing((320, 240))
    img = sensor.snapshot()

    #识别条形码并拍三张照片
    bar = img.find_barcodes()
    if bar:
         if countBar==0:
             img.save("bar0.jpg",quality=100)
         elif countBar==1:
             img.save("bar1.jpg",quality=100)
         elif countBar==2:
             img.save("bar2.jpg",quality=100)
         countBar+=1
         green_led.on()
    else:
         green_led.off()

    #识别二维码并拍三张照片
    qr = img.find_qrcodes()
    if qr:
         if countQR==0:
             img.save("qr0.jpg",quality=100)
         elif countQR==1:
             img.save("qr1.jpg",quality=100)
         elif countQR==2:
             img.save("qr2.jpg",quality=100)
         countQR+=1
         red_led.on()
    else:
        red_led.off()
