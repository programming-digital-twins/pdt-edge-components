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

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil

class ConfigUtilTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	ConfigUtil. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	"""
	DEFAULT_USER = "Foo"
	DEFAULT_AUTH = "Bar"
	
	# optionally test the following files
	#  - EmptyTestConfig.props
	#  - InvalidTestConfig.props
	#  - None (which will default to ./config/PdtConfig.props)
	configFile = "./ValidTestConfig.props"
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing ConfigUtil class...")
		self.configUtil = ConfigUtil(configFile = self.configFile)
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testGetBooleanProperty(self):
		enableLogging = self.configUtil.hasProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_LOGGING_KEY)
		self.assertTrue(enableLogging)
	
	#@unittest.skip("Ignore for now.")
	def testGetCredentials(self):
		creds = self.configUtil.getCredentials(ConfigConst.CONSTRAINED_DEVICE)
		self.assertIsNotNone(creds)
		self.assertEqual(creds[ConfigConst.USER_NAME_TOKEN_KEY], self.DEFAULT_USER)
		self.assertEqual(creds[ConfigConst.USER_AUTH_TOKEN_KEY], self.DEFAULT_AUTH)
		pass
		
	def testGetIntegerProperty(self):
		port = self.configUtil.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY)
		self.assertEqual(port, ConfigConst.DEFAULT_MQTT_PORT)
	
	def testGetFloatProperty(self):
		hSimFloor = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_FLOOR_KEY)
		self.assertGreater(hSimFloor, 0.0)
	
	def testGetProperty(self):
		hostName = self.configUtil.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY)
		self.assertTrue(hostName)
	
	def testHasProperty(self):
		self.assertTrue(self.configUtil.hasProperty(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY))

	def testHasSection(self):
		self.assertTrue(self.configUtil.hasSection(ConfigConst.CONSTRAINED_DEVICE))
	
	def testIsConfigDataLoaded(self):
		self.assertTrue(self.configUtil.isConfigDataLoaded())
	
if __name__ == "__main__":
	unittest.main()
