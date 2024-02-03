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

from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceDataTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	SystemPerformanceData. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	DEFAULT_NAME = "SystemPerformanceDataFooBar"
	DEFAULT_CPU_UTIL_DATA  = 10.0
	DEFAULT_DISK_UTIL_DATA = 10.0
	DEFAULT_MEM_UTIL_DATA  = 10.0
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing SystemPerformanceData class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testDefaultValues(self):
		spd = SystemPerformanceData()
		
		self.assertEqual(spd.getName(), ConfigConst.SYSTEM_PERF_NAME)
		self.assertEqual(spd.getStatusCode(), ConfigConst.DEFAULT_STATUS)
		
		self.assertEqual(spd.getCpuUtilization(), ConfigConst.DEFAULT_VAL)
		self.assertEqual(spd.getMemoryUtilization(), ConfigConst.DEFAULT_VAL)
		
		logging.info("System perf data as string: " + str(spd))

	def testParameterUpdates(self):
		spd = self._createTestSystemPerformanceData()
		
		self.assertEqual(spd.getName(), self.DEFAULT_NAME)
		
		self.assertEqual(spd.getCpuUtilization(), self.DEFAULT_CPU_UTIL_DATA)
		self.assertEqual(spd.getMemoryUtilization(), self.DEFAULT_MEM_UTIL_DATA)

	def testFullUpdate(self):
		spd = SystemPerformanceData()
		spd2 = self._createTestSystemPerformanceData()
		
		self.assertEqual(spd.getName(), ConfigConst.SYSTEM_PERF_NAME)
		
		self.assertEqual(spd.getCpuUtilization(), ConfigConst.DEFAULT_VAL)
		self.assertEqual(spd.getMemoryUtilization(), ConfigConst.DEFAULT_VAL)
		
		spd.updateData(spd2)
		
		self.assertEqual(spd.getName(), self.DEFAULT_NAME)
		
		self.assertEqual(spd.getCpuUtilization(), self.DEFAULT_CPU_UTIL_DATA)
		self.assertEqual(spd.getMemoryUtilization(), self.DEFAULT_MEM_UTIL_DATA)
	
	def _createTestSystemPerformanceData(self):
		spd = SystemPerformanceData()
		spd.setName(self.DEFAULT_NAME)
		
		spd.setCpuUtilization(self.DEFAULT_CPU_UTIL_DATA)
		spd.setMemoryUtilization(self.DEFAULT_MEM_UTIL_DATA)
		
		logging.info("System perf data as string: " + str(spd))
		
		return spd

if __name__ == "__main__":
	unittest.main()
	