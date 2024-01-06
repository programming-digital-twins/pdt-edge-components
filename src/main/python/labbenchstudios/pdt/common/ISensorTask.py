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

from labbenchstudios.pdt.data.SensorData import SensorData

class ISensorTask():
	"""
	This is a simple 'interface' definition for a sensor task abstraction.
	
	You may consider using this as a base class for all actuator
	sim task implementations or not - it's not required.
	"""
	
	def generateTelemetry(self) -> SensorData:
		"""
		Creates a SensorData instance based on the rules of the implementing class.
		
		@return The SensorData instance.
		"""
		pass
	
	def getLatestTelemetry(self) -> SensorData:
		"""
		Returns a newly created SensorData instance as a copy
		of the latest telemetry data generated.
		
		If no telemetry has been generated when this method is
		called, None is returned.
		
		@return SensorData
		"""
		pass
	
	def getName(self) -> str:
		"""
		Returns the name of this simulator.
		
		@return str
		"""
		pass
	
	def getTypeID(self) -> int:
		"""
		Returns the type ID of this simulator.
		
		@return int
		"""
		pass
	
	def getTelemetryValue(self) -> float:
		"""
		Returns the current value from the stored self.latestSensorData instance.
		If it hasn't been generated yet, this will invoke self.generateTelemetry()
		and then return the current value from the generated SensorData.
		
		@return float
		"""
		pass
