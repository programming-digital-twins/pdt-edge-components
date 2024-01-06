##
# MIT License
# 
# Copyright (c) 2020 - 2024 Andrew D. King
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import logging

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.common.IActuatorTask import IActuatorTask

class BaseActuatorTask(IActuatorTask):
	def __init__(self, \
			name: str = ConfigConst.NOT_SET, \
			typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, \
			typeCategoryID = ConfigConst.DEFAULT_TYPE_CATEGORY_ID, \
			simpleName: str = "Actuator"):
		"""
		Constructor.
		
		@param actuatorType The int representing the type of the actuator.
		"""
		self.latestActuatorResponse = ActuatorData(typeID = typeID, name = name)
		self.latestActuatorResponse.setAsResponse()
		
		self.name = name
		self.typeID = typeID
		self.typeCategoryID = typeCategoryID
		self.simpleName = simpleName
		self.lastKnownCommand = ConfigConst.DEFAULT_COMMAND
		self.lastKnownValue = ConfigConst.DEFAULT_VAL
		self.ignoreTypeID = False
		
	def getLatestResponse(self) -> ActuatorData:
		"""
		Returns a newly created ActuatorData instance as a copy
		of the latest actuator response data generated.
		
		@return ActuatorData
		"""
		if self.latestActuatorResponse:
			adCopy = ActuatorData()
			adCopy.updateData(self.latestActuatorResponse)
			
			return adCopy
		
		return None
	
	def getName(self) -> str:
		"""
		Returns the name of this simulator.
		
		@return str
		"""
		return self.name
	
	def getSimpleName(self) -> str:
		"""
		Returns the simplified name passed in from the sub-class.
		
		@return String
		"""
		return self.simpleName
	
	def getTypeID(self) -> int:
		"""
		Returns the type ID of this actuator.
		
		@return int
		"""
		return self.typeID
	
	def getTypeCategoryID(self) -> int:
		"""
		Returns the type category ID of this task.
		
		@return int
		"""
		return self.getTypeCategoryID
	
	def updateActuator(self, data: ActuatorData) -> ActuatorData:
		"""
		Updates the actuator state using the given ActuatorData.
		Performs basic validation internally - optionally, add a
		template method definition (e.g. def _validateData(data: ActuatorData) -> bool:),
		call, which can be overridden by the sub-class if needed.
		May also trigger a call to activate or deactivate the
		actuator, depending upon the command within data.
		
		This will setup the actuation call after validating
		'data', then invoke the 'private' _handleActuation() method,
		which in turn returns the status code to be used in the
		response data.
		
		@param data The ActuatorData to process.
		@return ActuatorData A new ActuatorData updated with the original command and the response flag enabled.
		"""
		if self.ignoreTypeID:
			allowActuation = True
		else:
			allowActuation = (self.typeID == data.getTypeID())

		if data and allowActuation:
			statusCode = ConfigConst.DEFAULT_STATUS
			
			curCommand = data.getCommand()
			curVal     = data.getValue()
			
			if self.typeID == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE:
				statusCode = self._activateActuator(val = data.getValue(), stateData = data.getStateData())
				return None
			
			# check if the command or value is a repeat from previous
			# if so, ignore the command and return None to caller
			#
			# but - whether ON or OFF - allow a new value to be set
			if curCommand == self.lastKnownCommand and curVal == self.lastKnownValue:
				logging.debug( \
					"New actuator command and value is a repeat. Ignoring: %s %s", \
					str(curCommand), str(curVal))
			else:
				logging.debug( \
					"New actuator command and value to be applied: %s %s", \
					str(curCommand), str(curVal))
				
				if curCommand == ConfigConst.DEFAULT_COMMAND:
					curCommand = ConfigConst.COMMAND_ON
					
				if curCommand == ConfigConst.COMMAND_ON:
					logging.info("Activating actuator...")
					statusCode = self._activateActuator(val = data.getValue(), stateData = data.getStateData())
				elif curCommand == ConfigConst.COMMAND_OFF:
					logging.info("Deactivating actuator...")
					statusCode = self._deactivateActuator(val = data.getValue(), stateData = data.getStateData())
				else:
					logging.warning("ActuatorData command is unknown. Ignoring: %s", str(curCommand))
					statusCode = -1
				
				# update the last known actuator command and value
				self.lastKnownCommand = curCommand
				self.lastKnownValue = curVal
				
				# create the ActuatorData response from the original command
				actuatorResponse = ActuatorData()
				actuatorResponse.updateData(data)
				actuatorResponse.setStatusCode(statusCode)
				actuatorResponse.setAsResponse()
				
				self.latestActuatorResponse.updateData(actuatorResponse)
				
				return actuatorResponse
			
		return None
	
	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Sets the actuator to 'on', or 'activated' with the
		associated value.
		
		For example, this can be used to instruct an actuator
		to open a valve 50%, or 100%.
		
		@param val The float value associated with the command.
		@return bool True on successful set; False otherwise.
		"""
		msg = "\n*******"
		msg = msg + "\n* O N *"
		msg = msg + "\n*******"
		
		msg = msg + "\n" + self.name + " VALUE -> " + str(val) + "\n======="
			
		logging.info("Simulating %s actuator ON: %s", self.name, msg)
		
		return 0
		
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Sets the actuator to 'off', or 'deactivated'.
		
		For example, this can be used to instruct an actuator
		to turn back to its off or disabled state from whatever
		value it's currently set to. That is, if it's a valve
		that's open at n%, it will simply be closed completely.
		
		@return bool True on successful set; False otherwise.
		"""
		msg = "\n*******"
		msg = msg + "\n* OFF *"
		msg = msg + "\n*******"
		
		logging.info("Simulating %s actuator OFF: %s", self.name, msg)
				
		return 0
	
	def _setDisableTypeCheckFlag(self, enable: bool = False):
		"""
		"""
		self.ignoreTypeID = enable
