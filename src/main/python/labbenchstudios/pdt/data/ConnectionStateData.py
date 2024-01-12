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

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.data.IotDataContext import IotDataContext

class ConnectionStateData(IotDataContext):
	"""
	
	"""
	
	def __init__(self, \
		typeCategoryID: int = ConfigConst.SYSTEM_MGMT_TYPE, \
		typeID: int = ConfigConst.SYSTEM_MGMT_TYPE_CATEGORY, \
		name = ConfigConst.NOT_SET, \
		d = None):
		super(ConnectionStateData, self).__init__(\
			name = name, typeID = typeID, typeCategoryID = typeCategoryID, d = d)
		
		self.hostName = ConfigConst.DEFAULT_HOST
		self.hostPort = ConfigConst.DEFAULT_MQTT_PORT
		self.msgInCount = 0
		self.msgOutCount = 0
		self.isDisconnected = True
		self.isConnecting = False
		self.isConnected = False
	
	def getHostName(self) -> str:
		return self.hostName
	
	def getHostPort(self) -> int:
		return self.hostPort
	
	def getMessageInCount(self) -> int:
		return self.msgInCount
	
	def getMessageOutCount(self) -> int:
		return self.msgOutCount
	
	def isClientConnecting(self) -> bool:
		return self.isConnecting
	
	def isClientConnected(self) -> bool:
		return self.isConnected
	
	def isClientDisconnected(self) -> bool:
		return self.isDisconnected
	
	def setHostName(self, hostName: str):
		self.hostName = hostName
		self.updateTimeStamp()

	def setHostPort(self, port: int):
		self.hostPort = port
		self.updateTimeStamp()

	def setMessageInCount(self, val: int):
		self.msgInCount = val
		self.updateTimeStamp()

	def setMessageOutCount(self, val: int):
		self.msgOutCount = val
		self.updateTimeStamp()

	def setIsClientConnectingFlag(self, flag: bool):
		self.isConnecting = flag
		self.updateTimeStamp()

		if self.isConnecting:
			self.isConnected = False
			self.isDisconnected = False

	def setIsClientConnectedFlag(self, flag: bool):
		self.isConnected = flag
		self.updateTimeStamp()

		if self.isConnected:
			self.isConnecting = False
			self.isDisconnected = False
			
	def setIsClientDisconnectedFlag(self, flag: bool):
		self.isDisconnected = flag
		self.updateTimeStamp()

		if self.isDisconnected:
			self.isConnected = False
			self.isConnecting = False
			
	def _handleUpdateData(self, data):
		if data and isinstance(data, ConnectionStateData):
			self.hostName = data.getHostName()
			self.hostPort = data.getHostPort()
			self.msgInCount = data.getMessageInCount()
			self.msgOutCount = data.getMessageOutCount()
			self.isConnecting = data.isClientConnecting()
			self.isConnected = data.isClientConnected()
			self.isDisconnected = data.isClientDisconnected()

	def __str__(self):
		"""
		String override function.
		
		"""
		s = IotDataContext.__str__(self) + ',{}={},{}={},{}={},{}={},{}={},{}={},{}={}'
		
		return s.format(
			ConfigConst.HOST_NAME_PROP, self.hostName,
			ConfigConst.PORT_KEY, self.hostPort,
			ConfigConst.MESSAGE_IN_COUNT_PROP, self.msgInCount,
			ConfigConst.MESSAGE_OUT_COUNT_PROP, self.msgOutCount,
			ConfigConst.IS_CONNECTING_PROP, self.isConnecting,
			ConfigConst.IS_CONNECTED_PROP, self.isConnected,
			ConfigConst.IS_DISCONNECTED_PROP, self.isDisconnected)
