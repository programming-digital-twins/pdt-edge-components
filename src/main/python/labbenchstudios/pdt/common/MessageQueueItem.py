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

class MessageQueueItem():
	"""
	Basic (default) implementation of an object that can be processed within the state machine's message queue.
	
	"""

	def __init__(self, msgData = None, callbackFunc = None):
		"""
		Default constructor. This will set remote server information and client connection
		information based on the default configuration file contents.
		
		"""
		self.msgData = msgData
		self.callbackFunc = callbackFunc

		logging.info("MessageQueueItem initialized: %s(%s)", str(self.callbackFunc), str(self.msgData))

	def invokeCallback(self) -> bool:
		"""
		Convenience method to invoke the callback function ref with the msgData param.

		"""

		# TODO: wrap in try / except
		if self.callbackFunc:
			logging.info("Invoking callback function with msg data: %s(%s)", str(self.callbackFunc), str(self.msgData))
			self.callbackFunc(self.msgData)

			return True
		else:
			logging.warning("No callback function ref. Nothing to invoke. Ignoring.")

			return False

	def resetItem(self):
		"""
		Simply sets all data local ref's to None.

		"""
		self.msgData = None
