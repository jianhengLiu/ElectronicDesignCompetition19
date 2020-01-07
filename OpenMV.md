# OpenMV

# 0.参数

## 0.1.图像

| **支持的图像格式** | Grayscale/RGB565/JPEG (and BAYER)                            |
| ------------------ | ------------------------------------------------------------ |
| **最大支持的像素** | **Grayscale**: 640×480 and under **RGB565**: 320×240 and under **Grayscale JPEG**: 640×480 and under **RGB565 JPEG**: 640×480 and under |

### 0.1.1.设置图像大小

- sensor.set_framesize() 设置图像的大
  - sensor.QQVGA: 160x120
  - sensor.QQVGA2: 128x160 (用于 lcd 扩展板)
  - sensor.HQVGA: 240x160
  - sensor.QVGA: 320x240
  - sensor.VGA: 640x480 (只用于OpenMV Cam M7 的灰度图处理图像，或者彩图采集图像)
  - sensor.QQCIF: 88x72
  - sensor.QCIF: 176x144
  - sensor.CIF: 352x288

## 0.2.镜头畸变

OpenMV中使用image.lens_corr(1.8)来矫正2.8mm焦距的镜头。也可以直接使用无畸变镜头。





# 1.颜色追踪

```python
# 颜色追踪的例子，一定要控制环境的光，保持光线是稳定的。
green_threshold   = (   0,   80,  -70,   -10,   -0,   30)
#设置绿色的阈值，括号里面的数值分别是L A B 的最大值和最小值（minL, maxL, minA, maxA, minB, maxB），LAB的值在图像左侧三个坐标图中选取。如果是灰度图，则只需设置（min, max）两个数字即可。

#LAB色彩模型是由亮度（L）和有关色彩的a, b三个要素组成。
#L表示明度（Luminosity），a表示从洋红色至绿色的范围，b表示从黄色至蓝色的范围。
#L的值域由0到100，L=50时，就相当于50%的黑；a和b的值域都是由+127至-128，其中+127 a就是红色，渐渐过渡到-128 a的时候就变成绿色；同样原理，+127 b是黄色，-128 b是蓝色。所有的颜色就以这三个值交互变化所组成。例如，一块色彩的Lab值是L = 100，a = 30, b = 0, 这块色彩就是粉红色。（注：此模式中的a轴,b轴颜色与RGB不同，洋红色更偏红，绿色更偏青，黄色略带红，蓝色有点偏青色）

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QQVGA) # 使用 QQVGA 速度快一些
sensor.skip_frames(time = 2000) # 跳过2000s，使新设置生效,并自动调节白平衡
sensor.set_auto_gain(False) # 关闭自动自动增益。默认开启的，在颜色识别中，一定要关闭白平衡。
sensor.set_auto_whitebal(False)
#关闭白平衡。白平衡是默认开启的，在颜色识别中，一定要关闭白平衡。
clock = time.clock() # 追踪帧率

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # 从感光芯片获得一张图像

    blobs = img.find_blobs([green_threshold])
    #find_blobs(thresholds, invert=False, roi=Auto),thresholds为颜色阈值，
    #是一个元组，需要用括号［ ］括起来。invert=1,反转颜色阈值，invert=False默认
    #不反转。roi设置颜色识别的视野区域，roi是一个元组， roi = (x, y, w, h)，代表
    #从左上顶点(x,y)开始的宽为w高为h的矩形区域，roi不设置的话默认为整个图像视野。
    #这个函数返回一个列表，[0]代表识别到的目标颜色区域左上顶点的x坐标，［1］代表
    #左上顶点y坐标，［2］代表目标区域的宽，［3］代表目标区域的高，［4］代表目标
    #区域像素点的个数，［5］代表目标区域的中心点x坐标，［6］代表目标区域中心点y坐标，
    #［7］代表目标颜色区域的旋转角度（是弧度值，浮点型，列表其他元素是整型），
    #［8］代表与此目标区域交叉的目标个数，［9］代表颜色的编号（它可以用来分辨这个
    #区域是用哪个颜色阈值threshold识别出来的）。
    if blobs:
    #如果找到了目标颜色
        for b in blobs:
        #迭代找到的目标颜色区域
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4]) # rect
            #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            #在目标颜色区域的中心画十字形标记

    print(clock.fps()) # 注意: 你的OpenMV连到电脑后帧率大概为原来的一半
    #如果断开电脑，帧率会增加
```

那么如何自己更改这个阈值呢？我们怎么知道我们的物体的颜色阈值呢？

- 数字列表项目首先在摄像头中找到目标颜色，在framebuffer中的目标颜色上左击圈出一个矩形
- 在framebuffer下面的坐标图中，选择LAB Color Space。

![img](https://book.openmv.cc/assets/02-019.jpg)

- 三个坐标图分别表示圈出的矩形区域内的颜色的LAB值，选取三个坐标图的最大最小值，即( 0, 60, -70, -10, -0, 30)

![img](https://book.openmv.cc/assets/02-020.jpg)

# 2.图像操作

## 2.1.获取/设置像素点

我们可以通过image.get_pixel(x, y)方法来获取一个像素点的值。

- image.get_pixel(x, y)
  - 对于灰度图: 返回(x,y)坐标的灰度值.
  - 对于彩色图: 返回(x,y)坐标的(r,g,b)的tuple.

同样，我们可以通过image.set_pixel(x, y, pixel)方法，来设置一个像素点的值。

- image.set_pixel(x, y, pixel)
  - 对于灰度图: 设置(x,y)坐标的灰度值。
  - 对于彩色图: 设置(x,y)坐标的(r,g,b)的值。

举例：

```python
img = sensor.snapshot()
img.get_pixel(10,10)
img.set_pixcel(10,10,(255,0,0))#设置坐标(10,10)的像素点为红色(255,0,0)
Copy
```

## 2.2获取图像的宽度和高度

- image.width()
  返回图像的宽度(像素)
- image.height()
  返回图像的高度(像素)
- image.format()
  灰度图会返回 sensor.GRAYSCALE，彩色图会返回 sensor.RGB565。
- image.size()
  返回图像的大小(byte)

## 2.3图像的运算

- image.invert()

取反，对于二值化的图像，0(黑)变成1(白)，1(白)变成0(黑)。

注：
图像可以是另一个image对象，或者是从 (bmp/pgm/ppm)文件读入的image对象。
两个图像都必须是相同的尺寸和类型（灰度图/彩色图）。

- image.nand(image)
  与另一个图片进行与非（NAND）运算。
- image.nor(image)
  与另一个图片进行或非（NOR）运算。
- image.xor(image)
  与另一个图片进行异或（XOR）运算。
- image.xnor(image)
  与另一个图片进行异或非（XNOR）运算。
- image.difference(image)
  从这张图片减去另一个图片。比如，对于每个通道的每个像素点，取相减绝对值操作。这个函数，经常用来做移动检测。

# 3.图像的统计信息

如果我想知道一个区域内的平均颜色或者占面积最大的颜色？

使用统计信息——Statistics！

## 3.1.ROI感兴趣的区域

![img](https://book.openmv.cc/assets/05-03-001.jpg)
roi的格式是(x, y, w, h)的tupple.

- x:ROI区域中左上角的x坐标
- y:ROI区域中左上角的y坐标
- w:ROI的宽度
- h:ROI的高度

## 3.2.Statistics

```
image.get_statistics(roi=Auto)
Copy
```

其中roi是目标区域。注意，这里的roi，bins之类的参数，一定要**显式**地标明，例如：

```
img.get_statistics(roi=(0,0,10,20))
Copy
```

**如果是 img.get_statistics((0,0,10,20))，ROI不会起作用。**

- statistics.mean() 返回灰度的**平均数**(0-255) (int)。你也可以通过statistics[0]获得。
- statistics.median() 返回灰度的**中位数**(0-255) (int)。你也可以通过statistics[1]获得。
- statistics.mode() 返回灰度的**众数**(0-255) (int)。你也可以通过statistics[2]获得。
- statistics.stdev() 返回灰度的**标准差**(0-255) (int)。你也可以通过statistics[3]获得。
- statistics.min() 返回灰度的**最小值**(0-255) (int)。你也可以通过statistics[4]获得。
- statistics.max() 返回灰度的**最大值**(0-255) (int)。你也可以通过statistics[5]获得。
- statistics.lq() 返回灰度的**第一四分数**(0-255) (int)。你也可以通过statistics[6]获得。
- statistics.uq() 返回灰度的**第三四分数**(0-255) (int)。你也可以通过statistics[7]获得。

上面的是灰度的值，接下来的

- l_mean，l_median，l_mode，l_stdev，l_min，l_max，l_lq，l_uq，
- a_mean，a_median，a_mode，a_stdev，a_min，a_max，a_lq，a_uq，
- b_mean，b_median，b_mode，b_stdev，b_min，b_max，b_lq，b_uq，

是LAB三个通道的平均数，中位数，众数，标准差，最小值，最大值，第一四分数，第三四分数。

## 3.3.检测左上方的区域中的颜色值。

检测左上方的区域中的颜色值。

```python
import sensor, image, time

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10) # 跳过10帧，使新设置生效
sensor.set_auto_whitebal(False)               # Create a clock object to track the FPS.

ROI=(80,30,15,15)

while(True):
    img = sensor.snapshot()         # Take a picture and return the image.
    statistics=img.get_statistics(roi=ROI)
    color_l=statistics.l_mode()
    color_a=statistics.a_mode()
    color_b=statistics.b_mode()
    print(color_l,color_a,color_b)
    img.draw_rectangle(ROI)
Copy
```

结果：

![img](https://book.openmv.cc/assets/05-03-002.jpg)

# 4.画图

- 颜色可以是灰度值(0-255)，或者是彩色值(r, g, b)的tupple。默认是白色。
- 其中的color关键字必须**显示**的标明**color=**。例如：

```
image.draw_line((10,10,20,30), color=(255,0,0))
image.draw_rectangle(rect_tuple, color=(255,0,0))
Copy
```

## 画线

- image.draw_line(line_tuple, color=White) 在图像中画一条直线。
  - line_tuple的格式是(x0, y0, x1, y1)，意思是(x0, y0)到(x1, y1)的直线。
  - 颜色可以是灰度值(0-255)，或者是彩色值(r, g, b)的tupple。默认是白色

## 画框

- image.draw_rectangle(rect_tuple, color=White) 在图像中画一个矩形框。
  - rect_tuple 的格式是 (x, y, w, h)。

## 画圆

- image.draw_circle(x, y, radius, color=White) 在图像中画一个圆。
  - x,y是圆心坐标
  - radius是圆的半径

## 画十字

- image.draw_cross(x, y, size=5, color=White) 在图像中画一个十字
  - x,y是坐标
  - size是两侧的尺寸

## 写字

- image.draw_string(x, y, text, color=White) 在图像中写字 8x10的像素
  - x,y是坐标。使用\n, \r, and \r\n会使光标移动到下一行。
  - text是要写的字符串。

## 例子

```python
# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time

sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10) # 跳过10帧，使新设置生效
while(True):
    img = sensor.snapshot()         # Take a picture and return the image.
    img.draw_line((20, 30, 40, 50))
    img.draw_line((80, 50, 100, 100), color=(255,0,0))
    img.draw_rectangle((20, 30, 41, 51), color=(255,0,0))
    img.draw_circle(50, 50, 30)
    img.draw_cross(90,60,size=10)
    img.draw_string(10,10, "hello world!")
Copy
```

![img](https://book.openmv.cc/assets/05-04-002.jpg)

## 5.find_blobs函数

追踪小球是OpenMV用的最多的功能了，在[10分钟快速上手](https://book.openmv.cc/quick-starter.html)中
通过find_blobs函数可以找到色块.我们来讨论一下，find_blobs的细节。

```
image.find_blobs(thresholds, roi=Auto, x_stride=2, y_stride=1, invert=False, area_threshold=10, pixels_threshold=10, merge=False, margin=0, threshold_cb=None, merge_cb=None)
Copy
```

这里的参数比较多。

- thresholds是颜色的阈值，注意：这个参数是一个列表，可以包含多个颜色。如果你只需要一个颜色，那么在这个列表中只需要有一个颜色值，如果你想要多个颜色阈值，那这个列表就需要多个颜色阈值。注意：在返回的色块对象blob可以调用code方法，来判断是什么颜色的色块。

```
red = (xxx,xxx,xxx,xxx,xxx,xxx)
blue = (xxx,xxx,xxx,xxx,xxx,xxx)
yellow = (xxx,xxx,xxx,xxx,xxx,xxx)

img=sensor.snapshot()
red_blobs = img.find_blobs([red])

color_blobs = img.find_blobs([red,blue, yellow])
Copy
```

- roi是“感兴趣区”。在[使用统计信息](https://book.openmv.cc/image/statistics.html)中已经介绍过了。

  left_roi = [0,0,160,240]
  blobs = img.find_blobs([red],roi=left_roi)

- x_stride 就是查找的色块的x方向上最小宽度的像素，默认为2，如果你只想查找宽度10个像素以上的色块，那么就设置这个参数为10：

  blobs = img.find_blobs([red],x_stride=10)

- y_stride 就是查找的色块的y方向上最小宽度的像素，默认为1，如果你只想查找宽度5个像素以上的色块，那么就设置这个参数为5：

  blobs = img.find_blobs([red],y_stride=5)

- invert 反转阈值，把阈值以外的颜色作为阈值进行查找

- area_threshold 面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉

- pixels_threshold 像素个数阈值，如果色块像素数量小于这个值，会被过滤掉

- merge 合并，如果设置为True，那么合并所有重叠的blob为一个。
  注意：这会合并所有的blob，无论是什么颜色的。如果你想混淆多种颜色的blob，只需要分别调用不同颜色阈值的find_blobs。

```
all_blobs = img.find_blobs([red,blue,yellow],merge=True)

red_blobs = img.find_blobs([red],merge=True)
blue_blobs = img.find_blobs([blue],merge=True)
yellow_blobs = img.find_blobs([yellow],merge=True)
Copy
```

- margin 边界，如果设置为1，那么两个blobs如果间距1一个像素点，也会被合并。

## 5.1.阈值

一个颜色阈值的结构是这样的：

```
red = (minL, maxL, minA, maxA, minB, maxB)
Copy
```

元组里面的数值分别是L A B 的最大值和最小值。

如果想在IDE的图像里获取这个阈值，见：[10分钟快速上手](https://book.openmv.cc/quick-starter.html)

在新版的IDE，有更方便的阈值选择工具，见下面。

## 5.2.颜色阈值选择工具

OpenMV 的IDE里加入了阈值选择工具，极大的方便了对于颜色阈值的调试。

首先运行hello world.py让IDE里的framebuffer显示图案。
![img](https://book.openmv.cc/assets/05-05-001.jpg)
然后打开 工具 → Mechine Vision → Threshold Editor
![img](https://book.openmv.cc/assets/05-05-002.jpg)

点击 Frame Buffer可以获取IDE中的图像，Image File可以自己选择一个图像文件。

![img](https://book.openmv.cc/assets/05-05-003.jpg)

拖动六个滑块，可以实时的看到阈值的结果，我们想要的结果就是，将我们的目标颜色变成白色，其他颜色全变为黑色。

![img](https://book.openmv.cc/assets/05-05-004.jpg)

## 5.4.blobs是一个列表

find_blobs对象返回的是多个blob的列表。（注意区分blobs和blob，这只是一个名字，用来区分多个色块，和一个色块）。
列表类似与C语言的数组，一个blobs列表里包含很多blob对象，blobs对象就是色块，每个blobs对象包含一个色块的信息。

```
blobs = img.find_blobs([red])
Copy
```

blobs就是很多色块。

可以用for循环把所有的色块找一遍。

```
for blob in blobs:
    print(blob.cx())
Copy
```

对于for循环的使用，见[python背景知识](https://book.openmv.cc/python-background.html)

## 5.5.blob色块对象

blob有多个方法：

- blob.rect() 返回这个色块的外框——矩形元组(x, y, w, h)，可以直接在image.draw_rectangle中使用。

- blob.x() 返回色块的外框的x坐标（int），也可以通过blob[0]来获取。

- blob.y() 返回色块的外框的y坐标（int），也可以通过blob[1]来获取。

- blob.w() 返回色块的外框的宽度w（int），也可以通过blob[2]来获取。

- blob.h() 返回色块的外框的高度h（int），也可以通过blob[3]来获取。

- blob.pixels() 返回色块的像素数量（int），也可以通过blob[4]来获取。

- blob.cx() 返回色块的外框的中心x坐标（int），也可以通过blob[5]来获取。

- blob.cy() 返回色块的外框的中心y坐标（int），也可以通过blob[6]来获取。

- blob.rotation() 返回色块的旋转角度（单位为弧度）（float）。如果色块类似一个铅笔，那么这个值为0~180°。如果色块是一个圆，那么这个值是无用的。如果色块完全没有对称性，那么你会得到0~360°，也可以通过blob[7]来获取。

- blob.code() 返回一个16bit数字，每一个bit会对应每一个阈值。举个例子：

  blobs = img.find_blobs([red, blue, yellow], merge=True)

如果这个色块是红色，那么它的code就是0001，如果是蓝色，那么它的code就是0010。注意：一个blob可能是合并的，如果是红色和蓝色的blob，那么这个blob就是0011。这个功能可以用于查找颜色代码。也可以通过blob[8]来获取。

- blob.count() 如果merge=True，那么就会有多个blob被合并到一个blob，这个函数返回的就是这个的数量。如果merge=False，那么返回值总是1。也可以通过blob[9]来获取。
- blob.area() 返回色块的外框的面积。应该等于(w * h)
- blob.density() 返回色块的密度。这等于色块的像素数除以外框的区域。如果密度较低，那么说明目标锁定的不是很好。
  比如，识别一个红色的圆，返回的blob.pixels()是目标圆的像素点数，blob.area()是圆的外接正方形的面积。

# 6.如何利用OpenMV进行测距

##### 视频教程10 - 测距以及测量物体大小：https://singtown.com/learn/50001/

##### 视频教程33 - ToF光学测距：https://singtown.com/learn/50539/

- 第一种方法：
  利用apriltag，Apriltag可以进行3D定位，具体实现参考我们的教程：
  AprilTag标记跟踪 http://book.openmv.cc/image/apriltag.html
- 第二种方法：
  OpenMV采用的是单目摄像头，想要实现测距，就需要选参照物，利用参照物的大小比例来计算距离。

本节分享一下第二种方法，如何通过摄像头里乒乓球的大小，计算摄像头与乒乓球之间的距离。

众所周知，乒乓球距离摄像头越远，摄像头里乒乓球的大小就越小，那么问题来了？
这个关系到底是什么呢？
（注：此处的数学几何问题，仅涉及到高中数学三角函数部分，不想看的，直接看结论也可）

为了简化问题，我们看一下图：
![img](https://book.openmv.cc/assets/05-09-001.jpg)

由左边的摄像头里的几何关系可得知：

![img](https://book.openmv.cc/assets/05-09-002.jpg)

所以有（1式）

![img](https://book.openmv.cc/assets/05-09-003.jpg)

由右边的真实环境里的几何关系得知：

![img](https://book.openmv.cc/assets/05-09-004.jpg)

带入（1式），可得（结论公式）：

![img](https://book.openmv.cc/assets/05-09-005.jpg)

上面就是最终我们想知道的关系啦！
这是什么意思呢？
等号左边的Lm是长度，Bpix是摄像头中，球所占的像素（直径的像素）。等号右边呢，Rm是球真实的半径，Apix是是固定的像素，a是视角的一半。
所以！所以！所以！所以！所以！所以！所以！
这个公式告诉我们的就是：

```
实际长度和摄像头里的像素成反比
```

简化就是

```
距离 = 一个常数/直径的像素
```

好啦，我们已经知道关系啦，而且还是这么的优雅简单！
具体操作步骤呢，就是先测出这个常数的值，怎么测不用说了吧，就是先让球距离摄像头10cm，打印出摄像头里直径的像素值，然后相乘，就得到了k的值！

然后 距离=这个常数/摄像头里像素点，so easy.



**三维空间中**

**d_pix= 根号（x^2 + y^2 + z^2）
K=实际距离/d_pix**

**K需自行校准**