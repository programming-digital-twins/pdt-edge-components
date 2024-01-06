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

from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.common.ISensorTask import ISensorTask

class BaseSystemUtilTask(ISensorTask):
	"""
	Shell implementation representation of class for student implementation.
	
	"""
	
	def __init__(self, name = ConfigConst.NOT_SET, typeID = ConfigConst.DEFAULT_SENSOR_TYPE):
		self.name = name
		self.typeID = typeID
		self.value = ConfigConst.DEFAULT_VAL

		self.latestSensorData = None
		
	def generateTelemetry(self) -> SensorData:
		"""
		Creates a SensorData instance using the latest telemetry value fromn the
		underlying system data. This is usually extracted via the getTelemetryValue()
		method.

		This will NOT force a call to the underlying system to generate a new telemetry
		value, only a new telemetry data wrapper (SensorData) from the previously cached
		telemetry value.
		
		@return The (possibly updated) latest SensorData instance.
		"""
		sensorData = SensorData(typeID = self.typeID, name = self.name)
		sensorData.setValue(self.value)
		
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
		Returns the name set during construction.
		
		@return name As a string.
		"""
		return self.name
	
	def getTypeID(self) -> int:
		"""
		Returns the type ID set during construction.

		@return typeID as an int.
		"""
		return self.typeID
	
	def getTelemetryValue(self) -> float:
		"""
		This triggers a call to the template method _handleGetTelemetryValue(),
		which is implemented by the sub-class.

		@return float The latest telemetry value, as a float.
		"""
		return self._handleGetTelemetryValue()

	def _handleGetTelemetryValue(self) -> float:
		"""
		Template method defintion to be implemented by the sub-class.
		
		@return float The latest telemetry value, as a float.
		"""
		pass
	