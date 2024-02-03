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

from labbenchstudios.pdt.data.SensorData import SensorData

class SensorDataTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	SensorData. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	DEFAULT_NAME = "SensorDataFooBar"
	TEST_COUNT = 2
	MIN_VALUE = 10.0
	MAX_VALUE = 50.0
	AVG_VALUE = ((MIN_VALUE + MAX_VALUE) / TEST_COUNT)
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing SensorData class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testDefaultValues(self):
		sd = SensorData()
		
		self.assertEqual(sd.getName(), ConfigConst.NOT_SET)
		self.assertEqual(sd.getValue(), ConfigConst.DEFAULT_VAL)
		
		logging.info("Sensor data as string: " + str(sd))

	def testParameterUpdates(self):
		sd = self._createTestSensorData()
		
		self.assertEqual(sd.getName(), self.DEFAULT_NAME)
		self.assertEqual(sd.getValue(), self.MIN_VALUE)

	def testFullUpdate(self):
		sd = SensorData()
		sd2 = self._createTestSensorData()
		
		sd.updateData(sd2)
		
		self.assertEqual(sd.getName(), self.DEFAULT_NAME)
		self.assertEqual(sd.getValue(), self.MIN_VALUE)
	
	def _createTestSensorData(self):
		sd = SensorData()
		
		sd.setName(self.DEFAULT_NAME)
		sd.setValue(self.MIN_VALUE)
		
		logging.info("Sensor data as string: " + str(sd))
		
		return sd

if __name__ == "__main__":
	unittest.main()
	