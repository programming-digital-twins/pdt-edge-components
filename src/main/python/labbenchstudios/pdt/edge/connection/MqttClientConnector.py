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
import traceback

import paho.mqtt.client as mqttClient

import ssl

import labbenchstudios.pdt.common.ConfigConst as ConfigConst

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.common.IDataMessageListener import IDataMessageListener
from labbenchstudios.pdt.common.ResourceNameContainer import ResourceNameContainer
from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum

from labbenchstudios.pdt.edge.connection.IPubSubClient import IPubSubClient

from labbenchstudios.pdt.data.DataUtil import DataUtil

class MqttClientConnector(IPubSubClient):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, clientID: str = None):
		"""
		Default constructor. This will set remote broker information and client connection
		information based on the default configuration file contents.
		
		@param clientID Defaults to None. Can be set by caller. If this is used, it's
		critically important that a unique, non-conflicting name be used so to avoid
		causing the MQTT broker to disconnect any client using the same name. With
		auto-reconnect enabled, this can cause a race condition where each client with
		the same clientID continuously attempts to re-connect, causing the broker to
		disconnect the previous instance.
		"""
		self.config = ConfigUtil()
		self.dataMsgListener = None
		
		self.host = \
			self.config.getProperty( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
			
		self.port = \
			self.config.getInteger( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
		
		self.keepAlive = \
			self.config.getInteger( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.defaultQos = \
			self.config.getInteger( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
		
		self.enableEncryption = \
			self.config.getBoolean( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.ENABLE_CRYPT_KEY)
		
		self.pemFileName = \
			self.config.getProperty( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.CERT_FILE_KEY)
		
		self.mqttClient = None
		
		self.deviceID = \
			self.config.getProperty( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_ID_KEY, 'EdgeDeviceApp')
		
		self.clientID = \
			self.config.getProperty( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY, 'EdgeDeviceApp')
		
		logging.info('\tMQTT Client ID:   ' + self.clientID)
		logging.info('\tMQTT Broker Host: ' + self.host)
		logging.info('\tMQTT Broker Port: ' + str(self.port))
		logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))
		
	def connectClient(self) -> bool:
		if not self.mqttClient:
			# TODO: make clean_session configurable
			self.mqttClient = mqttClient.Client(client_id = self.clientID, clean_session = False)
			
			try:
				if self.enableEncryption:
					logging.info("Enabling TLS encryption...")
					
					self.port = \
						self.config.getInteger( \
							ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.SECURE_PORT_KEY, ConfigConst.DEFAULT_MQTT_SECURE_PORT)
		
					self.mqttClient.tls_set(self.pemFileName, tls_version = ssl.PROTOCOL_TLS)

			except Exception as e:
				logging.warning("Failed to enable TLS encryption. Using unencrypted connection.")
				traceback.print_exception(type(e), e, e.__traceback__)
		
		if self.mqttClient:
			if not self.mqttClient.is_connected():
				self.mqttClient.on_connect = self.onConnect
				self.mqttClient.on_disconnect = self.onDisconnect
				self.mqttClient.on_message = self.onMessage
				self.mqttClient.on_publish = self.onPublish
				self.mqttClient.on_subscribe = self.onSubscribe

				logging.info('MQTT client connecting to broker at host: ' + self.host)

				self.mqttClient.connect(self.host, self.port, self.keepAlive)
				self.mqttClient.loop_start()
				
				return True
			else:
				logging.warning('MQTT client is already connected. Ignoring connect request.')

		else:
			logging.error('MQTT client could not be created. Check logs and exceptions for details.')

		return False
	
	def disconnectClient(self) -> bool:
		"""
		"""
		if self.mqttClient and self.mqttClient.is_connected():
			logging.info('Disconnecting MQTT client from broker: ' + self.host)
			self.mqttClient.loop_stop()
			self.mqttClient.disconnect()
			
			return True
		else:
			logging.warning('MQTT client already disconnected. Ignoring.')
			
			return False
			
	def onConnect(self, client, userdata, flags, rc):
		logging.info('[Callback] Connected to MQTT broker. Result code: ' + str(rc))
		
		actuatorCmdTopic = \
			ConfigConst.PRODUCT_NAME + '/' + self.deviceID + '/' + ConfigConst.ACTUATOR_CMD

		# NOTE: Be sure to set `self.defaultQos` during instantiation!
		self.mqttClient.subscribe( \
			topic = actuatorCmdTopic, qos = self.defaultQos)
		
		self.mqttClient.message_callback_add( \
			sub = actuatorCmdTopic, \
			callback = self.onActuatorCommandMessage)
		
		logging.info('Subscribed to incoming command topic: ' + actuatorCmdTopic)
		
	def onDisconnect(self, client, userdata, rc):
		"""
		"""
		logging.info('MQTT client disconnected from broker: ' + str(client))
		
	def onMessage(self, client, userdata, msg):
		"""
		"""
		payload = msg.payload
		
		if payload:
			logging.info('MQTT message received with payload: ' + str(payload.decode("utf-8")))
		else:
			logging.info('MQTT message received with no payload: ' + str(msg))
			
		if self.dataMsgListener:
			self.dataMsgListener.handleIncomingMessage(resource = ResourceNameEnum.CDA_UPDATE_NOTIFICATIONS_RESOURCE, msg = payload)
			
	def onActuatorCommandMessage(self, client, userdata, msg):
		"""
		This callback is used to process incoming actuator events
		from the subscribed ActuatorCmd topic.
		
		@param client The client reference context.
		@param userdata The user reference context.
		@param msg The message context, including the embedded payload.
		"""
		logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)
		
		if self.dataMsgListener:
			try:
				# assumes all data is encoded using UTF-8 and that the data
				# is in a JSON format that DataUtil can deserialize
				actuatorData = DataUtil().jsonToActuatorData(msg.payload.decode('utf-8'))
				
				self.dataMsgListener.handleActuatorCommandMessage(data = actuatorData)
			except:
				logging.exception("Failed to convert incoming actuation command payload to ActuatorData: ")
					
	def onPublish(self, client, userdata, mid):
		"""
		"""
		logging.info('MQTT client published msg to broker.')
		
	def onSubscribe(self, client, userdata, mid, granted_qos):
		"""
		"""
		logging.info('MQTT client subscribed to topic on broker: ' + str(client))
		
	def publishMessage(self, resource: ResourceNameContainer = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
		"""
		"""
		# check validity of resource (topic)
		if not resource:
			logging.warning('No topic specified. Cannot publish message.')
			return False
		
		# check validity of message
		if not msg:
			logging.warning('No message specified. Cannot publish message to topic: ' + resource.value)
			return False
					
		# check validity of QoS - set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
		
		# publish message, and wait for publish to complete before returning
		if self.mqttClient:
			msgInfo = self.mqttClient.publish(topic = resource.value, payload = msg, qos = qos)
			msgInfo.wait_for_publish()

			return True
		else:
			logging.warning('MQTT client not yet created. Call connectClient() first.')
			return False
	
	def subscribeToTopic(self, resource: ResourceNameContainer = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
		"""
		"""
		# check validity of resource (topic)
		if not resource:
			logging.warning('No topic specified. Cannot subscribe.')
			return False
		
		# check validity of QoS - set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
		
		# subscribe to topic
		if self.mqttClient:
			logging.info('Subscribing to topic %s', resource.value)
			self.mqttClient.subscribe(resource.value, qos)

			return True

		else:
			logging.warning('MQTT client not yet created. Call connectClient() first.')
			return False
	
	def subscribeToTopicByName(self, resource: str = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
		"""
		"""
		# check validity of resource (topic)
		if not resource:
			logging.warning('No topic specified. Cannot subscribe.')
			return False
		
		# check validity of QoS - set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
		
		# subscribe to topic
		if self.mqttClient:
			logging.info('Subscribing to topic %s', resource)
			self.mqttClient.subscribe(resource, qos)
		
			return True

		else:
			logging.warning('MQTT client not yet created. Call connectClient() first.')
			return False
	
	def unsubscribeFromTopic(self, resource: ResourceNameContainer = None):
		"""
		"""
		# check validity of resource (topic)
		if not resource:
			logging.warning('No topic specified. Cannot unsubscribe.')
			return False
		
		# unsubscribe from topic
		if self.mqttClient:
			logging.info('Unsubscribing from topic %s', resource.value)
			self.mqttClient.unsubscribe(resource.value)

			return True

		else:
			logging.warning('MQTT client not yet created. Call connectClient() first.')
			return False

	def setDataMessageListener(self, listener: IDataMessageListener = None):
		"""
		"""
		if listener:
			self.dataMsgListener = listener
