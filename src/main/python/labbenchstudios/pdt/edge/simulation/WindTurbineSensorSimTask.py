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
import math
import random

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.edge.system.BaseSensorTask import BaseSensorTask
from labbenchstudios.pdt.data.SensorData import SensorData

class WindTurbineSensorSimTask(BaseSensorTask):
	"""
	This is a simple wrapper for a Simulator abstraction - it provides
	a container for the simulator's state, value, name, and status.
	
	"""

	def __init__(self, dataSet = None):
		super( \
			WindTurbineSensorSimTask, self).__init__( \
				name = ConfigConst.WIND_TURBINE_NAME, \
				typeID = ConfigConst.WIND_TURBINE_AIR_SPEED_SENSOR_TYPE, \
				typeCategoryID = ConfigConst.ENERGY_TYPE_CATEGORY, \
				dataSet = dataSet,
				minVal = 5.0,
				maxVal = 9.0)
		
		self._initDefaultValues()

	def enableBrakingSystem(self, enable: bool = False):
		"""
		"""
		self.enableBraking = enable

	def getPowerOutputTelemetry(self) -> SensorData:
		"""
		"""
		sensorData = SensorData()
		sensorData.updateData(self.getLatestTelemetry())
		#sensorData.setName(ConfigConst.POWER_OUTPUT_NAME)
		sensorData.setTypeID(ConfigConst.WIND_TURBINE_POWER_OUTPUT_SENSOR_TYPE)
		sensorData.setTypeCategoryID(self.getTypeCategoryID())
		sensorData.setValue(self.getPowerOutput())
		
		return sensorData

	def getRotationalSpeedTelemetry(self) -> SensorData:
		"""
		"""
		sensorData = SensorData()
		sensorData.updateData(self.latestSensorData)
		#sensorData.setName(ConfigConst.ROTATIONAL_SPEED_NAME)
		sensorData.setTypeID(ConfigConst.WIND_TURBINE_HUB_SPEED_SENSOR_TYPE)
		sensorData.setTypeCategoryID(self.getTypeCategoryID())
		sensorData.setValue(self.getCalculatedRotorHubRpm())

		return sensorData
	
	def getWindSpeedTelemetry(self) -> SensorData:
		"""
		"""
		sensorData = SensorData()
		sensorData.updateData(self.getLatestTelemetry())
		#sensorData.setName(ConfigConst.WIND_SPEED_NAME)
		sensorData.setTypeID(ConfigConst.WIND_TURBINE_AIR_SPEED_SENSOR_TYPE)
		sensorData.setTypeCategoryID(self.getTypeCategoryID())
		sensorData.setValue(self.getWindSpeed())
		
		return sensorData

	def getAirDensity(self) -> float:
		"""
		"""
		return self.airDensity
	
	def getMaxPowerCoefficient(self) -> float:
		"""
		"""
		return self.maxPowerCoeff
	
	def getOptimalTSR(self) -> float:
		"""
		"""
		return self.optimalTSR
	
	def getPowerOutput(self) -> float:
		"""
		"""
		return self.powerOutput
	
	def getRotorDiameter(self) -> float:
		"""
		"""
		return self.rotorDiameter
	
	def getRotorSweptArea(self) -> float:
		"""
		"""
		return self.rotorSweptArea
	
	def getWindSpeed(self) -> float:
		"""
		"""
		return self.windSpeed
	
	def getCalculatedRotorHubRpm(self) -> float:
		"""
		"""
		return self.rotorHubRpm
	
	def getCalculatedRotorTipSpeed(self) -> float:
		"""
		"""
		return self.rotorTipSpeed
	
	def _generateSensorReading(self, windSpeed: float = ConfigConst.DEFAULT_VAL) -> float:
		"""
		Creates a SensorData instance with the current simulator value
		and associated timestamp. If self.useRandomizer is enabled,
		power output will be calculated by using a random wind speed
		value for each query to this function ranging between
		self.minWindSpeed and self.maxWindSpeed.
		
		If self.dataSet is valid, the wind speed value will be extracted
		from the self.dataSet entries, and self.dataSetIndex will be
		incremented to the next index, up to size - 1, after which it
		simply will revert back to 0.
		
		Formula for calculating power from a wind turbine:
		  Algorithm: P = Cp * (p/2) * A * (V^3)
		  Reference: https://windexchange.energy.gov/small-wind-guidebook#generate

		  P = Power output in watts
		  Cp = Max power coefficient (0.25 - 0.45 for this module, fixed at 0.35)
		  p = Air density in kg/m3
		  A = Rotor swept area (m2 or (pi * D^2) / 4, where D is rotor diameter in m)
		  V = Wind speed in m/sec

		@return The SensorData instance.
		"""
		sensorData = SensorData(typeID = self.typeID, typeCategoryID = self.typeCategoryID, name = self.name)

		self.windSpeed = windSpeed

		# actual hub rotation will be different in a real life scenario
		# for now, just use the optimalTSR and windspeed to generate a value
		#
		# important: this does NOT factor in cut-in speed or cut-out speed
		#            for Digital Twin testing, cut-in and cut-out processes
		#            will be managed in the DTA

		if (self.enableBraking):
			self.rotorTipSpeed = 0.0
			self.rotorHubRpm = 0.0
		else:
			self.rotorTipSpeed = (60 * self.windSpeed * self.optimalTSR) / self.rotorCircumference
			self.rotorHubRpm = self.rotorTipSpeed / self.hubCircumference

		self.powerOutput = \
			self.maxPowerCoeff * (self.airDensity / 2) * self.rotorSweptArea * (pow(self.windSpeed, 3))
		
		logging.debug("\nCalculated wind turbine power output:" \
				"\n\tmaxPowerCoeff:    " + str(self.getMaxPowerCoefficient()) +
				"\n\tairDensity:       " + str(self.getAirDensity()) +
				"\n\trotorSweptArea:   " + str(self.getRotorSweptArea()) +
				"\n\twindSpeed:        " + str(self.getWindSpeed()) +
				"\n\tpowerOutputWatts: " + str(self.getPowerOutput()) +
				"\n\trotorTipSpeed:    " + str(self.getCalculatedRotorTipSpeed()) +
				"\n\thubRpm:           " + str(self.getCalculatedRotorHubRpm()) +
				"\n\tenableBraking:    " + str(self.enableBraking) +
				"\n\t")

		self.latestSensorData = sensorData
		
		return self.windSpeed
	
	def _initDefaultValues(self):
		"""
		Initialize default values for:
		  Max power coefficient
		  Rotor diameter (for this module it will be 5 meters)
		  Rotor swept area

		Value range for maximum power coefficient:
		  Algorithm: 0.25 to 0.45, with theoreticial max of 0.59
		  Reference: https://windexchange.energy.gov/small-wind-guidebook#generate
		
		Formula for calculating rotor swept area for a wind turbine:
		  Algorithm: (pi * D^2) / 4
		  Reference: https://windexchange.energy.gov/small-wind-guidebook#generate
		
		  D = rotor diameter in m

		Formula for calculating optimal TSR:
		  Algorithm: max power = (4 * pi) / n
		  Reference: https://www.reuk.co.uk/wordpress/wind/wind-turbine-tip-speed-ratio/

		  n = number of blades

	    For further documentation on typical cut-out and cut-in speeds,
        see https://www.energy.gov/eere/articles/how-do-wind-turbines-survive-severe-storms
		"""
		self.enableBraking = False
		self.powerOutput   = 0.0
		self.rotorHubRpm   = 0
		self.rotorTipSpeed = 0
		self.windSpeed     = 0.0

		# TODO: pull these from the config file
		self.rotorDiameter      = 8
		self.rotorCircumference = math.pi * self.rotorDiameter
		self.hubDiameter        = 2
		self.hubCircumference   = math.pi * self.hubDiameter
		
		self.airDensity         = 1.225
		self.maxPowerCoeff      = 0.35
		self.optimalTSR         = 5

		self.minRndWindSpeed = 5.0
		self.maxRndWindSpeed = 9.0

		self.cutInSpeed  = 5.0
		self.cutOutSpeed = 55.0

		self.rotorSweptArea  = (math.pi * (pow(self.rotorDiameter, 2))) / 4
