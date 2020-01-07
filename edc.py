import sensor, image, pyb,math
from pyb import UART
from pyb import LED
from struct import pack, unpack
import lcd
import json

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA) # can be QVGA on M7...
#sensor.set_windowing((200, 200))
sensor.skip_frames(10)
#sensor.set_auto_gain(False) # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout..

uart = UART(3, 115200)
lcd.init()

GREEN = (0,255,0)

red_led   = LED(1)
green_led = LED(2)
#blue_led  = LED(3)
#ir_led    = LED(4)

black_threshold = (0, 43, -19, 18, -24, 20)
#gray_threshold = (20,100)

threshold_min = 3
threshold_max = 35

#min_degree = 0
#max_degree = 179
while(True):
    img = sensor.snapshot()
    img.lens_corr(1.8)
    img.find_edges(image.EDGE_CANNY,threshold = (0,160))
    #for l in img.find_lines():
        #if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            #print(l.theta())
            #img.draw_line(l.line(), color = GREEN)
    #img_binary.rotation_corr(x_rotation=0,y_rotation=0,z_rotation=0)
    #img = img_binary.copy()
    #lcd.display(img)
    #img.lens_corr(1.8) # strength of 1.8 is good for the 2.8mm lens.
    #img_binary.binary([black_threshold])
    #img_binary.to_grayscale()

###########################################
    tempY = [0,0]
    deltaY=[0,0,0,0]
    avgY=[0,0,0,0]
    for i in range(4):
        temp=0
        for height in range(img.height()):
            pix=img.get_pixel(int(img.width()*(i+1)/5),height)

            if(pix==255):
                temp+=1
                #print(temp)
                if temp == 1:
                    tempY[0]=height
                if temp == 2:
                    tempY[1]=height
                    deltaY[i]=tempY[1]-tempY[0]
                    #print(tempY)
                    tempY[0]=tempY[1]

                    if(deltaY[i]>threshold_min and deltaY[i]<threshold_max):
                        avgY[i]=(tempY[1]+tempY[0])/2
                        img.draw_cross(int(img.width()*(i+1)/5),int(avgY[i]),thickness=3)
                        #print(i,"\n",avgY[i])
                        break
                    else:
                        temp=1
                        deltaY[i]=0
                height+=1
    sumY=0
    tempI = [0,0,0]
    for i in range(4-1):
        if(abs(avgY[i]-avgY[i+1])<10):
            if tempI[2]==0:
                tempI[0]=i
                tempI[1]=i+1
                tempI[2]=1
            if tempI[1]<=i+1:
                tempI[1]=i+1

            img.draw_line(int(img.width()*(i+1)/5),int(avgY[i]),int(img.width()*(i+2)/5),int(avgY[i+1]),thickness=3)
    thetaR = 0
    thetaD = 0
    rho = 0
    if tempI[2]==1:
        thetaR = math.atan2((avgY[tempI[1]]-avgY[tempI[0]]),(img.width()*(tempI[1]+1)/5-img.width()*(tempI[0]+1)/5))
        thetaD = 180/math.pi*thetaR
        rho = 60-((img.height()-avgY[tempI[0]])-((img.width()/2-img.width()*(tempI[0]+1)/5)*math.tan(thetaR)))
        print(thetaD)
        print(rho)
        img.draw_line(int(img.width()*(tempI[0]+1)/5),int(avgY[tempI[0]]),int(img.width()*(tempI[1]+1)/5),int(avgY[tempI[1]]),thickness=3)

#########################
    #count=0
    #for i in range(img_binary.height()):
        #pix=img_binary.get_pixel(int(img_binary.width()/2),i)

        #if(pix[0]==255):
            #count+=1
        #else :
            #if(count<threshold_min or count>threshold_max):
                #count=0

    #if(count<threshold_min):
        #print("failed to detect wring!\n",count)
    #else:
        #print("wring pix = \n",count)
        #print("distance = \n",1009.05/count)




######################3
    #line = img_binary.get_regression([black_threshold])
    #if(line):
        #print("theta = ",line.theta(),"rho = ",line.rho(),"mag = %s" , str(line.magnitude()))
        #img_binary.draw_line(line.line(),color=GREEN,thickness=5)
##############
    qr = img.find_qrcodes()
    if qr:
        print(qr)
        img.save("qr.jpg",quality=100)
        red_led.on()
    else:
        red_led.off()

    bar = img.find_barcodes()
    if bar:
        print(bar)
        img.save("bar.jpg",quality=100)
        green_led.on()
    else:
        green_led.off()
####################
    #countW=[0,0,0,0]
    #countB=[0,0,0,0]
    #sumY=[0,0,0,0]
    #allY=0
    #for i in range(4):
        #for height in range(img_binary.height()):
            #pix=img_binary.get_pixel(int(img_binary.width()*(i+1)/5),height)
            ##print(pix)
            #if(pix[0]==255):
                #countW[i]+=1
                #sumY[i]+=height
            #else :
                #countB[i]+=1
                #if(countW[i]<threshold_min or countW[i]>threshold_max):
                    #countW[i]=0
                    #sumY[i]=0
                #if(countW[i]>threshold_min and countB[i]>threshold_min):
                    #break
        #if(countW[i]<threshold_min):
             #print("failed to detect wring!\n",i)
        #else:
             #allY+=sumY[i]
             #img_binary.draw_cross(int(img_binary.width()*(i+1)/5),int(sumY[i]/countW[i]),color=GREEN,thickness=3)
             #print("wring pix = \n",countW[i])
             #print("distance = \n",1009.05/countW[i])
    #avgY = allY/4
    #for i in range(3):
        #if((countW[i]!=0)and(countW[i+1]!=0)and sumY[i]):
            #img_binary.draw_line(int(img_binary.width()*(i+1)/5),int(sumY[i]/countW[i]),int(img_binary.width()*(i+2)/5),int(sumY[i+1]/countW[i+1]),color=GREEN,thickness=3)
#############################
    #blobs=[]
    #count=0
    #sumY=[0,0,0,0]
    #for i in range(4):
        #blobs.append(img.find_blobs([black_threshold],roi=[0,int(img_binary.height()*(i+1)/5),200,25],y_stride=3,pixels_threshold=5))
        #for blob in blobs[-1]:
            #count+=1
            #img_binary.draw_cross(blob.cx(),blob.cy(),color=GREEN,thickness=3)
    #if(count[i]<threshold_min):
         #print("failed to detect wring!\n",i)
    #else:
         #print("wring pix = \n",count[i])
         #print("distance = \n",1009.05/count[i])
#for i in range(3):
    #if((count[i]!=0)and(count[i+1]!=0)):
        #img_binary.draw_line(int(img_binary.width()*(i+1)/5),int(sumY[i]/count[i]),int(img_binary.width()*(i+2)/5),int(sumY[i+1]/count[i+1]),color=GREEN,thickness=3)

############################
    #if (line):
        #rho_err = abs(line.rho())-img.width()/2 #计算一条直线与图像中央的距离

        ##坐标变换  xy轴的角度
        #if line.theta()>90:
            #theta_err = line.theta()-180
        #else:
            #theta_err = line.theta()

        #img.draw_line(line.line(), color = 127)
        #output_str = "%f"%(theta_err)
        #sumA = 0
        #sumB = 0
        #data = bytearray([0x41,0x43])
        #uart.write(data)

        #data = bytearray([0x02,8])
        #for b in data:
            #sumB = sumB + b
            #sumA = sumA + sumB
        #uart.write(data)

        #float_value = theta_err
        #float_bytes = pack('f', float_value)
        #for b in float_bytes:
            #sumB = sumB + b
            #sumA = sumA + sumB
        #uart.write(float_bytes)

        #float_value = rho_err*0.1
        #float_bytes = pack('f', float_value)
        #for b in float_bytes:
            #sumB = sumB + b
            #sumA = sumA + sumB
        #uart.write(float_bytes)

        #data = bytearray([sumA, sumB])
        #uart.write(data)

        #print(float_value)
        ##print(rho_err*0.1)
    #else:
        #sumA = 0
        #sumB = 0
        #data = bytearray([0x41,0x43])
        #uart.write(data)

        #data = bytearray([0x02,8])
        #for b in data:
            #sumB = sumB + b
            #sumA = sumA + sumB
        #uart.write(data)

        #float_value = 200
        #float_bytes = pack('f', float_value)
        #for b in float_bytes:
            #sumB = sumB + b
            #sumA = sumA + sumB
        #uart.write(float_bytes)

        #float_value = 0
        #float_bytes = pack('f', float_value)
        #for b in float_bytes:
            #sumB = sumB + b
            #sumA = sumA + sumB
        #uart.write(float_bytes)

        #data = bytearray([sumA, sumB])
        #uart.write(data)
