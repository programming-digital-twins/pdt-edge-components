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

import json
import logging

from decimal import Decimal
from json import JSONEncoder

from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class DataUtil():
	"""

	"""

	def __init__(self, encodeToUtf8 = False):
		"""
		Constructor.
		
		@param encodeToUtf8 False by default. If true, will disable ascii
		output in JSON encoder and output UTF-8 encoded strings instead.
		"""
		self.encodeToUtf8 = encodeToUtf8
		
		logging.info("Created DataUtil instance.")
	
	def actuatorDataToJson(self, data: ActuatorData = None, useDecForFloat: bool = False):
		"""
		Convert ActuatorData object to JSON string.
		
		@param data The ActuatorData object to convert.
		@param useDecForFloat If true, any float value will be replaced as a Decimal.
		@return A JSON text string representing 'actuatorData',
		if ActuatorData is valid.
		"""
		if not data:
			logging.debug("ActuatorData is null. Returning empty string.")
			return ""
		
		logging.debug("Encoding ActuatorData to JSON [pre]  --> " + str(data))
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = False)
		
		logging.info("Encoding ActuatorData to JSON [post] --> " + str(jsonData))
		
		return jsonData
	
	def sensorDataToJson(self, data: SensorData = None, useDecForFloat: bool = False):
		"""
		Convert SensorData object to JSON string.
		
		@param data The SensorData object to convert.
		@param useDecForFloat If true, any float value will be replaced as a Decimal.
		@return A JSON text string representing 'sensorData',
		if SensorData is valid.
		"""		
		if not data:
			logging.debug("SensorData is null. Returning empty string.")
			return ""
		
		logging.debug("Encoding SensorData to JSON [pre]  --> " + str(data))
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = False)
		
		logging.debug("Encoding SensorData to JSON [post] --> " + str(jsonData))
		
		return jsonData

	def systemPerformanceDataToJson(self, data: SystemPerformanceData = None, useDecForFloat: bool = False):
		"""
		Convert SystemPerformanceData object to JSON string.
		
		@param data The SystemPerformanceData object to convert.
		@param useDecForFloat If true, any float value will be replaced as a Decimal.
		@return A JSON text string representing 'sysPerfData',
		if SystemPerformanceData is valid.
		"""
		if not data:
			logging.debug("SystemPerformanceData is null. Returning empty string.")
			return ""
		
		logging.debug("Encoding SystemPerformanceData to JSON [pre]  --> " + str(data))
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = False)
		
		logging.debug("Encoding SystemPerformanceData to JSON [post] --> " + str(jsonData))
		
		return jsonData
	
	def jsonToActuatorData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Convert JSON string to ActuatorData object.
		
		@param jsonData The JSON string data to convert into an
		ActuatorData instance.
		@param useDecForFloat If true, any float value will be replaced as a Decimal.
		@return ActuatorData An ActuatorData object representing 'jsonData',
		if jsonData is valid.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		logging.debug("Converting JSON to ActuatorData [pre]  --> " + str(jsonStruct))
		
		ad = ActuatorData()
		
		self._updateIotData(jsonStruct, ad)
		
		logging.debug("Converted JSON to ActuatorData [post] --> " + str(ad))
		
		return ad
	
	def jsonToSensorData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Convert JSON string to SensorData object.
		
		@param jsonData The JSON string data to convert into an
		SensorData instance.
		@param useDecForFloat If true, any float value will be replaced as a Decimal.
		@return SensorData A SensorData object representing 'jsonData',
		if jsonData is valid.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		logging.debug("Converting JSON to SensorData [pre]  --> " + str(jsonStruct))
		
		sd = SensorData()
		
		self._updateIotData(jsonStruct, sd)
		
		logging.debug("Converted JSON to SensorData [post] --> " + str(sd))
		
		return sd
	
	def jsonToSystemPerformanceData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Convert JSON string to SystemPerformanceData object.
		
		@param jsonData The JSON string data to convert into an
		SystemPerformanceData instance.
		@param useDecForFloat If true, any float value will be replaced as a Decimal.
		@return SystemPerformanceData A SystemPerformanceData object representing 'jsonData',
		if jsonData is valid.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		logging.debug("Converting JSON to SystemPerformanceData [pre]  --> " + str(jsonStruct))
		
		sp = SystemPerformanceData()
		
		self._updateIotData(jsonStruct, sp)
		
		logging.debug("Converted JSON to SystemPerformanceData [post] --> " + str(sp))
		
		return sp
	
	def _formatDataAndLoadDictionary(self, jsonData: str, useDecForFloat: bool = False) -> dict:
		"""
		Formats the jsonData parameter string by replacing single quotes with
		double quotes, and booleans 'False' and 'True' with 'false' and 'true',
		respectively.
		
		After string replacement, a dictionary struct is generated using the
		json.loads() method, returning the result.
		
		@param jsonData The string-based JSON data to format and load.
		@param useDecForFloat If true, any float value will be replaced as a Decimal.
		@return dict
		"""
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		
		jsonStruct = None
		
		if useDecForFloat:
			jsonStruct = json.loads(jsonData, parse_float = Decimal)
		else:
			jsonStruct = json.loads(jsonData)
		
		return jsonStruct
		
	def _generateJsonData(self, obj, useDecForFloat: bool = False) -> str:
		"""
		Generates JSON data from the passed in object using json.dumps().
		
		@param obj Expected to be a type that can be converted into JSON via JsonDataEncoder.
		@param useDecForFloat If true, any float value will be replaced as a Decimal. This will
		not be required for Part 02 - 03 testing, but may be required for CSP integration if
		this class is used within a FaaS component.
		@return The JSON string.
		"""
		jsonData = None
		
		if self.encodeToUtf8:
			logging.debug("Encoding data obj to JSON using UTF-8 encoding...")
			
			jsonData = json.dumps(obj, cls = JsonDataEncoder).encode('utf8')
		else:
			jsonData = json.dumps(obj, cls = JsonDataEncoder, indent = 4)
		
		if jsonData:
			if useDecForFloat:
				tmpData = json.loads(jsonData, parse_float = Decimal)
				logging.info("\n\nBEFORE:\n\n" + str(jsonData))
				logging.info("\n\nAFTER:\n\n" + str(tmpData))
				#jsonData = json.dumps(tmpData, cls = JsonDataEncoder)
			
			jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		
		return jsonData
	
	def _updateIotData(self, jsonStruct, obj):
		"""
		Maps the JSON key / value pairs contained in jsonStruct to the obj
		instance (which will be one of the sub-classes to BaseIotData).
		
		@param jsonStruct The JSON dictionary as the source key / value data.
		@param obj The BaseIotData sub-class instance to receive the mapping.
		"""
		varStruct = vars(obj)
		
		for key in jsonStruct:
			if key in varStruct:
				#logging.debug("JSON data contains key mappable to object: %s", key)
				setattr(obj, key, jsonStruct[key])
			else:
				logging.warn("JSON data contains key not mappable to object: %s", key)
		
class JsonDataEncoder(JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		return o.__dict__
	