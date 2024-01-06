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

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.edge.system.ActuatorAdapterManager import ActuatorAdapterManager
from labbenchstudios.pdt.common.DefaultDataMessageListener import DefaultDataMessageListener

from labbenchstudios.pdt.data.ActuatorData import ActuatorData

class ActuatorAdapterManagerTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	ActuatorSimAdapterManager. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing ActuatorAdapterManager class...")
		
		self.defaultMsgListener = DefaultDataMessageListener()
		self.actuatorAdapterMgr = ActuatorAdapterManager()
		self.actuatorAdapterMgr.setDataMessageListener(self.defaultMsgListener)
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testHumidifierSimulation(self):
		ad = ActuatorData(typeID = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
		ad.setValue(50.0)
		
		ad.setCommand(ConfigConst.COMMAND_ON)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)
		
		ad.setCommand(ConfigConst.COMMAND_OFF)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)

	def testHvacSimulation(self):
		ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
		ad.setValue(22.5)
		
		ad.setCommand(ConfigConst.COMMAND_ON)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)
		
		ad.setCommand(ConfigConst.COMMAND_OFF)
		self.actuatorAdapterMgr.sendActuatorCommand(ad)

if __name__ == "__main__":
	unittest.main()
	