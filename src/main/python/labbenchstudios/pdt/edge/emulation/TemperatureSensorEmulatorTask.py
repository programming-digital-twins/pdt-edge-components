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

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.edge.system.BaseSensorTask import BaseSensorTask

from pisense import SenseHAT

class TemperatureSensorEmulatorTask(BaseSensorTask):
	"""
	Implementation of the named task.
	
	"""

	def __init__(self):
		"""
		Constructor.
		
		@param dataSet The SensorDataSet to use for this task simulator.
		"""
		super( \
			TemperatureSensorEmulatorTask, self).__init__( \
				name = ConfigConst.TEMP_SENSOR_NAME, \
				typeID = ConfigConst.TEMP_SENSOR_TYPE, \
				typeCategoryID = ConfigConst.ENV_TYPE_CATEGORY)
		
		enableEmulation = \
			ConfigUtil().getBoolean( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate = enableEmulation)
	
	def generateTelemetry(self) -> SensorData:
		"""
		Creates a SensorData instance with the current emulator value
		and associated timestamp.
		
		@return The SensorData instance.
		"""
		sensorData = SensorData(name = self.getName() , typeID = self.getTypeID())
		sensorVal = self.sh.environ.temperature
				
		sensorData.setValue(sensorVal)
		
		self.latestSensorData = sensorData
		
		return sensorData
