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

import datetime
import logging
import socket

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common import ConfigUtil
from labbenchstudios.pdt.common.ResourceNameContainer import ResourceNameContainer
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener

from labbenchstudios.pdt.data import ActuatorData
from labbenchstudios.pdt.data import ConnectionStateData
from labbenchstudios.pdt.data import SensorData
from labbenchstudios.pdt.data import SystemPerformanceData

from labbenchstudios.pdt.edge.connection import IPersistenceClient

class InfluxClientConnector(IPersistenceClient):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, \
		serverHost: str = None, serverPort: int = 0, \
		clientToken: str = None, orgID: str = None):
		"""
		Default constructor. This will set remote TSDB server information and client
		connection information based on the default configuration file contents.
		
		@param serverHost
		@param serverPort
		@param clientToken
		@param orgID
		"""
		self.config = ConfigUtil()
		
		self.clientToken = clientToken
		self.orgID = orgID

		if serverHost:
			self.host = serverHost

		if not self.host:
			self.host = \
				self.config.getProperty( \
					ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)

		if serverPort > 0 and serverPort < 65535:
			self.port = serverPort
		else:
			self.port = \
				self.config.getInteger( \
					ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
		
		self.defaultQos = \
			self.config.getInteger( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
		
		self.clientID = \
			self.config.getProperty( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY, 'EdgeDeviceApp')
		
		self.dbClient = None
		self.dbClientWriteApi = None
		self.dbClientQueryApi = None

		self.uriPath = "http://" + self.host + ":" + str(self.port)
		
		logging.info('\tInfluxDB Host:Port: %s:%s', self.host, str(self.port))
		
		try:
			tmpHost = socket.gethostbyname(self.host)
			
			if tmpHost:
				self.host = tmpHost
			else:
				logging.error("Can't resolve host: " + self.host)
			
		except socket.gaierror:
			logging.info("Failed to resolve host: " + self.host)
			
		logging.info('\tInfluxDB Client ID:   ' + self.clientID)
		logging.info('\tInfluxDB Broker Host: ' + self.host)
		logging.info('\tInfluxDB Broker Port: ' + str(self.port))
		
	def connectClient(self) -> bool:
		"""
		Connects to the persistence server using configuration parameters
		specified by the sub-class.
		
		@return bool True on success; False otherwise.
		"""
		if not self.dbClient:
			self.dbClient = InfluxDBClient(url = self.uriPath, token = self.clientToken, org = self.orgID)
			self.dbClientWriteApi = self.dbClient.write_api(write_options = SYNCHRONOUS)
			self.dbClientQueryApi = self.dbClient.query_api()

			return True
		else:
			logging.warning('InfluxDB client already created / connected. Ignoring.')
			return False

	def disconnectClient(self) -> bool:
		"""
		Disconnects from the persistence server if the client is already connected.
		If not, this call is ignored, but will return a False.
		
		@return bool True on success; False otherwise.
		"""
		if not self.dbClient:
			logging.warning('InfluxDB client not yet created / connected. Ignoring.')

			return False
		else:
			return True
	
	def getActuatorData(self, resource: ResourceNameContainer = None, typeID: int = 0, startDate: datetime = None, endDate: datetime = None) -> ActuatorData:
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

	def getConnectionStateData(self, resource: ResourceNameContainer = None, typeID: int = 0, startDate: datetime = None, endDate: datetime = None) -> ConnectionStateData:
		"""
		Attempts to retrieve the named data instance from the persistence server.
		Will return null if there's no data matching the given type with the
		given parameters.
		
		@param resource The target resource name.
		@param typeID The type ID of the data to retrieve.
		@param startDate The start date (null if narrowing is not needed).
		@param endDate The end date (null if narrowing is not needed).
		@return ConnectionStateData[] The data instance(s) associated with the lookup parameters.
		"""
		pass

	def getSensorData(self, resource: ResourceNameContainer = None, typeID: int = 0, startDate: datetime = None, endDate: datetime = None) -> SensorData:
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

	def getSystemPerformanceData(self, resource: ResourceNameContainer = None, typeID: int = 0, startDate: datetime = None, endDate: datetime = None) -> SystemPerformanceData:
		"""
		Attempts to retrieve the named data instance from the persistence server.
		Will return null if there's no data matching the given type with the
		given parameters.
		
		@param resource The target resource name.
		@param typeID The type ID of the data to retrieve.
		@param startDate The start date (null if narrowing is not needed).
		@param endDate The end date (null if narrowing is not needed).
		@return SystemPerformanceData[] The data instance(s) associated with the lookup parameters.
		"""
		pass

	def storeData(self, resource: ResourceNameContainer = None, qos: int = 0, data: ActuatorData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""
		pass

	def storeData(self, resource: ResourceNameContainer = None, qos: int = 0, data: ConnectionStateData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""
		pass

	def storeData(self, resource: ResourceNameContainer = None, qos: int = 0, data: SensorData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""
		pass

	def storeData(self, resource: ResourceNameContainer = None, qos: int = 0, data: SystemPerformanceData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""
		pass
