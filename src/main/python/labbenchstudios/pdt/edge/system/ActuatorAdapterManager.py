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

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.IActuatorTask import IActuatorTask
from labbenchstudios.pdt.common.IDataManager import IDataManager
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener
from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum

from labbenchstudios.pdt.edge.simulation.SensorDataGenerator import SensorDataGenerator

from labbenchstudios.pdt.data.ActuatorData import ActuatorData

from labbenchstudios.pdt.edge.simulation.HvacActuatorSimTask import HvacActuatorSimTask
from labbenchstudios.pdt.edge.simulation.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from labbenchstudios.pdt.edge.simulation.LedDisplaySimTask import LedDisplaySimTask

class ActuatorAdapterManager(IDataManager):
	"""
	Manager class for running any actuator emulation or actual
	actuator integration logic.
	
	"""
	
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		"""
		Constructor.
		
		Sets the 'useEmulator' flag to determine if actual actuator integration
		is required or not.
		
		@param dataMsgListener The data message listener reference. Can be None, but shouldn't be, since
		it is necessary to permit registration of actuation commands that are sent to this manager
		from remote connections.
		"""
		self.dataMsgListener = dataMsgListener
		
		self.configUtil = ConfigUtil()
		
		self.useSimulator = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SIMULATOR_KEY)
		self.useEmulator  = \
			self.configUtil.getBoolean( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_EMULATOR_KEY)
		self.deviceID     = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		self.locationID   = \
			self.configUtil.getProperty( \
				section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		self.humidifierActuator = None
		self.hvacActuator       = None
		self.ledDisplayActuator = None
		
		#
		# FUTURE: use with labmodule04 only IFF connected to RPi
		#
		self.useSenseHatI2CBus = False
		
		self.resource = ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE
		#self.resource.setAsActuationResource(True)
		#self.resource.setDeviceName(self.deviceID)
		#self.resource.setResourceType(ConfigConst.ACTUATOR_RESPONSE)
		
		# TODO: make these configurable
		self.isEnvActuationActive = False
		
		# see PIOT-CDA-03-007 description for thoughts on the next line of code
		self._initEnvironmentalActuationTasks()
		
	def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
		"""
		Sends the command (and potential payload) specified within the
		ActuatorData message to the actuator (or emulator). Note that
		if the ActuatorData message has the isResponse flag set to
		True, the command issuance will be ignored and False will
		be returned.
		
		For now, this is a synchronous call, but could be asynchronous
		in a future implementation if the underlying actuator (or
		actuator emulator) requires an arbitrary amount of time to
		execute the command.
		
		On success, a new ActuatorData message is created from the
		original, with the isResponse flag set to true on the message.
		
		@param data The ActuatorData containing the command and other
		parameters (including payload) necessary for the actuation.
		@return ActuatorData A newly instanced ActuatorData object that
		contains the original ActuatorData message with the response flag
		enabled.
		"""

		# check if the data is valid and whether or not it's not a response
		# (if it is a response, ignore)
		updateDisplayOnActuation = \
			self.configUtil.getBoolean(\
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.UPDATE_DISPLAY_ON_ACTUATION_KEY)

		if data and not data.isResponseFlagEnabled():
			# check if the actuation event is destined for this device
			# via the location ID property
			if data.getLocationID() == self.locationID:
				logging.info("Actuator command received for location ID %s. Processing...", str(data.getLocationID()))

				aType = data.getTypeID()
				responseData = None

				if self.isEnvSensingActive:
					# and yes, there is a more elegant way to do this using a dict[]
					# with int index and function pointers for each of these sections -
					# this 	is merely to keep things clear considering we have a limited
					# number of actuator emulator types
					# TODO: implement appropriate logging and error handling
					if aType == \
						ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
						responseData = self.humidifierActuator.updateActuator(data)

						if updateDisplayOnActuation:
							data.setStateData(data.getName() + ': ' + str(data.getValue()))
							self.ledDisplayActuator.updateActuator(data)
							
					elif aType == \
						ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
						responseData = self.hvacActuator.updateActuator(data)

						if updateDisplayOnActuation:
							data.setStateData(data.getName() + ': ' + str(data.getValue()))
							self.ledDisplayActuator.updateActuator(data)

					elif aType == \
						ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
						responseData = self.ledDisplayActuator.updateActuator(data)

					else:
						logging.warning("No valid actuator type. Ignoring actuation for type: -%s- : -%s-", data.getTypeID(), aType)

				elif aType == \
					ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
					responseData = self.ledDisplayActuator.updateActuator(data)
				
				if responseData:
					responseData.setDeviceID(self.deviceID)

					return responseData
				
			else:
				logging.warning( \
					"Location ID doesn't match local. Ignoring: %s != %s", \
					str(self.locationID), str(data.getLocationID()))
					
		else:
			logging.warning( \
				"Actuator request received. Message is empty or response. Ignoring.")
		
		return None
	
	def setDataMessageListener(self, listener: IDataMessageListener = None):
		"""
		Sets the data message listener reference, assuming listener is non-null.
		
		@param listener The data message listener instance to use for passing relevant
		messages, such as those received from a subscription event.
		"""
		if listener:
			self.dataMsgListener = listener
			
	def startManager(self) -> bool:
		"""
		Starts the manager. This simply registers the current actuator state and - depending on
		the configuration - may activate the actuator command listeners.
		
		@return bool True on success; False otherwise
		"""
		
		return True
	
	def stopManager(self) -> bool:
		"""
		Stops the manager. Currently does nothing.
		
		@return bool True on success; False otherwise
		"""
		return True
	
	def _initEnvironmentalActuationTasks(self):
		"""
		Instantiates the environmental actuation tasks based on the configuration file
		settings - such as simulation only, emulation only, or I2C bus access only.
		
		If emulation or I2C access is enabled, dynamically load the emulation module
		and classes so as to avoid trying to load classes that can't be interpreted
		due to dependencies on other libraries that may not be installed
		on the current execution platform.
		
		"""
		
		if self.useSimulator:
			# load the environmental tasks for simulated actuation
			self.humidifierActuator = HumidifierActuatorSimTask()
			
			# create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()
			
			# create the LED actuator simulator
			self.ledDisplayActuator = LedDisplaySimTask()
			
			self.isEnvSensingActive = True
			
		elif self.useEmulator:
			# load the environmental tasks for emulated actuation -
			# the module will use the configuration settings to determine
			# if the emulator or actual SenseHAT device should be used - in
			# either case, the API is the same
			
			hueModule = import_module('labbenchstudios.pdt.edge.emulation.HumidifierActuatorEmulatorTask', 'HumidiferActuatorEmulatorTask')
			hueClazz = getattr(hueModule, 'HumidifierActuatorEmulatorTask')
			self.humidifierActuator = hueClazz()
			
			hveModule = import_module('labbenchstudios.pdt.edge.emulation.HvacActuatorEmulatorTask', 'HvacActuatorEmulatorTask')
			hveClazz = getattr(hveModule, 'HvacActuatorEmulatorTask')
			self.hvacActuator = hveClazz()

			leDisplayModule = import_module('labbenchstudios.pdt.edge.emulation.LedActuatorDisplayEmulatorTask', 'LedActuatorDisplayEmulatorTask')
			leClazz = getattr(leDisplayModule, 'LedActuatorDisplayEmulatorTask')
			self.ledDisplayActuator = leClazz()
			
			self.isEnvSensingActive = True
			
		elif self.useSenseHatI2CBus:
			# load the environmental tasks for I2C-specific actuation -
			# the module will use the configuration settings to determine
			# if the emulator or actual SenseHAT device should be used - in
			# either case, the API is the same
			
			liDisplayModule = import_module('labbenchstudios.pdt.edge.embedded.LedGpioActuatorAdapterTask', 'LedGpioActuatorAdapterTask')
			liClazz = getattr(liDisplayModule, 'LedGpioActuatorAdapterTask')
			self.ledDisplayActuator = liClazz()
			
			self.isEnvSensingActive = True
