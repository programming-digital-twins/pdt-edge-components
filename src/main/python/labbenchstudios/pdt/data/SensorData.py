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

class SensorData(IotDataContext):
	"""
	
	"""
		
	def __init__(self, \
		typeCategoryID: int = ConfigConst.DEFAULT_SENSOR_TYPE, \
		typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, \
		name = ConfigConst.NOT_SET, \
		d = None):
		super(SensorData, self).__init__(\
			name = name, typeID = typeID, typeCategoryID = typeCategoryID, d = d)
		
		self.value = ConfigConst.DEFAULT_VAL
	
	def getValue(self) -> float:
		return self.value
	
	def setValue(self, newVal: float):
		self.value = newVal
		self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		if data and isinstance(data, SensorData):
			self.value = data.getValue()

	def __str__(self):
		"""
		String override function.
		
		"""
		s = IotDataContext.__str__(self) + ',{}={}'
		
		return s.format(
			ConfigConst.VALUE_PROP, self.value)
