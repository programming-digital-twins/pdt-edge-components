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
import time

from apscheduler.schedulers.background import BackgroundScheduler

from threading import Thread

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.IDataManager import IDataManager
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener

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
		
		self.locationID = \
			self.configUtil.getProperty( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		self.pollRate = \
			self.configUtil.getInteger( \
				section = ConfigConst.WIND_TURBINE_SETTINGS_KEY, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		
		self.enableCommandName = \
			self.configUtil.getProperty( \
				section = ConfigConst.WIND_TURBINE_SETTINGS_KEY, key = ConfigConst.ENABLE_COMMAND_NAME_KEY, defaultVal = ConfigConst.NOT_SET)
		
		# for now, power generation is always a simulation
		self.useSimulator = True
		self.enableWindTurbineBraking = False

		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES

		self.scheduler = None
		self.schedThread = None

		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job( \
			self.handleTelemetry, 'interval', seconds = self.pollRate, \
			max_instances = 5, coalesce = True, misfire_grace_time = 30)

		'''
		self.schedThread = Thread(target = self._runTelemetrySchedule, name = "WindTurbineTask")
		self.schedThread.daemon = True
		'''

		self.windTurbine = None
		self.dataMsgListener = None
		self.curCommand = ConfigConst.DEFAULT_COMMAND

		self._initTasks()

	def handleTelemetry(self):
		"""
		"""
		self.windTurbineSimTask.enableBrakingSystem(enable = self.enableWindTurbineBraking)
		self.windTurbineSimTask.generateTelemetry()

		brakingStatus = "disabled"

		if (self.enableWindTurbineBraking):
			brakingStatus = "enabled"

		powerOutputData     = self.windTurbineSimTask.getPowerOutputTelemetry()
		rotationalSpeedData = self.windTurbineSimTask.getRotationalSpeedTelemetry()
		windSpeedData       = self.windTurbineSimTask.getWindSpeedTelemetry()
		
		logging.debug( \
			'Brake is %s: Power output is %s kw, rotational speed is %s rpm, wind speed is %s m/s.', \
			brakingStatus, \
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
		
		if self.schedThread:
			self.schedThread.start()
		elif self.scheduler:
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
			if self.schedThread:
				self.schedThread.join()
			elif self.scheduler:
				if self.scheduler.running:
					self.scheduler.shutdown()
			else:
				logging.warning("WindTurbineAdapterManager scheduler already stopped. Ignoring.")
		except:
			logging.warning("WindTurbineAdapterManager scheduler already stopped. Ignoring.")
			
	def updateSimulationData(self, data: ActuatorData = None):
		"""
		"""
		if (self.useSimulator):
			if (data and data.getLocationID() == self.locationID and not data.isResponseFlagEnabled()):
				
				if (data.getCommandName() != self.enableCommandName):
					logging.warning("Incoming wind turbine command is not supported. Ignoring: %s", data.getCommandName())
					return

				adResponse = ActuatorData()
				adResponse.updateData(data)
				adResponse.setAsResponse()
		
				command = data.getCommand()
				value = data.getValue()

				if (command == self.curCommand):
					logging.warning("Duplicate command received for wind turbine sim: %s. Igoring.", str(command))
				else:
					self.curCommand = command

					logging.info( \
						"Updating wind turbine simulated data set: name = %s, type = %s, cmd = %s, val = %s", \
						data.getName(), str(data.getTypeID()), str(command), str(value))

					if (command == ConfigConst.COMMAND_OFF):
						logging.info("  --> ENABLING Wind Turbine Brake...")
						self.enableWindTurbineBraking = True

					elif (command == ConfigConst.COMMAND_ON):
						logging.info("  --> DISABLING Wind Turbine Brake and updating simulated wind speed...")
						self.enableWindTurbineBraking = False

					#if self.dataMsgListener:
					#	self.dataMsgListener.handleActuatorCommandResponse(adResponse)

			else:
				logging.warning("Received update sim data request with invalid or response ActuatorData. Ignoring.")

		else:
			logging.warning("Received update sim data request, but sim is disabled. Ignoring.")

	def _initTasks(self):
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
	
	def _generateOscillatingSimulationData(self, sensorData: SensorData = None, targetVal: float = 0.0):
		"""
		"""
		if sensorData:
			self.dataGenerator = SensorDataGenerator()

			curVal = sensorData.getValue()
			minVal = curVal
			maxVal = curVal

			if (curVal > targetVal):
				minVal = targetVal
				maxVal = curVal

			if (curVal < targetVal):
				minVal = curVal
				maxVal = targetVal

			simData = \
				self.dataGenerator.generateOscillatingSensorDataSet( \
					minValue = minVal, maxValue = maxVal)
			
			return simData
		
		return None
	
	def _runTelemetrySchedule(self):
		"""
		"""
		while (True):
			self.handleTelemetry()

			time.sleep(self.pollRate)

		pass
