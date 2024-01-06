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

from pisense import SenseHAT

class SenseHatEmulatorQuickTest(unittest.TestCase):
	"""
	This test case class contains very basic unit tests for
	verifying the SenseHAT emulator is properly installed and
	currently running. It should not be considered complete,
	but serve as a starting point for the student implementing
	additional functionality within their Programming the IoT
	environment.
	
	NOTE: This test requires the sense_emu_gui to be running
	and must have access to the underlying libraries that
	support the pisense module. On Windows, one way to do
	this is by installing pisense and sense-emu within the
	Bash on Ubuntu on Windows environment and then execute this
	test case from the command line, as it will likely fail
	if run within an IDE in native Windows.
	
	"""
	HELLO_WORLD_A = "Hello, world!"
	HELLO_WORLD_B = "Welcome to Connected Devices!"
	
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing SenseHatEmulatorQuickTest class [using SenseHAT emulator]...")
		self.sh = SenseHAT(emulate = True)
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testCheckEmulator(self):
		self.assertTrue(self.sh.screen)
		
		self.sh.screen.scroll_text(self.HELLO_WORLD_A)
		self.sh.screen.scroll_text(self.HELLO_WORLD_B)
		self.sh.screen.scroll_text("Current temperature is: " + str(self.sh.environ.temperature))
		
		sleep(5)
		
		self.sh.screen.clear()
		self.sh.screen.close()
				
if __name__ == "__main__":
	unittest.main()
	