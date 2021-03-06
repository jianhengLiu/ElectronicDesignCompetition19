/**
  ******************************************************************************
  * 文件名          : Mission.h
  * 创建时间        : 2019.07.10
  * 作者            : 任云帆
  ******************************************************************************
  *								文件描述     								   *
  ******************************************************************************
  *	
	* 定义地盘全部功能
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




#ifndef MISSION_H
#define MISSION_H

#include "adc.h"
#include "tim.h"
void FlyMainTask(void);
void XY_feedback(void);
#endif //MISSION_H



