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
from labbenchstudios.pdt.edge.system.BaseActuatorTask import BaseActuatorTask

from pisense import SenseHAT

class LedActuatorDisplayEmulatorTask(BaseActuatorTask):
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
			LedActuatorDisplayEmulatorTask, self).__init__( \
				name = ConfigConst.LED_ACTUATOR_NAME, \
				typeID = ConfigConst.LED_DISPLAY_ACTUATOR_TYPE, \
				typeCategoryID = ConfigConst.SYSTEM_MGMT_TYPE_CATEGORY, \
				simpleName = "LED_Display")
			
		enableEmulation = \
			ConfigUtil().getBoolean( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate = enableEmulation)
		self._setDisableTypeCheckFlag(True)
		
	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Determines how to interact with the LED display based on the
		passed in command.
		
		If cmd == ActuatorData.COMMAND_ON, will attempt to write
		the stateData as a message to the emulated LED display
		using pre-configured scrolling, etc.
		
		If cmd == ActuatorData.COMMAND_OFF, will clear the emulated
		LED display and stop scrolling any message.
		
		@param cmd The actuation command to process.
		@param stateData The string state data to use in processing the command.
		@return int The status code from the actuation call.
		"""
		if self.sh.screen:
			self.sh.screen.scroll_text(stateData, size = 8)
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1
	
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Determines how to interact with the LED display based on the
		passed in command.
		
		If cmd == ActuatorData.COMMAND_ON, will attempt to write
		the stateData as a message to the emulated LED display
		using pre-configured scrolling, etc.
		
		If cmd == ActuatorData.COMMAND_OFF, will clear the emulated
		LED display and stop scrolling any message.
		
		@param cmd The actuation command to process.
		@param stateData The string state data to use in processing the command.
		@return int The status code from the actuation call.
		"""
		if self.sh.screen:
			self.sh.screen.clear()
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to clear / close.")
			return -1
	