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

import datetime

from labbenchstudios.pdt.common.ResourceNameContainer import ResourceNameContainer
from labbenchstudios.pdt.common.IDataLoader import IDataLoader
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.ConnectionStateData import ConnectionStateData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class IPersistenceClient(IDataLoader):
	"""
	Interface definition for persistence clients.
	
	"""
	
	def connectClient(self) -> bool:
		"""
		Connects to the persistence server using configuration parameters
		specified by the sub-class.
		
		@return bool True on success; False otherwise.
		"""
		pass

	def disconnectClient(self) -> bool:
		"""
		Disconnects from the persistence server if the client is already connected.
		If not, this call is ignored, but will return a False.
		
		@return bool True on success; False otherwise.
		"""
		pass
	
	def storeActuatorData(self, resource: ResourceNameContainer = None, qos: int = 0, data: ActuatorData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""

	def storeConnectionStateData(self, resource: ResourceNameContainer = None, qos: int = 0, data: ConnectionStateData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""

	def storeSensorData(self, resource: ResourceNameContainer = None, qos: int = 0, data: SensorData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""

	def storeSystemPerformanceData(self, resource: ResourceNameContainer = None, qos: int = 0, data: SystemPerformanceData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""

	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		"""
		Sets the data message listener reference, assuming listener is non-null.
		
		@param listener The data message listener instance to use for passing relevant
		messages, such as those received from a subscription event.
		@return bool True on success (if listener is non-null will always be the case); False otherwise.
		"""
		pass
	