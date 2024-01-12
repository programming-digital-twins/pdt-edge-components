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

import logging
import datetime
import dateutil
import socket
import traceback

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener
from labbenchstudios.pdt.common.ResourceNameContainer import ResourceNameContainer
from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum

from labbenchstudios.pdt.edge.connection.IPersistenceClient import IPersistenceClient

from labbenchstudios.pdt.data.DataUtil import DataUtil
from labbenchstudios.pdt.data.ActuatorData import ActuatorData
from labbenchstudios.pdt.data.ConnectionStateData import ConnectionStateData
from labbenchstudios.pdt.data.SensorData import SensorData
from labbenchstudios.pdt.data.SystemPerformanceData import SystemPerformanceData

class InfluxClientConnector(IPersistenceClient):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, \
		serverHost: str = None, serverPort: int = None, \
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

		self.host = \
			self.config.getProperty( \
				ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)

		self.port = \
			self.config.getInteger( \
				ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_TSDB_PORT)
			
		self.clientID = \
			self.config.getProperty( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY, 'EdgeDeviceApp')
		
		self.clientToken = None
		self.orgID = None

		authDict = self.config.getCredentials(ConfigConst.DATA_GATEWAY_SERVICE)

		if authDict:
			ct = authDict[ConfigConst.USER_AUTH_TOKEN_KEY]
			oid = authDict[ConfigConst.ORG_TOKEN_KEY]

			if ct:
				self.clientToken = ct

			if oid:
				self.orgID = oid
				
		self.defaultQos = \
			self.config.getInteger( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
		
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

			logging.info('Created Influx DB client instance and write / query API instances.')

		return True
	
	def disconnectClient(self) -> bool:
		"""
		Disconnects from the persistence server if the client is already connected.
		If not, this call is ignored, but will return a False.
		
		@return bool True on success; False otherwise.
		"""
		if not self.dbClient:
			logging.warning('InfluxDB client not yet created / connected. Ignoring.')

		return True

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

	def loadConnectionStateData(self, resource: ResourceNameContainer = None, typeID: int = 0, startDate: datetime = None, endDate: datetime = None) -> ConnectionStateData:
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

	def storeActuatorData(self, resource: ResourceNameContainer = None, qos: int = 0, data: ActuatorData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""
		if (data):
			dataPoint = self._createActuatorDataPoint(data)
			bucketName = ConfigConst.CMD_DATA_PERSISTENCE_NAME
			deviceID = data.getDeviceID()

			if (resource):
				if (resource.getPersistenceName()) : bucketName = resource.getPersistenceName()

			self.dbClientWriteApi.write(bucket = bucketName, record = dataPoint)

			logging.debug('Wrote ActuatorData instance %s to bucket %s', deviceID, bucketName)

			return True
		
		else:
			logging.warning('Invalid resource name and / or data container. Ignoring store SensorData request.')

		return False

	def storeConnectionStateData(self, resource: ResourceNameContainer = None, qos: int = 0, data: ConnectionStateData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""
		if (data):
			dataPoint = self._createConnectionStateDataPoint(data)
			bucketName = ConfigConst.CONN_DATA_PERSISTENCE_NAME
			deviceID = data.getDeviceID()

			if (resource):
				if (resource.getPersistenceName()) : bucketName = resource.getPersistenceName()

			self.dbClientWriteApi.write(bucket = bucketName, record = dataPoint)

			logging.debug('Wrote ConnectionStateData instance %s to bucket %s', deviceID, bucketName)

			return True
		
		else:
			logging.warning('Invalid resource name and / or data container. Ignoring store SensorData request.')

		return False

	def storeSensorData(self, resource: ResourceNameContainer = None, qos: int = 0, data: SensorData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""
		if (data):
			dataPoint = self._createSensorDataPoint(data)
			bucketName = ConfigConst.SENSOR_DATA_PERSISTENCE_NAME
			deviceID = data.getDeviceID()

			if (resource):
				if (resource.getPersistenceName()) : bucketName = resource.getPersistenceName()

			self.dbClientWriteApi.write(bucket = bucketName, record = dataPoint)

			logging.debug('Wrote SensorData instance %s to bucket %s', deviceID, bucketName)
			
			return True
		
		else:
			logging.warning('Invalid resource name and / or data container. Ignoring store SensorData request.')

		return False

	def storeSystemPerformanceData(self, resource: ResourceNameContainer = None, qos: int = 0, data: SystemPerformanceData = None) -> bool:
		"""
		Attempts to write the source data instance to the persistence server.
		
		@param resource The target resource name.
		@param qos The intended target QoS.
		@param data The data instance to store.
		@return boolean True on success; false otherwise.
		"""
		if (data):
			dataPoint = self._createSystemPerformanceDataPoint(data)
			bucketName = ConfigConst.SYS_DATA_PERSISTENCE_NAME
			deviceID = data.getDeviceID()

			if (resource):
				if (resource.getPersistenceName()) : bucketName = resource.getPersistenceName()

			self.dbClientWriteApi.write(bucket = bucketName, record = dataPoint)

			logging.debug('Wrote SystemPerformanceData instance %s to bucket %s', deviceID, bucketName)
			
			return True
		
		else:
			logging.warning('Invalid resource name and / or data container. Ignoring store SensorData request.')

		return False

	def _convertIso8601TimeStampToMillis(self, timeStampStr: str = None) -> int:
		"""
		A simple conversion function that accepts an expected ISO 8601
		timestamp string and translates into milliseconds.

		@param timeStampStr
		@return int
		"""
		timeParser = dateutil.parser.parse(timeStampStr)
		timeStampMillis = int(timeParser.timestamp() * 1000)

		return timeStampMillis

	def _createActuatorDataPoint(self, data: ActuatorData = None) -> Point:
		"""
		Creates an InfluxDB Point instance for the given type.
		
		@return Point The Point instance that represents the given
		data type container.
		"""
		timeStampMillis = self._convertIso8601TimeStampToMillis(data.getTimeStamp())

		dataPoint = \
			Point(data.getName()) \
				.tag(ConfigConst.DEVICE_ID_PROP, data.getDeviceID()) \
				.tag(ConfigConst.LOCATION_ID_PROP, data.getLocationID()) \
				.tag(ConfigConst.TYPE_ID_PROP, data.getTypeID()) \
				.tag(ConfigConst.TYPE_CATEGORY_ID_PROP, data.getTypeCategoryID()) \
				.field(ConfigConst.COMMAND_PROP, data.getCommand()) \
				.field(ConfigConst.STATE_DATA_PROP, data.getStateData()) \
				.field(ConfigConst.STATUS_CODE_PROP, data.getStatusCode()) \
				.field(ConfigConst.VALUE_PROP, data.getValue()) \
				.time(timeStampMillis, write_precision = "ms")

		return dataPoint

	def _createConnectionStateDataPoint(self, data: ConnectionStateData = None) -> Point:
		"""
		Creates an InfluxDB Point instance for the given type.
		
		@return Point The Point instance that represents the given
		data type container.
		"""
		timeStampMillis = self._convertIso8601TimeStampToMillis(data.getTimeStamp())
		
		dataPoint = \
			Point(data.getName()) \
				.tag(ConfigConst.DEVICE_ID_PROP, data.getDeviceID()) \
				.tag(ConfigConst.LOCATION_ID_PROP, data.getLocationID()) \
				.tag(ConfigConst.TYPE_ID_PROP, data.getTypeID()) \
				.tag(ConfigConst.TYPE_CATEGORY_ID_PROP, data.getTypeCategoryID()) \
				.field(ConfigConst.HOST_NAME_PROP, data.getHostName()) \
				.field(ConfigConst.PORT_KEY, data.getHostPort()) \
				.field(ConfigConst.MESSAGE_IN_COUNT_PROP, data.getMessageInCount()) \
				.field(ConfigConst.MESSAGE_OUT_COUNT_PROP, data.getMessageOutCount()) \
				.field(ConfigConst.IS_CONNECTING_PROP, data.isClientConnecting()) \
				.field(ConfigConst.IS_CONNECTED_PROP, data.isClientConnected()) \
				.field(ConfigConst.IS_DISCONNECTED_PROP, data.isClientDisconnected()) \
				.time(timeStampMillis, write_precision = "ms")

		return dataPoint

	def _createSensorDataPoint(self, data: SensorData = None) -> Point:
		"""
		Creates an InfluxDB Point instance for the given type.
		
		@return Point The Point instance that represents the given
		data type container.
		"""
		timeStampMillis = self._convertIso8601TimeStampToMillis(data.getTimeStamp())
		
		dataPoint = \
			Point(data.getName()) \
				.tag(ConfigConst.DEVICE_ID_PROP, data.getDeviceID()) \
				.tag(ConfigConst.LOCATION_ID_PROP, data.getLocationID()) \
				.tag(ConfigConst.TYPE_ID_PROP, data.getTypeID()) \
				.tag(ConfigConst.TYPE_CATEGORY_ID_PROP, data.getTypeCategoryID()) \
				.field(ConfigConst.VALUE_PROP, data.getValue()) \
				.time(timeStampMillis, write_precision = "ms")

		return dataPoint

	def _createSystemPerformanceDataPoint(self, data: SystemPerformanceData = None) -> Point:
		"""
		Creates an InfluxDB Point instance for the given type.
		
		@return Point The Point instance that represents the given
		data type container.
		"""
		timeStampMillis = self._convertIso8601TimeStampToMillis(data.getTimeStamp())
		
		dataPoint = \
			Point(data.getName()) \
				.tag(ConfigConst.DEVICE_ID_PROP, data.getDeviceID()) \
				.tag(ConfigConst.LOCATION_ID_PROP, data.getLocationID()) \
				.tag(ConfigConst.TYPE_ID_PROP, data.getTypeID()) \
				.tag(ConfigConst.TYPE_CATEGORY_ID_PROP, data.getTypeCategoryID()) \
				.field(ConfigConst.CPU_UTIL_PROP, data.getCpuUtilization()) \
				.field(ConfigConst.MEM_UTIL_PROP, data.getMemoryUtilization()) \
				.field(ConfigConst.DISK_UTIL_PROP, data.getDiskUtilization()) \
				.time(timeStampMillis, write_precision = "ms")

		return dataPoint
