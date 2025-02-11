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

import argparse
import logging
import os
import traceback

from time import sleep

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.edge.app.DeviceDataManager import DeviceDataManager

LOG_FORMAT = "%(asctime)s:::%(thread)d:%(name)s.%(module)s.%(funcName)s()[%(lineno)s]:%(levelname)s:%(message)s"
logging.basicConfig(format = LOG_FORMAT, level = logging.DEBUG)

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

		self.isStarted = False
		self.dataMgr = DeviceDataManager()

	def isAppStarted(self) -> bool:
		"""
		"""
		return self.isStarted
	
	def startApp(self):
		"""
		Start the CDA. Calls startManager() on the device data manager instance.
		
		"""
		logging.info("Starting EDA...")
		
		configUtil = ConfigUtil()

		if (configUtil.isConfigDataLoaded()):
			self.dataMgr.startManager()
			self.isStarted = True

			logging.info("EDA started.")
		else:
			logging.error("Failed to load config file and properly initialize app. EDA not started.")

	def stopApp(self, code: int):
		"""
		Stop the EDA. Calls stopManager() on the device data manager instance.
		
		"""
		if (self.isStarted):
			logging.info("EDA stopping...")

			self.dataMgr.stopManager()

			logging.info("EDA stopped with exit code %s.", str(code))
		else:
			logging.info("EDA not yet started.")

			pass
		
def main():
	"""
	Main function definition for running client as application.
	
	Current implementation runs for 65 seconds then exits.
	"""
	argParser = argparse.ArgumentParser( \
		description = 'Edge Device Application for simulating data sets as part of the Building Digital Twins course.')
	
	argParser.add_argument('-c', '--configFile', help = 'Optional custom configuration file for the EDA.')

	configFile = None

	try:
		args = argParser.parse_args()
		configFile = args.configFile

		logging.info('Parsed configuration file arg: %s', configFile)
	except:
		logging.info('No arguments to parse.')

	# init ConfigUtil
	configUtil = ConfigUtil(configFile)
	eda = None

	try:
		# init EDA
		eda = EdgeDeviceApp()

		# start EDA
		eda.startApp()

		# check if EDA should run forever
		runForever = configUtil.getBoolean(ConfigConst.EDGE_DEVICE, ConfigConst.RUN_FOREVER_KEY)

		if runForever:
			# sleep ~5 seconds every loop
			while (True):
				sleep(5)
			
		else:
			# run EDA for ~65 seconds then exit
			if (eda.isAppStarted()):
				sleep(65)
				eda.stopApp(0)
			
	except KeyboardInterrupt:
		logging.warning('Keyboard interruption for EDA. Exiting.')

		if (eda):
			eda.stopApp(-1)

	except Exception as e:
		# handle any uncaught exception that may be thrown
		# during EDA initialization
		logging.error('Startup exception caused EDA to fail. Exiting.')
		traceback.print_exception(type(e), e, e.__traceback__)

		if (eda):
			eda.stopApp(-2)

	# unnecessary
	logging.info('Exiting EDA.')
	exit()

if __name__ == '__main__':
	"""
	Attribute definition for when invoking as app via command line
	
	"""
	main()
	
def parseArgs(self, args):
	"""
	Parse command line args.
	
	@param args The arguments to parse.
	"""
	logging.info("Parsing command line args...")
