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

from labbenchstudios.pdt.common.ConfigUtil import ConfigUtil
from labbenchstudios.pdt.data.BaseIotData import BaseIotData

class IotDataContext(BaseIotData):
	"""
	classdocs
	
	"""

	def __init__(self, \
		typeCategoryID: int = ConfigConst.DEFAULT_TYPE_ID, \
		typeID: int = ConfigConst.DEFAULT_TYPE_CATEGORY_ID, \
		name: str = ConfigConst.NOT_SET, \
		d = None):
		"""
		Constructor
		
		"""
		super(IotDataContext, self).__init__(name = name, typeID = typeID, d = d)
		
		if d:
			try:
				self.deviceID = d[ConfigConst.DEVICE_ID_PROP]
				self.typeCategoryID = d[ConfigConst.TYPE_CATEGORY_ID_PROP]
			except:
				pass
			
		self.typeCategoryID = typeCategoryID

		# always pull device ID from configuration file
		self.deviceID = \
			ConfigUtil().getProperty( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_ID_PROP)
		
	def getDeviceID(self):
		"""
		Returns the device ID name.
	
		@return The device ID as a String. Default is {@see ConfigConst.NOT_SET}
		"""
		return self.deviceID
	
	def getTypeCategoryID(self):
		"""
		Returns the type category ID, which can be used as a convenient way to
		switch through different IoT data types when processing different data
		types.
	
		@return int
		"""
		return self.typeCategoryID
	
	def setDeviceID(self, idStr: str = None):
		"""
		Sets the device ID as a string. This can be used as a user-friendly label
		to identify the IoT data name or device name. It's usually used as
		the former.<p>
		Validation rules will check if the name is non-null and non-empty
		(post-trim). If the validation fails, nothing is done.
	
		@param name The string-based name to set.
		"""
		if idStr and len(idStr) > 0:
			self.deviceID = idStr
	
	def setTypeCategoryID(self, val: int = ConfigConst.DEFAULT_TYPE_ID):
		"""
		Sets the type categoryID int value. No validation is performed - can be
		any int value permitted by the JVM.
	
		@param id The type category ID int value to set.
		"""
		self.typeCategoryID = val
	
	def __str__(self):
		"""
		String override function.
		
		"""
		s = BaseIotData.__str__(self) + ',{}={},{}={}'
		
		return s.format(
			ConfigConst.DEVICE_ID_PROP, self.deviceID,
			ConfigConst.TYPE_CATEGORY_ID_PROP, self.typeCategoryID)

	def _handleUpdateData(self, data: BaseIotData = None):
		"""
		Implementation of base class template method to update this instance.
	
		@param BaseIotData While the parameter must implement this method,
		the sub-class is expected to cast the base class to its given type.
		"""
		if data and isinstance(data, IotDataContext):
			self.setDeviceID(data.getDeviceID())
			self.setTypeCategoryID(data.getTypeCategoryID())
