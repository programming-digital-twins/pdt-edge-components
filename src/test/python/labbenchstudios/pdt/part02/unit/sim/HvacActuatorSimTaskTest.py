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

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.edge.simulation.HvacActuatorSimTask import HvacActuatorSimTask

class HvacActuatorSimTaskTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	HvacActuatorSimTask. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	DEFAULT_VAL_A = 18.2
	DEFAULT_VAL_B = 21.4
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing HvacActuatorSimTask class...")
		self.hSimTask = HvacActuatorSimTask()
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testUpdateActuator(self):
		ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setValue(self.DEFAULT_VAL_A)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		self.assertEquals(adr.getValue(), self.DEFAULT_VAL_A)
		logging.info("ActuatorData: " + str(adr))
		
		ad.setValue(self.DEFAULT_VAL_B)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		self.assertEquals(adr.getValue(), self.DEFAULT_VAL_B)
		logging.info("ActuatorData: " + str(adr))
		
		ad.setCommand(ConfigConst.COMMAND_OFF)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		self.assertEquals(adr.getCommand(), ConfigConst.COMMAND_OFF)
		logging.info("ActuatorData: " + str(adr))
		
	@unittest.skip("Ignore for now.")
	def testUpdateActuatorRepeatCommands(self):
		ad = ActuatorData(typeID = ConfigConst.HVAC_ACTUATOR_TYPE)
		
		# new command ON with new value - should succeed
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setValue(self.DEFAULT_VAL_A)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		self.assertEquals(adr.getValue(), self.DEFAULT_VAL_A)
		logging.info("ActuatorData: " + str(adr))
		
		# same command ON with same value - should fail
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setValue(self.DEFAULT_VAL_A)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNone(adr)
		logging.info("ActuatorData: " + str(adr))
		
		# new command OFF with same value - should succeed
		ad.setCommand(ConfigConst.COMMAND_OFF)
		ad.setValue(self.DEFAULT_VAL_A)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		self.assertEquals(adr.getValue(), self.DEFAULT_VAL_A)
		logging.info("ActuatorData: " + str(adr))
		
		# same command OFF with different value - should succeed
		ad.setCommand(ConfigConst.COMMAND_OFF)
		ad.setValue(self.DEFAULT_VAL_B)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		logging.info("ActuatorData: " + str(adr))
		
		# new command ON with same value - should succeed
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setValue(self.DEFAULT_VAL_B)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		logging.info("ActuatorData: " + str(adr))
		
		# same command ON with new value - should succeed
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setValue(self.DEFAULT_VAL_A)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		logging.info("ActuatorData: " + str(adr))
		
		# new command OFF with same value - should succeed
		ad.setCommand(ConfigConst.COMMAND_OFF)
		ad.setValue(self.DEFAULT_VAL_A)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNotNone(adr)
		self.assertEquals(adr.getValue(), self.DEFAULT_VAL_A)
		logging.info("ActuatorData: " + str(adr))
		
		# same command OFF with same value - should fail
		ad.setCommand(ConfigConst.COMMAND_OFF)
		ad.setValue(self.DEFAULT_VAL_A)
		
		adr = self.hSimTask.updateActuator(ad)
		
		self.assertIsNone(adr)
		logging.info("ActuatorData: " + str(adr))
		
if __name__ == "__main__":
	unittest.main()
	