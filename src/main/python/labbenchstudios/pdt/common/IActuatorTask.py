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

from labbenchstudios.pdt.data.ActuatorData import ActuatorData

class IActuatorTask():
	"""
	This is a simple 'interface' for an Actuator abstraction.
	
	You may consider using this as a base class for all actuator
	sim task implementations or not - it's not required.
	"""

	def getSimpleName(self) -> str:
		"""
		Returns the simplified name passed in from the sub-class.
		
		@return String
		"""
		pass
	
	def updateActuator(self, data: ActuatorData) -> ActuatorData:
		"""
		Updates the actuator state using the given ActuatorData.
		Performs basic validation internally - optionally, add a
		template method definition (e.g. def _validateData(data: ActuatorData) -> bool:),
		call, which can be overridden by the sub-class if needed.
		May also trigger a call to activate or deactivate the
		actuator, depending upon the command within data.
		
		This will setup the actuation call after validating
		'data', then invoke the 'private' _handleActuation() method,
		which in turn returns the status code to be used in the
		response data.
		
		@param data The ActuatorData to process.
		@return ActuatorData A new ActuatorData updated with the original command and the response flag enabled.
		"""
		pass
	