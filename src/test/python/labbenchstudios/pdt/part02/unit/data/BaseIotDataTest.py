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

from labbenchstudios.pdt.data.BaseIotData import BaseIotData

class BaseIotDataTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	BaseIotData. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	DEFAULT_NAME = "TestIotDataSample"
	DEFAULT_LOCATION_ID = "MyLocation"
	DEFAULT_STATUS_CODE = 1
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing BaseIotData class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testDefaultValues(self):
		td = TestIotData()
		
		self.assertEqual(td.getName(), ConfigConst.NOT_SET)
		self.assertEqual(td.getTypeID(), ConfigConst.DEFAULT_TYPE_ID)
		self.assertEqual(td.getLocationID(), "constraineddevice001") # from PiotConfig.props
		self.assertEqual(td.getStatusCode(), ConfigConst.DEFAULT_STATUS)

	def testParameterUpdates(self):
		td = self._createTestIotData()
		
		self.assertEqual(td.getName(), self.DEFAULT_NAME)
		self.assertEqual(td.getLocationID(), self.DEFAULT_LOCATION_ID)
		self.assertEqual(td.getStatusCode(), self.DEFAULT_STATUS_CODE)
		
		td.setStatusCode(-1)
		
		self.assertTrue(td.hasErrorFlag())

	def testFullUpdate(self):
		td = TestIotData()
		td2 = self._createTestIotData()
		
		self.assertEqual(td.getName(), ConfigConst.NOT_SET)
		self.assertEqual(td.getLocationID(), "constraineddevice001") # from PiotConfig.props
		self.assertEqual(td.getStatusCode(), ConfigConst.DEFAULT_STATUS)
		
		td.updateData(td2)
		
		self.assertEqual(td.getName(), self.DEFAULT_NAME)
		self.assertEqual(td.getLocationID(), self.DEFAULT_LOCATION_ID)
		self.assertEqual(td.getStatusCode(), self.DEFAULT_STATUS_CODE)
		
	def _createTestIotData(self):
		td = TestIotData()
		
		td.setName(self.DEFAULT_NAME)
		td.setLocationID(self.DEFAULT_LOCATION_ID)
		td.setStatusCode(self.DEFAULT_STATUS_CODE)
		
		return td

class TestIotData(BaseIotData):
	def __init__(self, typeID: int = ConfigConst.DEFAULT_TYPE_ID, name = ConfigConst.NOT_SET, d = None):
		super(TestIotData, self).__init__(name = name, typeID = typeID, d = d)
		
		pass

if __name__ == "__main__":
	unittest.main()
	