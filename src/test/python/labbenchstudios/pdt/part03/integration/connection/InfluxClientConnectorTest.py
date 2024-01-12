##
# MIT License
# 
# Copyright (c) 2024 Andrew D. King
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
from tarfile import data_filter
import unittest

from time import sleep

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.edge.connection.InfluxClientConnector import InfluxClientConnector

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.ResourceNameContainer import ResourceNameContainer
from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum
from labbenchstudios.pdt.common.DefaultDataMessageListener import DefaultDataMessageListener

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.DataUtil import DataUtil
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData
from labbenchstudios.pdt.data.ConnectionStateData import ConnectionStateData

class InfluxClientConnectorTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	InfluxClientConnector. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing InfluxClientConnector class...")
		
		self.cfg = ConfigUtil()
		self.icc = InfluxClientConnector()
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	#@unittest.skip("Ignore for now.")
	def testConnectAndDisconnect(self):
		delay = 20
		
		self.icc.connectClient()
		
		sleep(delay + 5)
		
		self.icc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testActuatorDataWrite(self):
		delay = 20
		
		self.icc.connectClient()

		data = ActuatorData()
		data.setCommand(7)
		
		resource = ResourceNameContainer(resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)

		self.icc.storeActuatorData(resource = resource, data = data)
		
		self.icc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testConnectionStateDataWrite(self):
		delay = 20
		
		self.icc.connectClient()

		data = ConnectionStateData()
		data.setHostName("localhost")
		data.setHostPort(8080)
		data.setIsClientConnectedFlag(True)
		
		resource = ResourceNameContainer(resource = ResourceNameEnum.CDA_UPDATE_NOTIFICATIONS_RESOURCE)

		self.icc.storeConnectionStateData(resource = resource, data = data)
		
		self.icc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testSensorDataWrite(self):
		delay = 20
		
		self.icc.connectClient()

		data = SensorData()
		data.setValue(24.0)
		
		resource = ResourceNameContainer(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE)

		self.icc.storeSensorData(resource = resource, data = data)
		
		self.icc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testSystemPerformanceDataWrite(self):
		delay = 20
		
		self.icc.connectClient()

		data = SystemPerformanceData()
		data.setCpuUtilization(18.0)
		data.setMemoryUtilization(9.0)
		data.setDiskUtilization(2.0)
		
		resource = ResourceNameContainer(resource = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE)

		self.icc.storeSystemPerformanceData(resource = resource, data = data)
		
		self.icc.disconnectClient()


if __name__ == "__main__":
	unittest.main()
	