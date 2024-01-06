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

from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener
from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData
from labbenchstudios.pdt.common.ITelemetryDataListener import ITelemetryDataListener
from labbenchstudios.pdt.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener

class DefaultDataMessageListener(IDataMessageListener):
	"""
	Basic (default) implementation of the IDataMessageListener interface for testing.
	
	"""

	def __init__(self):
		"""
		Default constructor. This will set remote server information and client connection
		information based on the default configuration file contents.
		
		"""
		self.sysPerfDataListener = None
		self.telemetryDataListeners = {}
		
	def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
		"""
		Retrieves the named actuator data (response) item from the internal data cache.
		
		@param name
		@return ActuatorData
		"""
		pass
		
	def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
		"""
		Retrieves the named sensor data item from the internal data cache.
		
		@param name
		@return SensorData
		"""
		sd = SensorData()
		sd.setValue(15.0)
		
		return sd
	
	def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
		"""
		Retrieves the named system performance data from the internal data cache.
		
		@param name
		@return SystemPerformanceData
		"""
		pass
	
	def handleActuatorCommandMessage(self, data: ActuatorData) -> bool:
		"""
		Callback function to handle an actuator command message packaged as a ActuatorData object.
		
		@param data The ActuatorData message received.
		@return bool True on success; False otherwise.
		"""
		if data:
			logging.info('Actuator Command Msg: ' + str(data.getCommand()))
			
		return True
	
	def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
		"""
		Callback function to handle an actuator command response packaged as a ActuatorData object.
		
		@param data The ActuatorData message received.
		@return bool True on success; False otherwise.
		"""
		if data:
			logging.info('Actuator Command: ' + str(data.getCommand()))
			
		return True
	
	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		"""
		Callback function to handle incoming messages on a given topic with
		a string-based payload.
		
		@param resourceEnum The topic enum associated with this message.
		@param msg The message received. It is expected to be in JSON format.
		@return bool True on success; False otherwise.
		"""
		logging.info('Topic: %s  Message: %s', resourceEnum.value(), msg)
		return True

	def handleSensorMessage(self, data: SensorData) -> bool:
		"""
		Callback function to handle a sensor message packaged as a SensorData object.
		
		@param data The SensorData message received.
		@return bool True on success; False otherwise.
		"""
		if data:
			logging.info('Sensor Message: ' + str(data))
			
			if data.getName() in self.telemetryDataListeners:
				self.telemetryDataListeners[data.getName()].onSensorDataUpdate(data)
			
		return True
	
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
		"""
		Callback function to handle a system performance message packaged as
		SystemPerformanceData object.
		
		@param data The SystemPerformanceData message received.
		@return bool True on success; False otherwise.
		"""
		if data:
			logging.info('System Performance Message: ' + str(data))
			
			if self.sysPerfDataListener:
				self.sysPerfDataListener.onSystemPerformanceDataUpdate(data)
				
		return True
	
	def setSystemPerformanceDataListener(self, listener: ISystemPerformanceDataListener = None):
		"""
		Setter for the ITelemetryDataListener for system performance data.
		
		@param listener
		"""
		if listener:
			self.sysPerfDataListener = listener
			
	def setTelemetryDataListener(self, name: str = None, listener: ITelemetryDataListener = None):
		"""
		Sets the named telemetry data listener. The listener's callback function will be invoked
		when telemetry data is available for the given name.
		
		@param name The name of the listener.
		@param listener The listener reference.
		"""
		if listener:
			self.telemetryDataListeners[name] = listener
			