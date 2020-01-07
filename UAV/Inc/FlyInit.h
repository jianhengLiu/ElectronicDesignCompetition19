/**
  ******************************************************************************
  * 文件名          : ChassisInit.h
  * 创建时间        : 2019.07.10
  * 作者            : 任云帆
  ******************************************************************************
  *								文件描述     								   *
  ******************************************************************************
  *	
	* 本文件定义了底盘所有的全局变量和初始化函数。
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
	
	
#ifndef FLY_H
#define FLY_H
#include "main.h"
#define NOW  1
#define LAST 0

/**
* @brief 底盘工作状态枚举类型
* @param None
* @retval None
*/
typedef enum 
{
	STOP,	
	LAND,
	LAUNCH,
	OpenMV,
	STM32,
	State_error
}WorkState_e;

/**
* @brief PID结构体
* @param None
* @retval None
*/
typedef struct 
{
	int32_t msg_cnt;
	float real_w;
	int32_t DeltaPosbuf[30];
	int8_t PosIndex;
	float round_wheel;
	int32_t fdbPos[2];
	int32_t offsetPos;
	int32_t real_pos[2];
	int fdb_Vol;
	
	float real_angle;
	int16_t round;
	
	float KP;
	float KI;
	float KD;
	int fdb;
	int error[2];
	
	int ref;
	
	int cur_error;
	int output;
	int outputMax;
	
	int fdb_v;
}PID_t;

/**
* @brief 遥控器接收数据解析结构体
* @param None
* @retval None
*/
typedef struct 
{
    int YSpeed;
    int XSpeed;
    int YawSpeed;
}Target_t;

/**
* @brief 底盘全部参数结构体
* @param None
* @retval None
*/
typedef struct
{
	Target_t Target;
	PID_t Motor;
	WorkState_e WorkState;
}Fly_t;

void FlyInit(void);
extern Fly_t Fly;
extern uint8_t UsartReceive2[18]; 
extern int Controller[2];
extern uint8_t UsartReceive1[4];				 
extern uint8_t CanReceiveData[8]; 
#endif 	//FLY_H

