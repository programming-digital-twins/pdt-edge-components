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
import random

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.common.ISensorTask import ISensorTask

class BaseSensorTask(ISensorTask):
	DEFAULT_MIN_VAL = 0.0
	DEFAULT_MAX_VAL = 1000.0
	
	def __init__(self, \
	    	name = ConfigConst.NOT_SET, \
			typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, \
			typeCategoryID: int = ConfigConst.DEFAULT_TYPE_CATEGORY_ID, \
			dataSet = None, \
			minVal: float = DEFAULT_MIN_VAL, \
			maxVal: float = DEFAULT_MAX_VAL):
		"""
		Constructor.
		
		@param dataSet Defaults to None. Instance of SensorDataSet containing
		time-series data represented by timeEntries array and dataEntries array.
		"""
		self.dataSet = dataSet
		self.name = name
		self.typeID = typeID
		self.typeCategoryID = typeCategoryID
		self.dataSetIndex = 0
		self.useRandomizer = False
		self.enableDataRoll = True
		
		self.latestSensorData = None
		
		if not self.dataSet:
			self.useRandomizer = True
			self.minVal = minVal
			self.maxVal = maxVal
	
	def enableSimulatedDataRollover(self, enable: bool = True):
		"""
		"""
		self.enableDataRoll = enable
		
	def generateTelemetry(self) -> SensorData:
		"""
		Creates a SensorData instance with the current simulator value
		and associated timestamp. If self.useRandomizer is enabled, a random
		value between self.minVal and self.maxVal will be generated along
		with the current time stamp. If self.dataSet is valid, the data
		and time entries associated with self.dataSetIndex will be used,
		and self.dataSetIndex will be incremented to the next index, up
		to size - 1, after which it will revert back to 0.
		
		@return The SensorData instance.
		"""
		sensorData = SensorData(typeID = self.typeID, typeCategoryID = self.typeCategoryID, name = self.name)
		sensorVal = ConfigConst.DEFAULT_VAL
		
		if self.useRandomizer:
			sensorVal = random.uniform(self.minVal, self.maxVal)
		else:
			sensorVal = self.dataSet.getDataEntry(index = self.dataSetIndex)
			self.dataSetIndex = self.dataSetIndex + 1
			
			if self.dataSetIndex >= self.dataSet.getDataEntryCount() - 1:
				if (self.enableDataRoll):
					self.dataSetIndex = 0
				else:
					self.dataSetIndex = self.dataSet.getDataEntryCount() - 1
				
		sensorData.setValue(sensorVal)
		
		self.latestSensorData = sensorData
		
		return self.latestSensorData
	
	def getLatestTelemetry(self) -> SensorData:
		"""
		Returns a newly created SensorData instance as a copy
		of the latest telemetry data generated.
		
		If no telemetry has been generated when this method is
		called, None is returned.
		
		@return SensorData
		"""
		if self.latestSensorData:
			sdCopy = SensorData()
			sdCopy.updateData(self.latestSensorData)
			
			return sdCopy
		
		return None
	
	def getName(self) -> str:
		"""
		Returns the name of this simulator.
		
		@return str
		"""
		return self.name
	
	def getTypeID(self) -> int:
		"""
		Returns the type ID of this simulator.
		
		@return int
		"""
		return self.typeID
	
	def getTypeCategoryID(self) -> int:
		"""
		Returns the type category ID of this task.
		
		@return int
		"""
		return self.typeCategoryID
	
	def getTelemetryValue(self) -> float:
		"""
		Returns the current value from the stored self.latestSensorData instance.
		If it hasn't been generated yet, this will invoke self.generateTelemetry()
		and then return the current value from the generated SensorData.
		
		@return float
		"""
		if not self.latestSensorData:
			self.generateTelemetry()
		
		return self.latestSensorData.getValue()
