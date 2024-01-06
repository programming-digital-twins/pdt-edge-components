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

class ActuatorData(IotDataContext):
	"""
	
	"""

	def __init__(self, \
		typeCategoryID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, \
		typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, \
		name = ConfigConst.NOT_SET, \
		d = None):
		super(ActuatorData, self).__init__(
			name = name, typeID = typeID, typeCategoryID = typeCategoryID, d = d)
		
		self.value = ConfigConst.DEFAULT_VAL
		self.command = ConfigConst.DEFAULT_COMMAND
		self.stateData = None
		self.isResponse = False
		
	def getCommand(self) -> int:
		return self.command
	
	def getStateData(self) -> str:
		return self.stateData
	
	def getValue(self) -> float:
		return self.value
	
	def isResponseFlagEnabled(self) -> bool:
		return self.isResponse
	
	def setCommand(self, command: int):
		self.command = command
		self.updateTimeStamp()
	
	def setAsResponse(self):
		self.isResponse = True
		self.updateTimeStamp()
		
	def setStateData(self, stateData: str):
		if stateData:
			self.stateData = stateData
			self.updateTimeStamp()
	
	def setValue(self, val: float):
		self.value = val
		self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		if data and isinstance(data, ActuatorData):
			self.command = data.getCommand()
			self.stateData = data.getStateData()
			self.value = data.getValue()
			self.isResponse = data.isResponseFlagEnabled()
		
	def __str__(self):
		"""
		Returns a string representation of this instance.
		
		@return The string representing this instance.
		"""
		s = IotDataContext.__str__(self) + ',{}={},{}={},{}={},{}={}'
		
		return s.format(
			ConfigConst.COMMAND_PROP, self.command,
			ConfigConst.STATE_DATA_PROP, self.stateData,
			ConfigConst.VALUE_PROP, self.value,
			ConfigConst.IS_RESPONSE_PROP, self.isResponse)
