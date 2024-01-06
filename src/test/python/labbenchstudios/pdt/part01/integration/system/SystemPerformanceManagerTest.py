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

from labbenchstudios.pdt.edge.system.SystemPerformanceManager import SystemPerformanceManager
from labbenchstudios.pdt.common.DefaultDataMessageListener import DefaultDataMessageListener

class SystemPerformanceManagerTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	SystemPerformanceManager. It should not be considered complete,
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
	
	"""
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing SystemPerformanceManager class...")
		self.spMgr = SystemPerformanceManager()
		self.defaultMsgListener = DefaultDataMessageListener()
		self.spMgr.setDataMessageListener(self.defaultMsgListener)
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testStartAndStopManager(self):
		self.spMgr.startManager()
		
		sleep(60)
		
		self.spMgr.stopManager()

if __name__ == "__main__":
	unittest.main()
	