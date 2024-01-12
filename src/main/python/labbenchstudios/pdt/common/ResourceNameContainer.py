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

from labbenchstudios.pdt.common.ResourceNameEnum import ResourceNameEnum
from labbenchstudios.pdt.data.IotDataContext import IotDataContext

class ResourceNameContainer(object):
	"""
	classdocs
	"""


	def __init__(self, resource: ResourceNameEnum = None, data: IotDataContext = None, topic: str = None):
		"""
		Constructor
		
		"""

		self.resourceSubTypeSeparator = ConfigConst.SUB_TYPE_SEPARATOR_CHAR
		
		self.productPrefix	     = ConfigConst.PRODUCT_NAME
		self.deviceName	         = ConfigConst.NOT_SET
		self.fullResourceName    = ConfigConst.NOT_SET
		self.fullTypeName	     = ConfigConst.NOT_SET
		self.resourceTypeName	 = ConfigConst.NOT_SET
		self.resourceSubTypeName = None
		self.typeCategoryID      = ConfigConst.DEFAULT_TYPE_ID
		self.persistenceName     = None
		
		self.isActuationResource = False
		self.isMediaResource     = False
		self.isSensingResource   = False
		self.isSystemResource    = False
		self.isSubscription      = False
		
		self.iotDataContext      = data
		
		if not resource:
			resource = ResourceNameEnum.SYSTEM_REQUEST_RESOURCE
			
		self._initResource(resource = resource)
		
		if data:
			if data.getDeviceID():
				self.deviceName = data.getDeviceID()
				
			if data.getName():
				self.resourceTypeName = data.getName()
				
			self.typeID = data.getTypeID()
			self.typeCategoryID = data.getTypeCategoryID()			
		else:
			self.typeID = ConfigConst.DEFAULT_TYPE_ID
			
		if topic:
			self.originationTopic = topic
		else:
			self.originationTopic = None
			
		self._initResourceName()
			
	def getDeviceName(self):
		"""
		Returns the device named used for this resource.
		Defaults to {@see ConfigConst.NOT_SET}
	
		@return str The device name.
		"""
		return self.deviceName
	
	def getFullResourceName(self):
		"""
		Returns the fully qualified resource name. This will used the resource enum
		stored internally and swap out the device name portion with {@see #deviceName}
		if it's been explicitly set to a valid device name.
		
		@return str The adjusted, fully qualified resource name.
		"""
		return self.fullResourceName
	
	def getFullTypeName(self):
		"""
		Returns the full type name, which is the last part of of the topic name.
		It will either be represented as two sub-topics, or as a single sub-topic
		as a concatenation of the resource type and sub-type.
	
		@return str
		"""
		return self.fullTypeName
	
	def getGenericDeviceFullResourceName(self):
		"""
		Returns the generic device resource name. This will delegate to the
		{@see ResourceTypeEnum#getGenericResourceName} method, which is simply
		the resource enum with {@see ConfigConst.LEVEL_WILDCARD} as the device name.
	
		@return str
		"""
		genDevResName = self.fullResourceName.replace(self.deviceName, ConfigConst.LEVEL_WILDCARD)
		
		return genDevResName
	
	def getIotDataContext(self):
		"""
		Returns the IoT data context reference.
		
		@return IotDataContext
		"""
		return self.iotDataContext
	
	def getOriginationTopic(self):
		"""
		Returns the origination topic set during construction, or null if there
		is none.
	
		@return str
		"""
		return self.originationTopic
	
	def getPersistenceName(self):
		"""
		Returns the persistence name. This may be a bucket name for TSDB storage,
		or a generic name to identify this resource to a particular data store.

		@return str
		"""
	def getProductPrefix(self):
		"""
		Returns the resource product prefix, which is the string content that
		precedes the device name.
	
		@return str
		"""
		return self.productPrefix
	
	def getResourceTypeName(self):
		"""
		Returns the resource type. This will always be the content following
		the device name.
	
		@return str The resource type.
		"""
		return self.resourceTypeName
	
	def getResourceSubTypeName(self):
		"""
		Returns the resource sub-type. This will always be the content following
		the device name and the resource type.
	
		@return str The resource sub-type.
		"""
		return self.resourceSubTypeName
	
	def getTypeCategoryID(self):
		"""
		Returns the type category value.
	
		@return int
		"""
		return self.typeCategoryID
	
	def getTypeID(self):
		"""
		Returns the type ID value.
	
		@return int
		"""
		return self.typeID

	def isActuationResource(self):
		"""
		Returns the flag indicating if this resource is associated with actuation.
		
		@return boolean True if this is a actuation resource.
		"""
		return self.isActuationResource
	
	def isMediaResource(self):
		"""
		Returns the flag indicating if this resource is associated with media.
		
		@return boolean True if this is a media resource.
		"""
		return self.isMediaResource
	
	def isSensingResource(self):
		"""
		Returns the flag indicating if this resource is associated with sensing.
		
		@return boolean True if this is a sensing resource.
		"""
		return self.isSensingResource
	
	def isSystemResource(self):
		"""
		Returns the flag indicating if this resource is associated with the system.
		
		@return boolean True if this is a system resource.
		"""
		return self.isSystemResource
		
	def isSubscriptionResource(self):
		"""
		Returns the flag indicating if this resource is for subscribing.
	
		@return boolean True if this is a subscription resource false otherwise.
		"""
		return self.isSubscription
	
	def setAsActuationResource(self, enable: bool = False):
		"""
		Sets the named flag.
		
		@param enable
		"""
		self.isActuationResource = enable
	
	def setAsMediaResource(self, enable: bool = False):
		"""
		Sets the named flag.
		
		@param enable
		"""
		self.isMediaResource = enable
	
	def setAsSensingResource(self, enable: bool = False):
		"""
		Sets the named flag.
		
		@param enable
		"""
		self.isSensingResource = enable
	
	def setAsSystemResource(self, enable: bool = False):
		"""
		Sets the named flag.
		
		@param enable
		"""
		self.isSystemResource = enable
	
	def setAsSubscriptionResource(self, enable: bool = False):
		"""
		Sets the isSubscription flag to indicate this resource either is (true)
		or is not (false) a subscription resource.
	
		@param enable
		"""
		self.isSubscription = enable
	
	def setDeviceName(self, name: str = None):
		"""
		Sets the device name used for this resource container.
	
		@param deviceName The name of the device to set as part of the resource name.
		"""
		if name and len(name.strip()) > 0:
			self.deviceName = name.strip()
			
			self._initResourceName()
	
	def setPersistenceName(self, name: str = None):
		"""
		Sets the persistence name for this resource container. If valie, it will
		stored internally as a reference to the persistence bucket name or other
		persistence 'tag' associated with the contents of this container.

		@param name The persistence name to set.
		"""
		if name and len(name.strip()) > 0:
			self.persistenceName = name.strip()

	def setProductPrefix(self, name: str = None):
		"""
		Sets the product prefix for this resource container. If valid, it will
		be used to replace the current prefix, as defined by the internally
		stored ResourceTypeEnum (which is the product name).
	
		@param name
		"""
		if name and len(name.strip()) > 0:
			self.productPrefix = name.strip()
			
			self._initResourceName()
	
	def setResourceType(self, name: str = None):
		"""
		Sets the resource type name.
	
		@param name
		"""
		if name and len(name.strip()) > 0:
			self.resourceTypeName = name.strip()
			
			self._initResourceName()
	
	def setResourceSubType(self, name: str = None):
		"""
		Sets the resource type sub-name, which - if valid - will append
		the current resource type name with a hyphen ('-') and the given
		name.
		
		@param name
		"""
		if name and len(name.strip()) > 0:
			self.resourceSubTypeName = name.strip()
			
			self._initResourceName()
	
	def setTypeID(self, val: int = ConfigConst.DEFAULT_TYPE_ID):
		"""
		Sets the type ID for this resource.
	
		@param id
		"""
		self.typeID = val
	
	def useSubTopicForSubResourceTypes(self, enable: bool = False):
		"""
		Sets the flag indicating the sub-resource type should either be a
		sub-topic from the resource type (true) or an extension of the resource
		type (false). If the former, the resource separator char will
		be used {@see ConfigConst.RESOURCE_SEPARATOR_CHAR}, otherwise, the
		default will be used {@see ConfigConst.SUB_TYPE_SEPARATOR_CHAR}.
	
		@param enable
		"""
		if enable:
			self.resourceSubTypeSeparator = ConfigConst.RESOURCE_SEPARATOR_CHAR
		else:
			self.resourceSubTypeSeparator = ConfigConst.SUB_TYPE_SEPARATOR_CHAR
		
		self._initResourceName()
	
	def _initResource(self, resource: ResourceNameEnum = None):
		"""
		Initializes the resource name string using the local
		{@see ResourceTypeEnum} and sets the components of the resource,
		such as the product prefix, device name, and resource type.
	
		"""
		if resource == ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE or \
		   resource == ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE:
			self.isActuationResource = True
		else:
			self.isSensingResource = True
		
		# temporary - can be overridden later
		self.typeID = self.typeCategoryID
		
		self._initResourceName()
	
	def _initResourceName(self):
		"""
		Initializes the resource name by generating a fully qualified resource
		using the individual components of the name. These are initially set
		using the ResourceTypeEnum passed into the constructor, but can be
		replaced using the individual setter methods.
	
		Upon each successfully setter method call, this method will be invoked
		to re-generate the fully qualified resource name.
	
		"""
		self.fullResourceName = \
			self.productPrefix + ConfigConst.RESOURCE_SEPARATOR_CHAR + \
			self.deviceName + ConfigConst.RESOURCE_SEPARATOR_CHAR
			
		self._initResourceTypeName()
		
		self.fullResourceName = self.fullResourceName + self.fullTypeName
	
	def _initResourceTypeName(self):
		"""
		Initializes the full type name, which comprises the ending of the topic.
		This can be the resource type only, or include the resource sub-type as
		either an appendage to the resource type (via a connecting char, like
		a hyphen), or a new sub-topic level following the resource type.
		e.g., SensorMsg-Temp
		e.g., SensorMsg/Temp
	
		"""
		# ensure naming consistency - resource types may or may not
		# end with ConfigConst.MSG - if not, append it to the name
		endStr = self.resourceTypeName
		
		if not endStr.endswith(ConfigConst.MSG):
			endStr = endStr + ConfigConst.MSG
			
		if self.resourceSubTypeName:
			self.fullTypeName = endStr + str(self.resourceSubTypeSeparator) + str(self.resourceSubTypeName)
		else:
			self.fullTypeName = endStr
