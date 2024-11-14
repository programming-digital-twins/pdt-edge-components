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
import threading
import traceback
import queue

from time import sleep

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener
from labbenchstudios.pdt.common.MessageQueueItem import MessageQueueItem
from labbenchstudios.pdt.common.ResourceNameContainer import ResourceNameContainer

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class EventDispatchManager(IDataMessageListener):
	"""
	This class handles all internal messaging events by processing them all within
	a simple queue and then redirecting each via a dispatch thread. This ensures
	that messages can be quickly offloaded by the various internal simulators and
	connection infrastructure whilst also effectively delegated to their destinations.

	This implements the IDataMessageListener interface, so is designed to integrate
	with existing EDA business logic seamlessly.
	
	"""
	
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		"""
		Constructor.
		
		"""
		self.configUtil = ConfigUtil()
		
		self.dataMsgListener = dataMsgListener

		self.enableMsgQueue   = \
			self.configUtil.getBoolean( \
				section = ConfigConst.EDGE_DEVICE, key = ConfigConst.ENABLE_MSG_QUEUE_KEY)
		
		self.msgQueue           = None
		self.msgQueueThread     = None
		
		if self.enableMsgQueue:
			self.msgQueue = queue.SimpleQueue()
			self.msgQueueThread = threading.Thread(target = self._processQueueMessages, name = "EventDispatchManager", daemon = True)
			logging.info("Message queue and processing thread enabled")

	def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
		"""
		Not implemented.
		
		@param name
		@return ActuatorData
		"""
		pass
		
	def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
		"""
		Not implemented.
		
		@param name
		@return SensorData
		"""
		pass
	
	def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
		"""
		Not implemented.
		
		@param name
		@return SystemPerformanceData
		"""
		pass
	
	def handleActuatorCommandMessage(self, data: ActuatorData = None) -> ActuatorData:
		"""
		Callback function to handle an actuator command message packaged as a ActuatorData object.
		
		@param data The ActuatorData message received.
		@return bool True on success; False otherwise.
		"""
		if self.msgQueue:
			msgQueueItem = MessageQueueItem(msgData = data, callbackFunc = self._processActuatorCommandMessage)
			self.msgQueue.put(msgQueueItem)

			logging.info("Added ActuatorData command to message queue.")
		else:
			logging.warning("Message queue not enabled. Ignoring incoming ActuatorData command msg.")

	def handleActuatorCommandResponse(self, data: ActuatorData = None) -> bool:
		"""
		Callback function to handle an actuator command response packaged as a ActuatorData object.
		
		@param data The ActuatorData message received.
		@return bool True on success; False otherwise.
		"""
		if self.msgQueue:
			msgQueueItem = MessageQueueItem(msgData = data, callbackFunc = self._processActuatorCommandResponse)
			self.msgQueue.put(msgQueueItem)

			logging.info("Added ActuatorData response to message queue.")
		else:
			logging.warning("Message queue not enabled. Ignoring incoming ActuatorData response msg.")

	def handleSensorMessage(self, data: SensorData = None) -> bool:
		"""
		Callback function to handle a sensor message packaged as a SensorData object.
		
		@param data The SensorData message received.
		@return bool True on success; False otherwise.
		"""
		if self.msgQueue:
			msgQueueItem = MessageQueueItem(msgData = data, callbackFunc = self._processSensorMessage)
			self.msgQueue.put(msgQueueItem)

			logging.info("Added SensorData to message queue.")
		else:
			logging.warning("Message queue not enabled. Ignoring incoming SensorData msg.")
		
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData = None) -> bool:
		"""
		Callback function to handle a system performance message packaged as
		SystemPerformanceData object.
		
		@param data The SystemPerformanceData message received.
		@return bool True on success; False otherwise.
		"""
		if self.msgQueue:
			msgQueueItem = MessageQueueItem(msgData = data, callbackFunc = self._processSystemPerformanceMessage)
			self.msgQueue.put(msgQueueItem)

			logging.info("Added SystemPerformanceData to message queue.")
		else:
			logging.warning("Message queue not enabled. Ignoring incoming SystemPerformance msg.")

	def handleIncomingMessage(self, resource: ResourceNameContainer = None, msg: str = None) -> bool:
		"""
		Callback function to handle a generic string-based message.
		
		@param resource The ResourceNameContainer
		@param data The string-based message received.
		@return bool True on success; False otherwise.
		"""
		logging.warning("Generic incoming message callback not implemented. Use data container specific interface.")

	def startManager(self):
		"""
		Starts the manager - this will invoke the start methods on
		the connection client and system performance manager.
		
		"""
		logging.info("Starting EventDispatchManager...")
		
		if self.msgQueueThread:
			logging.info("Starting message queue processor thread...")
			self.msgQueueThread.start()

		logging.info("Started EventDispatchManager.")
		
	def stopManager(self):
		"""
		Stops the manager - this will invoke the stop methods on
		the connection client and system performance manager.
		
		"""
		logging.info("Stopping EventDispatchManager...")
		
		if self.msgQueueThread:
			timeoutSecs = 5.0 # make this configurable
			logging.info("Processing remaining queued message items from message queue thread. Timeout: %s", str(timeoutSecs))
			self.msgQueueThread.join(timeout = timeoutSecs)
			
		logging.info("Stopped EventDispatchManager.")
		
	def _processActuatorCommandMessage(self, data: ActuatorData = None) -> ActuatorData:
		"""
		Callback function to handle an actuator command message packaged as a ActuatorData object.
		
		@param data The ActuatorData message received.
		@return bool True on success; False otherwise.
		"""
		if self.dataMsgListener:
			logging.info("Dispatching queued ActuatorData command to message listener implementation.")

			return self.dataMsgListener.handleActuatorCommandMessage(data)
		else:
			logging.warning("No data message listener instance stored. Ignoring queued ActuatorData command msg.")
		
	def _processActuatorCommandResponse(self, data: ActuatorData = None) -> bool:
		"""
		Callback function to handle an actuator command response packaged as a ActuatorData object.
		
		@param data The ActuatorData message received.
		@return bool True on success; False otherwise.
		"""
		if self.dataMsgListener:
			logging.info("Dispatching queued ActuatorData response to message listener implementation.")

			return self.dataMsgListener.handleActuatorCommandResponse(data)
		else:
			logging.warning("No data message listener instance stored. Ignoring queued ActuatorData response msg.")
	
	def _processSensorMessage(self, data: SensorData = None) -> bool:
		"""
		Callback function to handle a sensor message packaged as a SensorData object.
		
		@param data The SensorData message received.
		@return bool True on success; False otherwise.
		"""
		if self.dataMsgListener:
			logging.info("Dispatching queued SensorData to message listener implementation.")

			return self.dataMsgListener.handleSensorMessage(data)
		else:
			logging.warning("No data message listener instance stored. Ignoring queued SensorData msg.")
		
	def _processSystemPerformanceMessage(self, data: SystemPerformanceData = None) -> bool:
		"""
		Callback function to handle a system performance message packaged as
		SystemPerformanceData object.
		
		@param data The SystemPerformanceData message received.
		@return bool True on success; False otherwise.
		"""
		if self.dataMsgListener:
			logging.info("Dispatching queued SystemPerformanceData to message listener implementation.")

			return self.dataMsgListener.handleSystemPerformanceMessage(data)
		else:
			logging.warning("No data message listener instance stored. Ignoring queued SystemPerformanceData msg.")
	
	def _processQueueMessages(self):
		"""
		A simple queue 'get' and 'task complete' method for use by the queue processing thread.
		This call will block while the queued item is pulled off and processed by the thread,
		but should not block other operations until the DeviceDataManager is stopped.

		"""
		while True:
			count = 0

			try:
				while (not self.msgQueue.empty()):
					msgItem = self.msgQueue.get()

					# msgItem will be of type MessageQueueItem
					logging.info("Working on queue item: %s", str(msgItem))

					# do work
					if msgItem and isinstance(msgItem, MessageQueueItem):
						msgItem.invokeCallback()

					count = count + 1
					
			except Exception as e:
				# queue is prob empty
				logging.warning("Failed to process queue item.")
				traceback.print_exception(type(e), e, e.__traceback__)

			# sleep for a wee bit - make this configurable,
			# since we process a bunch of queue msgs in one
			# sweep, we should be able to keep this delay
			# to about 1000 ms (1 second)
			sleep(1.0)
