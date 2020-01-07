/**
  ******************************************************************************
  * 文件名          : Calculate.h
  * 文件描述        : 机器人的各个参数计算
  * 创建时间        : 2019.0710
  * 作者            : 任云帆
  ******************************************************************************
  *								文件描述     								   *
  ******************************************************************************
  *	
	* 本文件定义了底盘的电机PID
	*
  ******************************************************************************
  * 1.本代码基于STM32F427IIH6开发，编译环境为Keil 5。
  * 2.本代码只适用于WTRobot一代全向底盘，不建议用作其他用途
  * 3.本代码以UTF-8格式编码，请勿以ANSI编码形式打开
  * 4.本代码最终解释权归哈尔滨工业大学（深圳）南工问天战队所有
  *
  * Copyright (c) 2019 哈尔滨工业大学（深圳）南工问天战队 版权所有
  ******************************************************************************
  */

#ifndef CALCULATE_H
#define CALCULATE_H
#include "main.h"
#include "CanCommute.h"
#include "FlyInit.h"
#include <math.h>
#include <stdlib.h>



void PID_Calc(PID_t *pid);
void FourWheelVellControl(double x,double y,double a);
void Calculate(void);


#endif  	//CALCULATE_H



