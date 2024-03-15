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

from importlib import import_module

from apscheduler.schedulers.background import BackgroundScheduler

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.IDataManager import IDataManager
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener
from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData

from labbenchstudios.pdt.edge.simulation.SensorDataGenerator import SensorDataGenerator
from labbenchstudios.pdt.edge.simulation.HumiditySensorSimTask import HumiditySensorSimTask
from labbenchstudios.pdt.edge.simulation.TemperatureSensorSimTask import TemperatureSensorSimTask
from labbenchstudios.pdt.edge.simulation.PressureSensorSimTask import PressureSensorSimTask

class SensorAdapterManager(IDataManager):
	"""
	Manager class for running any sensor simulators or actual
	sensor integration logic within a scheduled polling system.
	
	"""
	
	def __init__(self):
		"""
		Constructor.
		
		"""
		self.configUtil = ConfigUtil()
		
		self.pollRate     = \
			self.configUtil.getInteger( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
			
		self.useEmulator  = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_EMULATOR_KEY)
			
		self.locationID   = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
			
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
			
		# technically we only need 1 instance - important to set coalesce
		# to True and allow for misfire grace period
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job( \
			self.handleTelemetry, 'interval', seconds = self.pollRate, max_instances = 2, coalesce = True, misfire_grace_time = 15)
		
		self.dataMsgListener = None
		
		#
		# NOTE: New config property added into baseline
		#
		self.useSimulator = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SIMULATOR_KEY)
			
		self.useSenseHat = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SENSE_HAT_KEY)
			
		self.deviceID = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		#
		# FUTURE: use with labmodule04 only IFF connected to RPi
		#
		self.useSenseHatI2CBus = False
		
		self.resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
		#self.resource.setAsSensingResource(True)
		#self.resource.setDeviceName(self.deviceID)
		#self.resource.setResourceType(ConfigConst.SENSOR_MSG)
		
		self.isEnvSensingActive = False
		
		# see PIOT-CDA-03-006 description for thoughts on the next line of code
		self._initEnvironmentalSensorTasks()
		
	def handleTelemetry(self):
		"""
		Callback function used by the scheduler to invoke the retrieval
		of telemetry from any simulated or actual sensors. Once data
		is retrieved, the data listener will be invoked.
		
		"""
		if self.isEnvSensingActive:
			humidityData = self.humidityAdapter.generateTelemetry()
			pressureData = self.pressureAdapter.generateTelemetry()
			tempData     = self.tempAdapter.generateTelemetry()
			
			humidityData.setDeviceID(self.deviceID)
			humidityData.setLocationID(self.locationID)

			pressureData.setDeviceID(self.deviceID)
			pressureData.setLocationID(self.locationID)
			
			tempData.setDeviceID(self.deviceID)
			tempData.setLocationID(self.locationID)
			
			logging.debug('Generated humidity data: ' + str(humidityData.getValue()))
			logging.debug('Generated pressure data: ' + str(pressureData.getValue()))
			logging.debug('Generated temp data: ' + str(tempData.getValue()))
			
			if self.dataMsgListener:
				self.dataMsgListener.handleSensorMessage(humidityData)
				self.dataMsgListener.handleSensorMessage(pressureData)
				self.dataMsgListener.handleSensorMessage(tempData)
		else:
			logging.debug('Environmental sensing is not active. Ignoring handle telemetry call.')
			
	def setDataMessageListener(self, listener: IDataMessageListener):
		"""
		Sets the data message listener reference, assuming listener is non-null.
		
		@param listener The data message listener instance to use for passing relevant
		messages, such as those received from a subscription event.
		"""
		if listener:
			self.dataMsgListener = listener

	def startManager(self) -> bool:
		"""
		Starts the manager and any background scheduler threads.
		
		"""
		logging.info("Started SensorAdapterManager.")
		
		if not self.scheduler.running:
			self.scheduler.start()
			
			return True
		else:
			logging.info("SensorAdapterManager scheduler already started. Ignoring.")
			
			return False
		
	def stopManager(self) -> bool:
		"""
		Stops the manager and any background scheduler threads.
		
		"""
		logging.info("Stopped SensorAdapterManager.")
		
		try:
			self.scheduler.shutdown()
			
			return True
		except:
			logging.info("SensorAdapterManager scheduler already stopped. Ignoring.")
			
			return False
		
	def updateSimulationData(self, data: ActuatorData = None):
		"""
		"""
		if data and self.useSimulator:
			logging.info("Updating simulator data set: " + data.getName())

			if data.getTypeID() == ConfigConst.THERMOSTAT_TYPE:
				simData = \
					self._generateTrendingSimulationData( \
						self.tempAdapter.getLatestTelemetry(), data.getValue())
				
				self.tempAdapter = None
				self.tempAdapter = TemperatureSensorSimTask(dataSet = simData)
				self.tempAdapter.enableSimulatedDataRollover(enable = False)

			elif data.getTypeID() == ConfigConst.HUMIDIFIER_TYPE:
				simData = \
					self._generateTrendingSimulationData( \
						self.humidityAdapter.getLatestTelemetry(), data.getValue())
				
				self.humidityAdapter = None
				self.humidityAdapter = HumiditySensorSimTask(dataSet = simData)
				self.humidityAdapter.enableSimulatedDataRollover(enable = False)

	def _generateTrendingSimulationData(self, sensorData: SensorData = None, targetVal: float = 0.0):
		"""
		"""
		if sensorData:
			self.dataGenerator = SensorDataGenerator()

			curVal = sensorData.getValue()
			minVal = curVal
			maxVal = curVal
			raiseTemp = False

			if (curVal > targetVal):
				minVal = targetVal
				maxVal = curVal
				raiseTemp = False

			if (curVal < targetVal):
				minVal = curVal
				maxVal = targetVal
				raiseTemp = True

			simData = \
				self.dataGenerator.generateTrendingSensorDataSet( \
					trendUpwards = raiseTemp, minValue = minVal, maxValue = maxVal)
			
			return simData
		
		return None
	
	def _initEnvironmentalSensorTasks(self):
		"""
		Instantiates the environmental sensor tasks based on the configuration file
		settings - such as simulation only, emulation only, or I2C bus access only.
		
		If emulation or I2C access is enabled, dynamically load the emulation module
		and classes so as to avoid trying to load classes that can't be interpreted
		due to dependencies on other libraries that may not be installed
		on the current execution platform.
		
		"""
		humidityFloor   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
		humidityCeiling = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
		
		pressureFloor   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		pressureCeiling = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
		
		tempFloor       = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
		tempCeiling     = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
		
		if self.useSimulator:
			self.dataGenerator = SensorDataGenerator()
			
			humidityData = \
				self.dataGenerator.generateDailyEnvironmentHumidityDataSet( \
					minValue = humidityFloor, maxValue = humidityCeiling, useSeconds = False)
			pressureData = \
				self.dataGenerator.generateDailyEnvironmentPressureDataSet( \
					minValue = pressureFloor, maxValue = pressureCeiling, useSeconds = False)
			tempData     = \
				self.dataGenerator.generateDailyIndoorTemperatureDataSet( \
					minValue = tempFloor, maxValue = tempCeiling, useSeconds = False)
			
			self.humidityAdapter = HumiditySensorSimTask(dataSet = humidityData)
			self.pressureAdapter = PressureSensorSimTask(dataSet = pressureData)
			self.tempAdapter     = TemperatureSensorSimTask(dataSet = tempData)
			
			self.isEnvSensingActive = True
			
		elif self.useEmulator or self.useSenseHat:
			# load the environmental emulators - the module will use the configuration settings
			# to determine if the emulator or actual SenseHAT device should be used - in
			# either case, the API is the same
			logging.info("Importing emulator modules...")
			
			heModule = import_module('labbenchstudios.pdt.edge.emulation.HumiditySensorEmulatorTask', 'HumiditySensorEmulatorTask')
			heClazz = getattr(heModule, 'HumiditySensorEmulatorTask')
			self.humidityAdapter = heClazz()
			logging.info("Instantiated humidity emulator task")
			
			peModule = import_module('labbenchstudios.pdt.edge.emulation.PressureSensorEmulatorTask', 'PressureSensorEmulatorTask')
			peClazz = getattr(peModule, 'PressureSensorEmulatorTask')
			self.pressureAdapter = peClazz()
			logging.info("Instantiated pressure emulator task")
			
			teModule = import_module('labbenchstudios.pdt.edge.emulation.TemperatureSensorEmulatorTask', 'TemperatureSensorEmulatorTask')
			teClazz = getattr(teModule, 'TemperatureSensorEmulatorTask')
			self.tempAdapter = teClazz()
			logging.info("Instantiated temperature emulator task")
			
			logging.info("Successfully imported emulator modules.")
			
			self.isEnvSensingActive = True
			
		elif self.useSenseHatI2CBus:
			#
			# TODO: FUTURE for labmodule04 ONLY
			#
			# load the environmental I2C tasks - the interface to each task is the same
			# as those in the emulator and simulator section, but relay on the SenseHAT
			# specific I2C bus settings for operation
			hiModule = import_module('labbenchstudios.pdt.edge.embedded.HumidityI2cSensorAdapterTask', 'HumidityI2cSensorAdapterTask')
			hiClazz = getattr(hiModule, 'HumidityI2cSensorAdapterTask')
			self.humidityAdapter = hiClazz()
			
			piModule = import_module('labbenchstudios.pdt.edge.embedded.PressureI2cSensorAdapterTask', 'PressureI2cSensorAdapterTask')
			piClazz = getattr(piModule, 'PressureI2cSensorAdapterTask')
			self.pressureAdapter = piClazz()
			
			tiModule = import_module('labbenchstudios.pdt.edge.embedded.TemperatureI2cSensorAdapterTask', 'TemperatureI2cSensorAdapterTask')
			tiClazz = getattr(tiModule, 'TemperatureI2cSensorAdapterTask')
			self.tempAdapter = tiClazz()
			
			self.isEnvSensingActive = True
			