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

from labbenchstudios.pdt.edge.simulation.FactoryWorkcellSimTask import FactoryWorkcellSimTask

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData

from labbenchstudios.pdt.edge.simulation.SensorDataGenerator import SensorDataGenerator

class FactoryWorkcellAdapterManager(IDataManager):
	"""
	
	"""

	def __init__(self):
		"""
		Constructor - no args.
		
		Loads the poll rate and other config properties.
		"""
		self.configUtil = ConfigUtil()
		self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
		
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

		self.lkgItemProdRate = self.defaultItemProdRate
		self.itemProdRateSeconds = 60.0

		self._initItemProductionRateSeconds()

		logging.info("\nSetting min / max item production rate (per minute): " + str(self.minItemProdRate) + " to " + str(self.maxItemProdRate) + "\n")
		logging.info("\nSetting default item production rate (per minute): " + str(self.defaultItemProdRate) + "\n")

		# for now, factory workcell production is always a simulation
		self.useSimulator = True

		# set to True whenever production rate <= 0
		self.pauseProduction = False

		# poll rate is the non-zero item production rate in seconds
		if self.itemProdRateSeconds > 0:
			self.pollRate = self.itemProdRateSeconds

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
		self.workcellSimTask.setProductionPauseFlag(enable = self.pauseProduction)
		self.workcellSimTask.generateTelemetry()

		productionStatus = "running"

		if (self.pauseProduction):
			productionStatus = "paused"

		powerOutputData     = self.workcellSimTask.getPowerOutputTelemetry()
		rotationalSpeedData = self.workcellSimTask.getRotationalSpeedTelemetry()
		windSpeedData       = self.workcellSimTask.getWindSpeedTelemetry()
		
		logging.debug( \
			'Brake is %s: Power output is %s kw, rotational speed is %s rpm, wind speed is %s m/s.', \
			productionStatus, \
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
	
	def setProductionRate(self, curProdRate: int = 0):
		"""
		"""
		if curProdRate == 0:
			# pause all production
			self.curItemProdRate = 0
			self._initItemProductionRateSeconds()
		elif curProdRate >= self.minItemProdRate and curProdRate <= self.maxItemProdRate:
			# update production rate
			self.curItemProdRate = curProdRate
			self._initItemProductionRateSeconds()

	def startManager(self):
		"""
		Starts the workcell manager, and starts the scheduled
		polling of workcell tasks.
		
		"""
		logging.info("Starting workcell manager...")
		
		if self.schedThread:
			self.schedThread.start()
		elif self.scheduler:
			if not self.scheduler.running:
				self.scheduler.start()
		else:
			logging.warning("WindTurbineAdapterManager scheduler already started. Ignoring.")
		
	def stopManager(self):
		"""
		Stops the workcell manager, and stops the scheduler.
		
		"""
		logging.info("Stopping workcell manager...")
		
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
					logging.warning("Incoming workcell command is not supported. Ignoring: %s", data.getCommandName())
					return

				adResponse = ActuatorData()
				adResponse.updateData(data)
				adResponse.setAsResponse()
		
				command = data.getCommand()
				value = data.getValue()

				if (command == self.curCommand):
					logging.warning("Duplicate command received for workcell sim: %s. Igoring.", str(command))
				else:
					self.curCommand = command

					logging.info( \
						"Updating workcell simulated data set: name = %s, type = %s, cmd = %s, val = %s", \
						data.getName(), str(data.getTypeID()), str(command), str(value))

					if (command == ConfigConst.COMMAND_OFF):
						logging.info("  --> DISABLING workcell production...")
						self.setProductionRate(0)

					elif (command == ConfigConst.COMMAND_ON):
						logging.info("  --> ENABLING workcell production...")
						self.pauseProduction = False

					elif (command == ConfigConst.COMMAND_UPDATE):
						logging.info("  --> UPDATING workcell production rate...")
						self._updateProductionRate(value)

					#if self.dataMsgListener:
					#	self.dataMsgListener.handleActuatorCommandResponse(adResponse)

			else:
				logging.warning("Received update sim data request with invalid or response ActuatorData. Ignoring.")

		else:
			logging.warning("Received update sim data request, but sim is disabled. Ignoring.")

	def _initItemProductionRateSeconds(self):
		"""
		"""
		if self.defaultItemProdRate > 0.0:
			self.itemProdRateSeconds = 60.0 / self.defaultItemProdRate
			self.pauseProduction = False
			logging.info("\nItem production rate (in seconds): " + str(self.itemProdRateSeconds) + "\n")
		else:
			self.itemProdRateSeconds = 0.0
			self.pauseProduction = True
			logging.info("\nItem production is currently DISABLED: Prod Rate = " + str(self.defaultItemProdRate) + "\n")

	def _initTasks(self):
		"""
		Instantiates the workcell sensor tasks based on the configuration file
		settings (e.g., simulation only).
		
		"""
		self.dataGenerator = SensorDataGenerator()
		
		self.workcellSimTask = FactoryWorkcellSimTask()
			
	def _runTelemetrySchedule(self):
		"""
		"""
		while (True):
			self.handleTelemetry()

			time.sleep(self.pollRate)
