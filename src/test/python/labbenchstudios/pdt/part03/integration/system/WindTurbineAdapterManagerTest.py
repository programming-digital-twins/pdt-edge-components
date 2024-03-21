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

from labbenchstudios.pdt.common.DefaultDataMessageListener import DefaultDataMessageListener
from labbenchstudios.pdt.edge.system.WindTurbineAdapterManager import WindTurbineAdapterManager

from labbenchstudios.pdt.data.ActuatorData import ActuatorData

class WindTurbineAdapterManagerTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	WindTurbineAdapterManager. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing WindTurbineAdapterManager class...")
		
		self.defaultMsgListener = DefaultDataMessageListener()
		self.windTurbineMgr = WindTurbineAdapterManager()
		self.windTurbineMgr.setDataMessageListener(self.defaultMsgListener)
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testStartAndStopManager(self):
		cmdData = \
			ActuatorData( \
				name = 'Test', \
				typeCategoryID = ConfigConst.ENERGY_TYPE_CATEGORY, \
				typeID = ConfigConst.WIND_TURBINE_BRAKE_SYSTEM_ACTUATOR_TYPE)
		
		self.windTurbineMgr.startManager()
		
		sleep(15)

		cmdData.setCommand(ConfigConst.COMMAND_ON)
		self.windTurbineMgr.updateSimulationData(data = cmdData)

		sleep(15)

		cmdData.setCommand(ConfigConst.COMMAND_OFF)
		self.windTurbineMgr.updateSimulationData(data = cmdData)
		
		sleep(25)

		self.windTurbineMgr.stopManager()

if __name__ == "__main__":
	unittest.main()
	