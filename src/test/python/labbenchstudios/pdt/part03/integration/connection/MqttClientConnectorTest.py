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

from labbenchstudios.pdt.edge.connection.MqttClientConnector import MqttClientConnector
from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum
from labbenchstudios.pdt.common.DefaultDataMessageListener import DefaultDataMessageListener
from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.DataUtil import DataUtil

class MqttClientConnectorTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	MqttClientConnector. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing MqttClientConnector class...")
		
		self.cfg = ConfigUtil()
		self.mcc = MqttClientConnector()
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	#@unittest.skip("Ignore for now.")
	def testConnectAndDisconnect(self):
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		
		sleep(delay + 5)
		
		self.mcc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testConnectAndCDAManagementStatusPubSub(self):
		qos = 1
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos = qos)
		sleep(5)
		
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg = "TEST: This is the CDA message payload.", qos = qos)
		sleep(5)
		
		self.mcc.unsubscribeFromTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
		sleep(5)
		
		sleep(delay)
		
		self.mcc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testNewActuatorCmdPubSub(self):
		qos = 1
	
		# NOTE: delay can be anything you'd like - the sleep() calls are simply to slow things down a bit for observation
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		actuatorData = ActuatorData()
		payload = DataUtil().actuatorDataToJson(actuatorData)
		
		self.mcc.setDataMessageListener(DefaultDataMessageListener())
		self.mcc.connectClient()
		
		sleep(5)
		
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, msg = payload, qos = qos)
		
		sleep(delay)
		
		self.mcc.disconnectClient()
		
	#@unittest.skip("Ignore for now.")
	def testActuatorCmdPubSub(self):
		qos = 0
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		actuatorData = ActuatorData()
		actuatorData.setCommand(7)
		
		self.mcc.setDataMessageListener(DefaultDataMessageListener())
		
		payload = DataUtil().actuatorDataToJson(actuatorData)
		
		self.mcc.connectClient()
		
		sleep(5)
				
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, msg = payload, qos = qos)
		
		sleep(delay + 5)
		
		self.mcc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testSensorMsgPub(self):
		qos = 0
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		sensorData = SensorData()
		sensorData.setValue(22.0)
		
		self.mcc.setDataMessageListener(DefaultDataMessageListener())
		
		payload = DataUtil().sensorDataToJson(sensorData)
		
		self.mcc.connectClient()
		
		sleep(5)
				
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = payload, qos = qos)
		
		sleep(delay + 5)
		
		self.mcc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testCDAManagementStatusSubscribe(self):
		qos = 1
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_MGMT_STATUS_CMD_RESOURCE, qos = qos)
		
		sleep(delay)
		
		self.mcc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testCDAActuatorCmdSubscribe(self):
		qos = 1
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, qos = qos)
		
		sleep(300)
		
		self.mcc.disconnectClient()

	#@unittest.skip("Ignore for now.")
	def testCDAManagementStatusPublish(self):
		"""
		Uncomment this test when integration between the GDA and CDA using MQTT.
		
		"""
		qos = 1
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.mcc.connectClient()
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg = "TEST: This is the CDA message payload.", qos = qos)
		
		sleep(delay)
		
		self.mcc.disconnectClient()

if __name__ == "__main__":
	unittest.main()
	