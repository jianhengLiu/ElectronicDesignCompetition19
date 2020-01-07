/**
  ******************************************************************************
  * 文件名          : Mission.c
  * 创建时间        : 2019.07.10
  * 作者            : 任云帆
  ******************************************************************************
  *								文件描述     								   *
  ******************************************************************************
  *	
	* 定义底盘所有功能
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
	
#include "Mission.h"


int Controller[2];
int flag = 0;
void FlyMainTask()
{
		for(uint8_t i=0;i<2;i++)
		{
			HAL_ADC_Start(&hadc1);
			HAL_ADC_PollForConversion(&hadc1,10);
			Controller[i]=HAL_ADC_GetValue(&hadc1)/100;
			HAL_Delay(1);
		}
			XY_feedback();
	
}

void XY_feedback()
{
	if(Controller[0]<25&&Controller[1]<25&&Controller[0]>15&&Controller[1]>15)
	{
		__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1,140);
	}
	else if(Controller[0]<15&&Controller[1]>25)
	{
		__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1,160);
	}
	else if(Controller[0]>25&&Controller[1]>25)
	{
		__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1,120);
	}
	else if(Controller[1]<15)
	{
		__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1,100);
	}
	
}
