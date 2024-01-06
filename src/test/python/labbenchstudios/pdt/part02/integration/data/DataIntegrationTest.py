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
import os
import unittest

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from pathlib import Path

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.data.DataUtil import DataUtil

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class DataIntegrationTest(unittest.TestCase):
	"""
	This test case class contains very basic integration tests for
	DataUtil and data container classes for use between the CDA and
	GDA to verify JSON compatibility. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Running DataIntegrationTest test cases...")
		
		encodeToUtf8 = False
		
		self.dataUtil = DataUtil(encodeToUtf8)

		self.cdaDataPath = ConfigUtil().getProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEST_CDA_DATA_PATH_KEY)
		self.gdaDataPath = ConfigUtil().getProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEST_GDA_DATA_PATH_KEY)
		
		if not os.path.exists(self.cdaDataPath):
			logging.info("================================================")
			logging.info("DataIntegrationTest - path needs to be created: " + self.cdaDataPath)
			os.makedirs(self.cdaDataPath, exist_ok = True)
			
	def setUp(self):
		logging.info("================================================")
		logging.info("DataIntegrationTest test execution...")
		logging.info("================================================")
		
		pass

	def tearDown(self):
		pass
	
	#@unittest.skip("Ignore for now.")
	def testWriteActuatorDataToCdaDataPath(self):
		logging.info("\n\n----- [ActuatorData to JSON to file] -----")
		
		dataObj  = ActuatorData()
		dataStr  = self.dataUtil.actuatorDataToJson(dataObj)
		fileName = self.cdaDataPath + '/ActuatorData.dat'

		logging.info("Sample ActuatorData JSON (validated): " + str(dataStr))
		logging.info("Writing ActuatorData JSON to CDA data path: " + fileName)
		
		fileRef = Path(fileName)
		fileRef.write_text(dataStr, encoding = 'utf-8')
		
	#@unittest.skip("Ignore for now.")
	def testWriteSensorDataToCdaDataPath(self):
		logging.info("\n\n----- [SensorData to JSON to file] -----")
		
		dataObj  = SensorData()
		dataStr  = self.dataUtil.sensorDataToJson(dataObj)
		fileName = self.cdaDataPath + '/SensorData.dat'

		logging.info("Sample SensorData JSON (validated): " + str(dataStr))
		logging.info("Writing SensorData JSON to CDA data path: " + fileName)
		
		fileRef = Path(fileName)
		fileRef.write_text(dataStr, encoding = 'utf-8')

	#@unittest.skip("Ignore for now.")
	def testWriteSystemPerformanceDataToCdaDataPath(self):
		logging.info("\n\n----- [SystemPerformanceData to JSON to file] -----")
		
		dataObj  = SystemPerformanceData()
		dataStr  = self.dataUtil.sensorDataToJson(dataObj)
		fileName = self.cdaDataPath + '/SystemPerformanceData.dat'

		logging.info("Sample SystemPerformanceData JSON (validated): " + str(dataStr))
		logging.info("Writing SystemPerformanceData JSON to CDA data path: " + fileName)
		
		fileRef = Path(fileName)
		fileRef.write_text(dataStr, encoding = 'utf-8')

	#@unittest.skip("Ignore for now.")
	def testReadActuatorDataFromGdaDataPath(self):
		logging.info("\n\n----- [ActuatorData JSON from file to object] -----")
		
		fileName = self.gdaDataPath + '/ActuatorData.dat'
		fileRef  = Path(fileName)
		dataStr  = fileRef.read_text(encoding = 'utf-8')

		dataObj  = self.dataUtil.jsonToActuatorData(dataStr)

		logging.info("ActuatorData JSON from GDA: " + dataStr)
		logging.info("ActuatorData object: " + str(dataObj))

	#@unittest.skip("Ignore for now.")
	def testReadSensorDataFromGdaDataPath(self):
		logging.info("\n\n----- [SensorData JSON from file to object] -----")
		
		fileName = self.gdaDataPath + '/SensorData.dat'
		fileRef  = Path(fileName)
		dataStr  = fileRef.read_text(encoding = 'utf-8')

		dataObj  = self.dataUtil.jsonToSensorData(dataStr)

		logging.info("SensorData JSON from GDA: " + dataStr)
		logging.info("SensorData object: " + str(dataObj))

	#@unittest.skip("Ignore for now.")
	def testReadSystemPerformanceDataFromGdaDataPath(self):
		logging.info("\n\n----- [SystemPerformanceData JSON from file to object] -----")
		
		fileName = self.gdaDataPath + '/SystemPerformanceData.dat'
		fileRef  = Path(fileName)
		dataStr  = fileRef.read_text(encoding = 'utf-8')

		dataObj  = self.dataUtil.jsonToSystemPerformanceData(dataStr)

		logging.info("SystemPerformanceData JSON from GDA: " + dataStr)
		logging.info("SystemPerformanceData object: " + str(dataObj))

if __name__ == "__main__":
	unittest.main()
