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

from labbenchstudios.pdt.edge.system.SystemCpuUtilTask import SystemCpuUtilTask
from labbenchstudios.pdt.edge.system.SystemMemUtilTask import SystemMemUtilTask

from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceManager(IDataManager):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		"""
		Constructor - no args.
		
		Loads the poll rate and other config properties.
		"""
		configUtil = ConfigUtil()
		
		self.pollRate = \
			configUtil.getInteger( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		
		self.locationID = \
			configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
			
		#self.scheduler = BackgroundScheduler()
		#self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job( \
			self.handleTelemetry, 'interval', seconds = self.pollRate, \
			max_instances = 2, coalesce = True, misfire_grace_time = 15)
		
		self.cpuUtilTask = SystemCpuUtilTask()
		self.memUtilTask = SystemMemUtilTask()
		
		self.dataMsgListener = None
		
	def handleTelemetry(self):
		"""
		"""
		self.cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
		self.memUtilPct = self.memUtilTask.getTelemetryValue()
		
		logging.debug('CPU utilization is %s percent, and memory utilization is %s percent.', str(self.cpuUtilPct), str(self.memUtilPct))
		
		sysPerfData = SystemPerformanceData()
		sysPerfData.setLocationID(self.locationID)
		sysPerfData.setCpuUtilization(self.cpuUtilPct)
		sysPerfData.setMemoryUtilization(self.memUtilPct)
		
		if self.dataMsgListener:
			self.dataMsgListener.handleSystemPerformanceMessage(data = sysPerfData)
			
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		"""
		"""
		if listener:
			self.dataMsgListener = listener
	
	def startManager(self):
		"""
		Starts the system performance manager, and starts the scheduled
		polling of the tasks (CPU and Memory Utilization).
		
		"""
		logging.info("Starting system performance manager...")
		
		if not self.scheduler.running:
			self.scheduler.start()
		else:
			logging.warning("SystemPerformanceManager scheduler already started. Ignoring.")
		
	def stopManager(self):
		"""
		Stops the system performance manager, and stops the scheduler.
		
		"""
		logging.info("Stopping system performance manager...")
		
		try:
			if self.scheduler.running:
				self.scheduler.shutdown()
			else:
				logging.warning("SystemPerformanceManager scheduler already stopped. Ignoring.")
		except:
			logging.warning("SystemPerformanceManager scheduler already stopped. Ignoring.")
			