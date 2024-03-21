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

from apscheduler.schedulers.background import BackgroundScheduler

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.IDataManager import IDataManager
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener

from labbenchstudios.pdt.edge.simulation import WindTurbineSensorSimTask
from labbenchstudios.pdt.edge.simulation.WindTurbineSensorSimTask import WindTurbineSensorSimTask

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData

from labbenchstudios.pdt.edge.simulation.SensorDataGenerator import SensorDataGenerator

class WindTurbineAdapterManager(IDataManager):
	"""
	
	"""

	def __init__(self):
		"""
		Constructor - no args.
		
		Loads the poll rate and other config properties.
		"""
		self.configUtil = ConfigUtil()
		
		self.pollRate = \
			self.configUtil.getInteger( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		
		self.locationID = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		# for now, power generation is always a simulation
		self.useSimulator = True
		self.enableWindTurbineBraking = False

		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
			
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job( \
			self.handleTelemetry, 'interval', seconds = self.pollRate, \
			max_instances = 2, coalesce = True, misfire_grace_time = 15)
		
		self.windTurbine = None
		self.dataMsgListener = None

		self._initWindTurbineSensorTasks()

	def handleTelemetry(self):
		"""
		"""
		self.windTurbineSimTask.enableBrakingSystem(enable = self.enableWindTurbineBraking)
		self.windTurbineSimTask.generateTelemetry()

		powerOutputData     = self.windTurbineSimTask.getPowerOutputTelemetry()
		rotationalSpeedData = self.windTurbineSimTask.getRotationalSpeedTelemetry()
		windSpeedData       = self.windTurbineSimTask.getWindSpeedTelemetry()
		
		logging.debug( \
			'Power output is %s kw, rotational speed is %s rpm, wind speed is %s m/s.', \
			str(powerOutputData.getValue()), \
			str(rotationalSpeedData.getValue()), \
			str(windSpeedData.getValue()))
		
		# a future upgrade may package both values into a single generic SensorData
		# for now, just send two separate SensorData instances
		if self.dataMsgListener:
			self.dataMsgListener.handleSensorMessage(data = powerOutputData)
			self.dataMsgListener.handleSensorMessage(data = rotationalSpeedData)
			self.dataMsgListener.handleSensorMessage(data = windSpeedData)
			
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		"""
		"""
		if listener:
			self.dataMsgListener = listener
	
	def startManager(self):
		"""
		Starts the wind turbine manager, and starts the scheduled
		polling of wind turbine tasks.
		
		"""
		logging.info("Starting wind turbine manager...")
		
		if not self.scheduler.running:
			self.scheduler.start()
		else:
			logging.warning("WindTurbineAdapterManager scheduler already started. Ignoring.")
		
	def stopManager(self):
		"""
		Stops the wind turbine manager, and stops the scheduler.
		
		"""
		logging.info("Stopping wind turbine manager...")
		
		try:
			if self.scheduler.running:
				self.scheduler.shutdown()
			else:
				logging.warning("WindTurbineAdapterManager scheduler already stopped. Ignoring.")
		except:
			logging.warning("WindTurbineAdapterManager scheduler already stopped. Ignoring.")
			
	def updateSimulationData(self, data: ActuatorData = None):
		"""
		"""
		if data and self.useSimulator:
			logging.info("Updating wind turbine simulated data set: " + data.getName())

			if data.getTypeID() == ConfigConst.WIND_TURBINE_BRAKE_SYSTEM_ACTUATOR_TYPE:
				if (data.getCommand() == ConfigConst.COMMAND_ON):
					self.enableWindTurbineBraking = True
				else:
					self.enableWindTurbineBraking = False

	def _initWindTurbineSensorTasks(self):
		"""
		Instantiates the wind turbine sensor tasks based on the configuration file
		settings (e.g., simulation only).
		
		"""
		minWindSpeed   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.MIN_WIND_SPEED_KEY, defaultVal = 2.0)
		maxWindSpeed   = \
			self.configUtil.getFloat( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.MAX_WIND_SPEED_KEY, defaultVal = 20.0)
		
		logging.info("\n\n*****\n\nSetting min / max wind speed: " + str(minWindSpeed) + " to " + str(maxWindSpeed) + "\n\n*****\n\n")

		self.dataGenerator = SensorDataGenerator()
		
		windSpeedData = \
			self.dataGenerator.generateOscillatingSensorDataSet( \
				minValue = minWindSpeed, maxValue = maxWindSpeed, useSeconds = False)
		
		self.windTurbineSimTask = WindTurbineSensorSimTask(dataSet = windSpeedData)
			
	def _initSampleWeatherData(self):
		pass
		
	def _initSampleWindTurbine(self):
		pass
