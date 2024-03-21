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

class DataValueContainer():
	"""
	
	"""
		
	def __init__(self):
		self.unit = ConfigConst.NOT_SET
		self.value = ConfigConst.DEFAULT_VAL
		self.targetValue = ConfigConst.DEFAULT_VAL
		self.nominalValueDelta = ConfigConst.DEFAULT_VAL
		self.maxValueDelta = ConfigConst.DEFAULT_VAL
		self.rangeMaxFloor = ConfigConst.DEFAULT_VAL
		self.rangeNominalFloor = ConfigConst.DEFAULT_VAL
		self.rangeMaxCeiling = ConfigConst.DEFAULT_VAL
		self.rangeNominalCeiling = ConfigConst.DEFAULT_VAL
	
	def getUnit(self) -> str:
		return self.unit
	
	def getValue(self) -> float:
		return self.value
	
	def getTargetValue(self) -> float:
		return self.targetValue
	
	def getNominalValueDelta(self) -> float:
		return self.nominalValueDelta
	
	def getMaxValueDelta(self) -> float:
		return self.maxValueDelta
	
	def getRangeMaxCeiling(self) -> float:
		return self.rangeMaxCeiling
	
	def getRangeNominalCeiling(self) -> float:
		return self.rangeNominalCeiling
	
	def getRangeMaxFloor(self) -> float:
		return self.rangeMaxFloor
	
	def getRangeNominalFloor(self) -> float:
		return self.rangeNominalFloor
	
	def setUnit(self, newVal: str):
		self.unit = newVal
		
	def setValue(self, newVal: float):
		self.value = newVal
		
	def getTargetValue(self, newVal: float):
		self.targetValue = newVal
		
	def getNominalValueDelta(self, newVal: float):
		self.nominalValueDelta = newVal
		
	def getMaxValueDelta(self, newVal: float):
		self.maxValueDelta = newVal
		
	def getRangeMaxCeiling(self, newVal: float):
		self.rangeMaxCeiling = newVal
		
	def getRangeNominalCeiling(self, newVal: float):
		self.rangeNominalCeiling = newVal
		
	def getRangeMaxFloor(self, newVal: float):
		self.rangeMaxFloor = newVal
		
	def getRangeNominalFloor(self, newVal: float):
		self.rangeNominalFloor = newVal
		
	def _handleUpdateData(self, data):
		if data and isinstance(data, DataValueContainer):
			self.unit = data.getValue()
			self.value = data.getValue()
			self.targetValue = data.getValue()
			self.nominalValueDelta = data.getValue()
			self.maxValueDelta = data.getValue()
			self.rangeMaxFloor = data.getValue()
			self.rangeNominalFloor = data.getValue()
			self.rangeMaxCeiling = data.getValue()
			self.rangeNominalCeiling = data.getValue()

	def __str__(self):
		"""
		String override function.
		
		"""
		s = '{}={},{}={},{}={},{}={},{}={},{}={},{}={},{}={},{}={}'
		
		return s.format(
			ConfigConst.UNIT_PROP, self.unit,
			ConfigConst.VALUE_PROP, self.value,
			ConfigConst.TARGET_VALUE_PROP, self.targetValue,
			ConfigConst.NOMINAL_VALUE_DELTA_PROP, self.nominalValueDelta,
			ConfigConst.MAX_VALUE_DELTA_PROP, self.maxValueDelta,
			ConfigConst.RANGE_MAX_FLOOR_PROP, self.rangeMaxFloor,
			ConfigConst.RANGE_NOMINAL_FLOOR_PROP, self.rangeNominalFloor,
			ConfigConst.RANGE_MAX_CEILING_PROP, self.rangeMaxCeiling,
			ConfigConst.RANGE_NOMINAL_CEILING_PROP, self.rangeNominalCeiling)
