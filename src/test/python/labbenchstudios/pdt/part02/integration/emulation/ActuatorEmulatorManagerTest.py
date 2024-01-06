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
import unittest

from time import sleep

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.edge.system.ActuatorAdapterManager import ActuatorAdapterManager
from labbenchstudios.pdt.common.DefaultDataMessageListener import DefaultDataMessageListener

from labbenchstudios.pdt.data.ActuatorData import ActuatorData

class ActuatorEmulatorManagerTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	ActuatorSimAdapterManager. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	
	NOTE: This test requires the sense_emu_gui to be running
	and must have access to the underlying libraries that
	support the pisense module. On Windows, one way to do
	this is by installing pisense and sense-emu within the
	Bash on Ubuntu on Windows environment and then execute this
	test case from the command line, as it will likely fail
	if run within an IDE in native Windows.
	
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing ActuatorAdapterManager class [using SenseHAT emulator]...")
		
		self.defaultMsgListener = DefaultDataMessageListener()
		self.actuatorAdapterMgr = ActuatorAdapterManager()
		self.actuatorAdapterMgr.setDataMessageListener(self.defaultMsgListener)
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testHumidifierEmulation(self):
		ad = ActuatorData(typeID = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
		ad.setValue(50.0)
		
		ad.setCommand(ConfigConst.COMMAND_ON)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)
		
		ad.setCommand(ConfigConst.COMMAND_OFF)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)

	def testHvacEmulation(self):
		ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
		ad.setValue(22.5)
		
		ad.setCommand(ConfigConst.COMMAND_ON)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)
		
		ad.setCommand(ConfigConst.COMMAND_OFF)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)

	def testLedDisplayEmulation(self):
		ad = ActuatorData(typeID = ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setStateData("What's up?")
		self.actuatorAdapterMgr.sendActuatorCommand(ad)
		
		ad.setCommand(ConfigConst.COMMAND_OFF)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)

if __name__ == "__main__":
	unittest.main()
	