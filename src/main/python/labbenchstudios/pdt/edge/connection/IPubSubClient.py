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

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ResourceNameContainer import ResourceNameContainer
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener

class IPubSubClient():
	"""
	Interface definition for pub/sub clients.
	
	"""
	
	def connectClient(self) -> bool:
		"""
		Connects to the pub/sub broker / server using configuration parameters
		specified by the sub-class.
		
		@return bool True on success; False otherwise.
		"""
		pass

	def disconnectClient(self) -> bool:
		"""
		Disconnects from the pub/sub broker / server if the client is already connected.
		If not, this call is ignored, but will return a False.
		
		@return bool True on success; False otherwise.
		"""
		pass

	def publishMessage(self, resource: ResourceNameContainer = None, payload: str = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
		"""
		Attempts to publish a message to the given topic with the given qos
		to the pub/sub broker / server. If not already connected, the sub-class
		implementation should either throw an exception, or handle the exception
		and log a message, and return False.
		
		@param resource The topic container holding the topic value to publish the message to.
		@param msg The message to publish. This is expected to be well-formed JSON.
		@param qos The QoS level. This is expected to be 0 - 2. Default is DEFAULT_QOS.
		@return bool True on success; False otherwise.
		"""
		pass

	def subscribeToTopic(self, resource: ResourceNameContainer = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
		"""
		Attempts to subscribe to a topic with the given qos hosted by the
		pub/sub broker / server. If not already connected, the sub-class
		implementation should either throw an exception, or handle the exception
		and log a message, and return False.
		
		@param resource The topic container holding the topic value to publish the message to.
		@param callback The callback function reference to use for incoming messages
		destined for the resource named topic. Default is None, which means the default
		incoming message callback should be used instead.
		@param qos The QoS level. This is expected to be 0 - 2. Default is DEFAULT_QOS.
		@return bool True on success; False otherwise.
		"""
		pass

	def unsubscribeFromTopic(self, resource: ResourceNameContainer = None) -> bool:
		"""
		Attempts to unsubscribe from a topic hosted by the pub/sub broker / server.
		If not already connected, the sub-class implementation should either
		throw an exception, or handle the exception and log a message, and return False.
		
		@param resource The topic container holding the topic value to publish the message to.
		@return bool True on success; False otherwise.
		"""
		pass

	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		"""
		Sets the data message listener reference, assuming listener is non-null.
		
		@param listener The data message listener instance to use for passing relevant
		messages, such as those received from a subscription event.
		@return bool True on success (if listener is non-null will always be the case); False otherwise.
		"""
		pass
	