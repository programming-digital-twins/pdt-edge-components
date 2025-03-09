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

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.edge.system.BaseSensorTask import BaseSensorTask
from labbenchstudios.pdt.data.SensorData import SensorData

class FactoryWorkcellSimTask(BaseSensorTask):
	"""
	This is a simple wrapper for a Simulator abstraction - it provides
	a container for the simulator's state, value, name, and status.
	
	"""

	def __init__(self, \
		configSection: str = ConfigConst.FACTORY_WORKCELL_SETTINGS_KEY, \
		name: str = "FactoryWorkcell", \
		typeName: str = "boxProduction", \
		typeID = ConfigConst.FACTORY_WORKCELL_GENERIC_TYPE):
		super( \
			FactoryWorkcellSimTask, self).__init__( \
				name = name, \
				typeName = typeName, \
				typeID = typeID, \
				typeCategoryID = ConfigConst.FACTORY_WORKCELL_TYPE_CATEGORY)
		
		self._initDefaultValues()

	def getPowerDrawTelemetrySensorData(self) -> SensorData:
		"""
		"""
		# generate random float between 2.0 and 3.0 (KW)
		sensorData = \
			self.generateTelemetry( \
				typeID = ConfigConst.FACTORY_WORKCELL_POWER_DRAW_TYPE, \
				typeName = ConfigConst.POWER_DRAW_NAME, \
				minVal = 2.0, \
				maxVal = 3.0)
		
		return sensorData

	def getAmbientTemperatureTelemetrySensorData(self) -> SensorData:
		"""
		"""
		# generate random float between 18.0 and 22.0 (C)
		sensorData = \
			self.generateTelemetry( \
				typeID = ConfigConst.FACTORY_WORKCELL_AMBIENT_TEMP_TYPE, \
				typeName = ConfigConst.AMBIENT_TEMPERATURE_NAME, \
				minVal = 18.0, \
				maxVal = 22.0)

		return sensorData
	
	def getCurrentItemsProducedSensorData(self) -> SensorData:
		"""
		"""
		sensorData = \
			self.generateTelemetry( \
				typeID = ConfigConst.FACTORY_WORKCELL_ITEMS_PRODUCED_TYPE, \
				typeName = ConfigConst.ITEMS_PRODUCED_NAME, \
				minVal = float(self.minItemProdRate), \
				maxVal = float(self.maxItemProdRate))

		# the value from generateTelemetry will be randomly calculated
		# as a float betweein minVal and maxVal - override it to set
		# the actual items produced value instead
		sensorData.setValue(self.itemProductionCounter)

		return sensorData
	
	def getCurrentItemsProducedAsValue(self) -> int:
		"""
		"""
		return self.itemProductionCounter
	
	def getDefaultItemsProducedPerMinute(self) -> float:
		"""
		"""
		return self.defaultItemProdRate
	
	def getMinItemsProducedPerMinute(self) -> float:
		"""
		"""
		return self.minItemProdRate
	
	def getMaxItemsProducedPerMinute(self) -> float:
		"""
		"""
		return self.maxItemProdRate
	
	def isProductionPaused(self):
		"""
		"""
		return self.pauseProduction
	
	def setProductionPauseFlag(self, enable: bool = False):
		"""
		"""
		self.pauseProduction = enable

	def _generateSensorReading(self, sensorVal: float = ConfigConst.DEFAULT_VAL) -> float:
		"""
		This call simply increments the itemProductionCounter if production is NOT paused.
		If production is paused, no action is taken.
		"""
		if not self.pauseProduction:
			self.itemProductionCounter += 1

		return float(self.itemProductionCounter)

	def _initDefaultValues(self):
		"""
		"""
		self.itemProductionCounter = 0

		self.configUtil = ConfigUtil()
		
		self.locationID = \
			self.configUtil.getProperty( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		self.enableCommandName = \
			self.configUtil.getProperty( \
				section = ConfigConst.FACTORY_WORKCELL_SETTINGS_KEY, key = ConfigConst.ENABLE_COMMAND_NAME_KEY, defaultVal = ConfigConst.NOT_SET)
		
		self.minItemProdRate   = \
			self.configUtil.getFloat( \
				section = ConfigConst.FACTORY_WORKCELL_SETTINGS_KEY, key = ConfigConst.MIN_PRODUCTION_RATE_KEY, defaultVal = 1.0)

		self.maxItemProdRate   = \
			self.configUtil.getFloat( \
				section = ConfigConst.FACTORY_WORKCELL_SETTINGS_KEY, key = ConfigConst.MAX_PRODUCTION_RATE_KEY, defaultVal = 60.0)
		
		self.defaultItemProdRate = \
			self.configUtil.getFloat( \
				section = ConfigConst.FACTORY_WORKCELL_SETTINGS_KEY, key = ConfigConst.DEFAULT_PRODUCTION_RATE_KEY, defaultVal = 30.0)
