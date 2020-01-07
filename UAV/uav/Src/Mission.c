/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : Mission.c
  * @brief          : Mavlink main body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */

#include "Mission.h"

#include "Mavlink.h"

mavlink_status_t status;
mavlink_message_t msg;
int chan = MAVLINK_COMM_0;

void decode(){

	while(serial.bytesAvailable > 0)
	{
		uint8_t byte = serial.getNextByte();
		if (mavlink_parse_char(chan, byte, &msg, &status))
			{
			printf("Received message with ID %d, sequence: %d from component %d of system %d\n", msg.msgid, msg.seq, msg.compid, msg.sysid);
			// ... DECODE THE MESSAGE PAYLOAD HERE ...
			}
	}
	
}

