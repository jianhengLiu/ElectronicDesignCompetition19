/**
  ******************************************************************************
  * 文件名          : UARTCommute.h
  * 文件描述        : 机器人串口通讯管理模块
  * 创建时间        : 2019.0710
  * 作者            : 任云帆
  ******************************************************************************
  *								文件描述     								   *
  ******************************************************************************
  *	
	* 包含：
	*				用于与大疆遥控器通讯的UART1
	* 			用于与上位机通讯的UART2
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

#ifndef UARECOMMUTE_H
#define UARECOMMUTE_H


#include "usart.h"
#include "main.h"
#include "FlyInit.h"
#include <math.h>

#define CH0_BIAS 1024
#define CH1_BIAS 1024
#define CH2_BIAS 1024
#define CH3_BIAS 1024


typedef struct 
{
	int16_t ch0;
	int16_t ch1;
	int16_t ch2;
	int16_t ch3;
	int8_t left;
	int8_t right;
}Remote_t;



void RemoteReceiveHandle(void);
void GyroReceiveHandle(void);
void sendSerial(uint8_t* Data, uint8_t length);
void send_Encoder(void);
void ROSReceiveHandle(void);
#endif //UARECOMMUTE_H
