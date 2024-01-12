##
# MIT License
# 
# Copyright (c) 2024 Andrew D. King
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

import datetime

from labbenchstudios.pdt.common.ResourceNameContainer import ResourceNameContainer

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.ConnectionStateData import ConnectionStateData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class IDataLoader():
	"""
	Interface definition for data loader clients.
	
	"""
	
	def loadActuatorData(self, resource: ResourceNameContainer = None, typeID: int = 0, startDate: datetime = None, endDate: datetime = None) -> ActuatorData:
		"""
		Attempts to retrieve the named data instance from the persistence server.
		Will return null if there's no data matching the given type with the
		given parameters.
		
		@param resource The target resource name.
		@param typeID The type ID of the data to retrieve.
		@param startDate The start date (null if narrowing is not needed).
		@param endDate The end date (null if narrowing is not needed).
		@return ActuatorData[] The data instance(s) associated with the lookup parameters.
		"""
		pass

	def loadConnectionStateData(self, resource: ResourceNameContainer = None, startDate: datetime = None, endDate: datetime = None) -> ConnectionStateData:
		"""
		Attempts to retrieve the named data instance from the persistence server.
		Will return null if there's no data matching the given type with the
		given parameters.
		
		@param resource The target resource name.
		@param startDate The start date (null if narrowing is not needed).
		@param endDate The end date (null if narrowing is not needed).
		@return ConnectionStateData[] The data instance(s) associated with the lookup parameters.
		"""
		pass

	def loadSensorData(self, resource: ResourceNameContainer = None, typeID: int = 0, startDate: datetime = None, endDate: datetime = None) -> SensorData:
		"""
		Attempts to retrieve the named data instance from the persistence server.
		Will return null if there's no data matching the given type with the
		given parameters.
		
		@param resource The target resource name.
		@param typeID The type ID of the data to retrieve.
		@param startDate The start date (null if narrowing is not needed).
		@param endDate The end date (null if narrowing is not needed).
		@return SensorData[] The data instance(s) associated with the lookup parameters.
		"""
		pass

	def loadSystemPerformanceData(self, resource: ResourceNameContainer = None, startDate: datetime = None, endDate: datetime = None) -> SystemPerformanceData:
		"""
		Attempts to retrieve the named data instance from the persistence server.
		Will return null if there's no data matching the given type with the
		given parameters.
		
		@param resource The target resource name.
		@param startDate The start date (null if narrowing is not needed).
		@param endDate The end date (null if narrowing is not needed).
		@return SystemPerformanceData[] The data instance(s) associated with the lookup parameters.
		"""
		pass
