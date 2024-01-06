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

from time import sleep

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.edge.app.DeviceDataManager import DeviceDataManager

logging.basicConfig(format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s', level = logging.DEBUG)

class EdgeDeviceApp():
	"""
	Definition of the EdgeDeviceApp class.
	
	"""
	
	def __init__(self):
		"""
		Initialization of class.
		
		@param path The name of the resource to apply to the URI.
		"""
		logging.info("Initializing EDA...")
		
		self.dataMgr = DeviceDataManager()

	def startApp(self):
		"""
		Start the CDA. Calls startManager() on the device data manager instance.
		
		"""
		logging.info("Starting EDA...")
		
		self.dataMgr.startManager()
		
		logging.info("EDA started.")

	def stopApp(self, code: int):
		"""
		Stop the EDA. Calls stopManager() on the device data manager instance.
		
		"""
		logging.info("EDA stopping...")
		
		self.dataMgr.stopManager()
		
		logging.info("EDA stopped with exit code %s.", str(code))
		
	def parseArgs(self, args):
		"""
		Parse command line args.
		
		@param args The arguments to parse.
		"""
		logging.info("Parsing command line args...")


def main():
	"""
	Main function definition for running client as application.
	
	Current implementation runs for 65 seconds then exits.
	"""
	cda = EdgeDeviceApp()
	cda.startApp()
	
	runForever = ConfigUtil().getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.RUN_FOREVER_KEY)
	
	if runForever:
		while (True):
			sleep(5)
			
	else:
		sleep(65)
		
		# optionally stop the app - this can be removed if needed
		cda.stopApp(0)

if __name__ == '__main__':
	"""
	Attribute definition for when invoking as app via command line
	
	"""
	main()
	