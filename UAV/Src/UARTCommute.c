/**
  ******************************************************************************
  * 文件名          : UARTCommute.c
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
	
#include "UARTCommute.h"
#include <stdlib.h>
Remote_t Raw_Data;

int SPEEDLEVEL;
/**
* @brief 上位机串口速度信息接收
* @param None
* @retval None
*/
	int v,w;
void ROSReceiveHandle(){


}


/**
* @brief 上位机串口发送
* @param None
* @retval None
*/
void sendSerial(uint8_t* Data, uint8_t length){
	uint8_t sendData[20] = {0};
	sendData[0] = 0xFF;
	sendData[1] = 0xaa;
	sendData[2] = length;
  for(int i=0; i<length; i++){
	sendData[i+2] = Data[i];
	}
	HAL_UART_Transmit_DMA(&huart1,sendData,3+length);
}


/**
* @brief 串口校验位计算
* @param None
* @retval None
*/
uint8_t checkSum(uint8_t* data)
{
	uint8_t sum = 0;
	uint8_t length = data[2];
	for(int i=0;i<length;i++){
		sum+=data[i+2];
	}
	sum+=length;
	return sum;
}





