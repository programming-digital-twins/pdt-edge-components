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

class ActuatorDataTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	ActuatorData. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	DEFAULT_NAME = "ActuatorDataFooBar"
	DEFAULT_STATE_DATA = "{state: None}"
	DEFAULT_VALUE = 15.2
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing ActuatorData class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testDefaultValues(self):
		ad = ActuatorData()
		
		self.assertEquals(ad.getCommand(), ConfigConst.DEFAULT_COMMAND)
		self.assertEquals(ad.getStatusCode(), ConfigConst.DEFAULT_STATUS)
		
		logging.info("Actuator data as string: " + str(ad))

	def testParameterUpdates(self):
		ad = self._createTestActuatorData()
		
		self.assertEquals(ad.getName(), self.DEFAULT_NAME)
		self.assertEquals(ad.getCommand(), ConfigConst.COMMAND_ON)
		self.assertEquals(ad.getStateData(), self.DEFAULT_STATE_DATA)
		self.assertEquals(ad.getValue(), self.DEFAULT_VALUE)

	def testFullUpdate(self):
		ad = ActuatorData()
		ad2 = self._createTestActuatorData()
		
		ad.updateData(ad2)
		
		self.assertEquals(ad.getCommand(), ConfigConst.COMMAND_ON)
		self.assertEquals(ad.getStateData(), self.DEFAULT_STATE_DATA)
		self.assertEquals(ad.getValue(), self.DEFAULT_VALUE)
		
	def _createTestActuatorData(self):
		ad = ActuatorData()
		
		ad.setName(self.DEFAULT_NAME)
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setStateData(self.DEFAULT_STATE_DATA)
		ad.setValue(self.DEFAULT_VALUE)
		
		logging.info("Actuator data as string: " + str(ad))
		
		return ad

if __name__ == "__main__":
	unittest.main()
	