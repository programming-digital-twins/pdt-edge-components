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

from time import sleep

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.edge.system.BaseActuatorTask import BaseActuatorTask

from pisense import SenseHAT

class HvacActuatorEmulatorTask(BaseActuatorTask):
	"""
	This is a simple wrapper for an Actuator abstraction - it provides
	a container for the actuator's state, value, name, and status. A
	command variable is also provided to instruct the actuator to
	perform a specific function (in addition to setting a new value
	via the 'val' parameter.
	
	"""

	def __init__(self):
		"""
		Constructor.
		
		@param actuatorType The int representing the type of the actuator.
		"""
		super( \
			HvacActuatorEmulatorTask, self).__init__( \
				name = ConfigConst.HVAC_ACTUATOR_NAME, \
				typeID = ConfigConst.HVAC_ACTUATOR_TYPE, \
				typeCategoryID = ConfigConst.ENV_TYPE_CATEGORY, \
				simpleName = "HVAC")
		
		enableEmulation = \
			ConfigUtil().getBoolean( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate = enableEmulation)

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Enables the SenseHAT emulator (or device) LED display based on the
		passed in parameters.
		
		This method call will attempt to scroll an ON message with the humidity
		value to the emulated LED display using pre-configured scrolling, etc.
		
		@param val The actuation value to process.
		@param stateData The string state data to use in processing the command.
		@return int The status code from the actuation call.
		"""
		if self.sh.screen:
			msg = self.getSimpleName() + ' ON: ' + str(val) + 'C'
			self.sh.screen.scroll_text(msg)
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1

	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Disables the SenseHAT emulator (or device) LED display based on the
		passed in parameters.
		
		This method call will attempt to scroll an OFF message for up to 5
		seconds, then clear the emulated (or device) LED display.
		
		@param val The actuation value to process.
		@param stateData The string state data to use in processing the command.
		@return int The status code from the actuation call.
		"""
		if self.sh.screen:
			msg = self.getSimpleName() + ' OFF'
			self.sh.screen.scroll_text(msg)
			
			# optional sleep (5 seconds) for message to scroll before clearing display
			sleep(5)
			
			self.sh.screen.clear()
			#self.sh.screen.close()
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to clear / close.")
			return -1
