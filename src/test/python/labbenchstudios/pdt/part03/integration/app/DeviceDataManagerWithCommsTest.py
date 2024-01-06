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

from labbenchstudios.pdt.edge.app.DeviceDataManager import DeviceDataManager
from labbenchstudios.pdt.edge.connection.MqttClientConnector import MqttClientConnector

from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum
from labbenchstudios.pdt.data.DataUtil import DataUtil
from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData

class DeviceDataManagerWithCommsTest(unittest.TestCase):
	"""
	This test case class contains very basic integration tests for
	DeviceDataManager. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	
	NOTE: This test MAY require the sense_emu_gui to be running,
	depending on whether or not the 'enableEmulator' flag is
	True within the ConstraineDevice section of PiotConfig.props.
	If so, it must have access to the underlying libraries that
	support the pisense module. On Windows, one way to do
	this is by installing pisense and sense-emu within the
	Bash on Ubuntu on Windows environment and then execute this
	test case from the command line, as it will likely fail
	if run within an IDE in native Windows.
	
	NOTE 2: This test requires you to examine each test case,
	none of which will execute as they're currently disabled.
	Choose the test
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing DeviceDataManager class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	#@unittest.skip("Ignore for now.")
	def testStartAndStopManagerWithMqtt(self):
		"""
		NOTE: Be sure to enable CoAP by setting the following flag to True
		within PiotConfig.props
		enableMqttClient = True
		enableCoapClient = False
		
		"""
		ddMgr = DeviceDataManager()
		ddMgr.startManager()
		
		mqttClient = MqttClientConnector()
		mqttClient.connectClient()
		
		ad = ActuatorData()
		ad.setCommand(ConfigConst.COMMAND_ON)
		ad.setValue(15.4)
		ad.setAsResponse()
		adJson = DataUtil().actuatorDataToJson(ad)
		
		mqttClient.publishMessage(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, msg = adJson, qos = 1)
		
		sd = SensorData()
		sd.setValue(133.5)
		sdJson = DataUtil().sensorDataToJson(sd)
		
		mqttClient.publishMessage(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = sdJson, qos = 1)
		
		sleep(10)
		
		mqttClient.disconnectClient()
		ddMgr.stopManager()

	@unittest.skip("Ignore for now.")
	def testStartAndStopManagerWithCoap(self):
		"""
		NOTE: Be sure to enable CoAP by setting the following flag to True
		within PiotConfig.props
		enableMqttClient = False
		enableCoapClient = True
		
		"""
		
		ddMgr = DeviceDataManager()
		ddMgr.startManager()
		
		sleep(60)
		
		ddMgr.stopManager()

	@unittest.skip("Ignore for now.")
	def testStartAndStopManagerWithMqttAndCoap(self):
		"""
		NOTE: Be sure to enable MQTT and CoAP by setting the following flags to True
		within PiotConfig.props
		enableMqttClient = True
		enableCoapClient = True
		
		"""
		
		ddMgr = DeviceDataManager()
		ddMgr.startManager()
		
		sleep(60)
		
		ddMgr.stopManager()

if __name__ == "__main__":
	unittest.main()
	