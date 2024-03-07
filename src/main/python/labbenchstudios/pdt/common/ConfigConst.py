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

"""
Configuration and other constants for use when looking up
configuration values or when default values may be needed.
 
"""

#####
# General Names and Defaults
#

NOT_SET = 'Not Set'
RESOURCE_SEPARATOR_CHAR = '/'
SUB_TYPE_SEPARATOR_CHAR = '-'

DEFAULT_HOST             = 'localhost'
DEFAULT_COAP_PORT        = 5683
DEFAULT_COAP_SECURE_PORT = 5684
DEFAULT_MQTT_PORT        = 1883
DEFAULT_MQTT_SECURE_PORT = 8883
DEFAULT_TSDB_PORT        = 8086
DEFAULT_RTSP_STREAM_PORT = 8554
DEFAULT_KEEP_ALIVE       = 60
DEFAULT_POLL_CYCLES      = 60
DEFAULT_VAL              = 0.0
DEFAULT_COMMAND          = 0
DEFAULT_STATUS           = 0
DEFAULT_TIMEOUT          = 5
DEFAULT_TTL              = 300
DEFAULT_QOS              = 0

# for purposes of this library, float precision is more then sufficient
DEFAULT_LAT = DEFAULT_VAL
DEFAULT_LON = DEFAULT_VAL
DEFAULT_ELEVATION = DEFAULT_VAL

DEFAULT_ACTION_ID = 0
INITIAL_SEQUENCE_NUMBER = 0

DEFAULT_STREAM_FPS             =    30
DEFAULT_MIN_STREAM_FPS         =     8
DEFAULT_MAX_STREAM_FPS         =    60
DEFAULT_STREAM_FRAME_WIDTH     =  1440
DEFAULT_STREAM_FRAME_HEIGHT    =  1080
DEFAULT_MIN_MOTION_PIXELS_DIFF = 12000
DEFAULT_MAX_CACHED_FRAMES      =    10
DEFAULT_STREAM_PROTOCOL        = 'rtsp'
DEFAULT_STREAM_FPS = 30
DEFAULT_MIN_MOTION_PIXELS_DIFF = 10000
DEFAULT_STREAM_PROTOCOL = 'rtsp'

PRODUCT_NAME = 'PDT'
CLOUD        = 'Cloud'
GATEWAY      = 'Gateway'
EDGE         = 'Edge'
CONSTRAINED  = EDGE
# NOTE: CONSTRAINED global name has been changed to use EDGE for PDT
#CONSTRAINED  = 'Constrained'
DEVICE       = 'Device'
SERVICE      = 'Service'

# CONSTRAINED_DEVICE and EDGE_DEVICE will be the same
# They're both used for backwards compatability
CONSTRAINED_DEVICE = CONSTRAINED + DEVICE
EDGE_DEVICE        = EDGE + DEVICE
GATEWAY_SERVICE    = GATEWAY + SERVICE
CLOUD_SERVICE      = CLOUD + SERVICE

#####
# Property Names
#

NAME_PROP        = 'name'
DEVICE_ID_PROP   = 'deviceID'
TYPE_CATEGORY_ID_PROP = 'typeCategoryID'
TYPE_ID_PROP     = 'typeID'
TIMESTAMP_PROP   = 'timeStamp'
HAS_ERROR_PROP   = 'hasError'
STATUS_CODE_PROP = 'statusCode'
LOCATION_ID_PROP = 'locationID'
LATITUDE_PROP    = 'latitude'
LONGITUDE_PROP   = 'longitude'
ELEVATION_PROP   = 'elevation'

COMMAND_PROP     = 'command'
STATE_DATA_PROP  = 'stateData'
VALUE_PROP       = 'value'
IS_RESPONSE_PROP = 'isResponse'

CPU_UTIL_PROP    = 'cpuUtil'
DISK_UTIL_PROP   = 'diskUtil'
MEM_UTIL_PROP    = 'memUtil'

ACTION_ID_PROP             = 'actionID'
DATA_URI_PROP              = 'dataURI'
MESSAGE_PROP               = 'message'
ENCODING_NAME_PROP         = 'encodingName'
RAW_DATA_PROP              = 'rawData'
SEQUENCE_NUMBER_PROP       = 'seqNo'
USE_SEQUENCE_NUMBER_PROP   = 'useSeqNo'
SEQUENCE_NUMBER_TOTAL_PROP = 'seqNoTotal'

SEND_RESOURCE_NAME_PROP    = 'sendResourceName'
RECEIVE_RESOURCE_NAME_PROP = 'receiveResourceName'
IS_PING_PROP               = 'isPing'

MESSAGE_DATA_PROP          = 'msgData'

HOST_NAME_PROP             = 'hostName'
MESSAGE_IN_COUNT_PROP      = 'msgInCount'
MESSAGE_OUT_COUNT_PROP     = 'msgOutCount'
IS_CONNECTING_PROP         = 'isConnecting'
IS_CONNECTED_PROP          = 'isConnected'
IS_DISCONNECTED_PROP       = 'isDisconnected'

CMD_DATA_PERSISTENCE_NAME    = 'pdt-cmd-data'
CONN_DATA_PERSISTENCE_NAME   = 'pdt-conn-data'
SENSOR_DATA_PERSISTENCE_NAME = 'pdt-sensor-data'
SYS_DATA_PERSISTENCE_NAME    = 'pdt-sys-data'

#####
# Resource and Topic Names
#

MSG = 'Msg'

ACTUATOR_CMD      = 'ActuatorCmd'
ACTUATOR_RESPONSE = 'ActuatorResponse'
MGMT_STATUS_MSG   = 'MgmtStatusMsg'
MGMT_STATUS_CMD   = 'MgmtStatusCmd'
MEDIA_MSG         = 'MediaMsg'
SENSOR_MSG        = 'SensorMsg'
SYSTEM_PERF_MSG   = 'SystemPerfMsg'

UPDATE_NOTIFICATIONS_MSG      = 'UpdateMsg'
RESOURCE_REGISTRATION_REQUEST = 'ResourceRegRequest'

LED_ACTUATOR_NAME        = 'Lighting'
HUMIDIFIER_ACTUATOR_NAME = 'Humidifier'
HVAC_ACTUATOR_NAME       = 'Thermostat'

HUMIDITY_SENSOR_NAME = 'Humidifier'
PRESSURE_SENSOR_NAME = 'Barometer'
TEMP_SENSOR_NAME     = 'Thermostat'
SYSTEM_MGMT_NAME     = 'EdgeComputingDevice'
SYSTEM_PERF_NAME     = 'EdgeComputingDevice'
CAMERA_SENSOR_NAME   = 'Camera'

COMMAND_ON  = 1
COMMAND_OFF = 2
COMMAND_MSG_ONLY = 5

DEFAULT_TYPE_ID           =    0
DEFAULT_TYPE_CATEGORY_ID  =    0
DEFAULT_ACTUATOR_TYPE     = DEFAULT_TYPE_ID
DEFAULT_SENSOR_TYPE       = DEFAULT_TYPE_ID

ENV_DEVICE_TYPE           = 1000
ENV_TYPE_CATEGORY         = 1000
HVAC_ACTUATOR_TYPE        = 1001
HUMIDIFIER_ACTUATOR_TYPE  = 1002

HUMIDITY_SENSOR_TYPE      = 1010
PRESSURE_SENSOR_TYPE      = 1012
TEMP_SENSOR_TYPE          = 1013

DISPLAY_DEVICE_TYPE       = 2000
LED_DISPLAY_ACTUATOR_TYPE = 2001

CAMERA_SENSOR_NAME        = 'CameraSensor'
MEDIA_TYPE_NAME           = 'MediaType'
MEDIA_TYPE_CATEGORY       = 3000
DEFAULT_MEDIA_TYPE        = 3000
MEDIA_DEVICE_TYPE         = 3000
CAMERA_SENSOR_TYPE        = 3001
CAMERA_MOTION_SENSOR_TYPE = 3002
CAMERA_STREAM_SENSOR_TYPE = 3004

SYSTEM_MGMT_TYPE          = 8000
SYSTEM_MGMT_TYPE_CATEGORY = 8000
RESOURCE_MGMT_TYPE        = 8001

RESOURCE_MGMT_NAME        = 'ResourceMgmt'

SYSTEM_PERF_TYPE          = 9000
SYSTEM_PERF_TYPE_CATEGORY = 9000
CPU_UTIL_TYPE             = 9001
DISK_UTIL_TYPE            = 9002
MEM_UTIL_TYPE             = 9003

CPU_UTIL_NAME  = 'DeviceCpuUtil'
DISK_UTIL_NAME = 'DeviceDiskUtil'
MEM_UTIL_NAME  = 'DeviceMemUtil'

#####
# typical topic naming conventions
#

# for CDA to GDA communications
# e.g., PIOT/ConstrainedDevice/ActuatorCmd
# e.g., PIOT/ConstrainedDevice/SensorMsg

SYSTEM_REQUEST_RESOURCE = PRODUCT_NAME + '/' + SYSTEM_MGMT_NAME

CDA_UPDATE_NOTIFICATIONS_MSG_RESOURCE = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + UPDATE_NOTIFICATIONS_MSG
CDA_ACTUATOR_CMD_MSG_RESOURCE         = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + ACTUATOR_CMD
CDA_ACTUATOR_RESPONSE_MSG_RESOURCE    = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + ACTUATOR_RESPONSE
CDA_MGMT_STATUS_MSG_RESOURCE          = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + MGMT_STATUS_MSG
CDA_MGMT_CMD_MSG_RESOURCE             = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + MGMT_STATUS_CMD
CDA_MEDIA_DATA_MSG_RESOURCE           = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + MEDIA_MSG
CDA_REGISTRATION_REQUEST_RESOURCE     = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + RESOURCE_REGISTRATION_REQUEST
CDA_SENSOR_DATA_MSG_RESOURCE          = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + SENSOR_MSG
CDA_SYSTEM_PERF_MSG_RESOURCE          = PRODUCT_NAME + '/' + CONSTRAINED_DEVICE + '/' + SYSTEM_PERF_MSG

#####
# Configuration Sections, Keys and Defaults
#

# NOTE: You may need to update these paths if you change
# the directory structure for python-components

DEFAULT_CONFIG_FILE_NAME = '/mnt/d/pdt/pdt-edge-components/config/PdtConfig.props'
DEFAULT_CRED_FILE_NAME   = '/mnt/d/pdt/pdt-edge-components/cred/PdtCred.props'

TEST_GDA_DATA_PATH_KEY = 'testGdaDataPath'
TEST_CDA_DATA_PATH_KEY = 'testCdaDataPath'

LOCAL   = 'Local'
DATA    = 'Data'
MQTT    = 'Mqtt'
COAP    = 'Coap'
OPCUA   = 'Opcua'
SMTP    = 'Smtp'

DEVICE_ID_KEY          = 'deviceID'
DEVICE_LOCATION_ID_KEY = 'deviceLocationID'

CLOUD_GATEWAY_SERVICE = CLOUD   + '.' + GATEWAY_SERVICE
COAP_GATEWAY_SERVICE  = COAP    + '.' + GATEWAY_SERVICE
DATA_GATEWAY_SERVICE  = DATA    + '.' + GATEWAY_SERVICE
MQTT_GATEWAY_SERVICE  = MQTT    + '.' + GATEWAY_SERVICE
OPCUA_GATEWAY_SERVICE = OPCUA   + '.' + GATEWAY_SERVICE
SMTP_GATEWAY_SERVICE  = SMTP    + '.' + GATEWAY_SERVICE

CRED_SECTION = "Credentials"

FROM_ADDRESS_KEY     = 'fromAddr'
TO_ADDRESS_KEY       = 'toAddr'
TO_MEDIA_ADDRESS_KEY = 'toMediaAddr'
TO_TXT_ADDRESS_KEY   = 'toTxtAddr'

HOST_KEY             = 'host'
PORT_KEY             = 'port'
SECURE_PORT_KEY      = 'securePort'

ROOT_CERT_ALIAS = 'root';

KEY_STORE_CLIENT_IDENTITY_KEY = 'keyStoreClientIdentity';
KEY_STORE_SERVER_IDENTITY_KEY = 'keyStoreServerIdentity';

KEY_STORE_FILE_KEY    = 'keyStoreFile';
KEY_STORE_AUTH_KEY    = 'keyStoreAuth';
TRUST_STORE_FILE_KEY  = 'trustStoreFile';
TRUST_STORE_ALIAS_KEY = 'trustStoreAlias';
TRUST_STORE_AUTH_KEY  = 'trustStoreAuth';
USER_NAME_TOKEN_KEY   = 'userToken'
USER_AUTH_TOKEN_KEY   = 'authToken'
API_TOKEN_KEY         = 'apiToken'
ORG_TOKEN_KEY         = 'orgToken'

CERT_FILE_KEY        = 'certFile'
CRED_FILE_KEY        = 'credFile'
ENABLE_AUTH_KEY      = 'enableAuth'
ENABLE_CRYPT_KEY     = 'enableCrypt'
ENABLE_SIMULATOR_KEY = 'enableSimulator'
ENABLE_EMULATOR_KEY  = 'enableEmulator'
ENABLE_SENSE_HAT_KEY = 'enableSenseHAT'
ENABLE_LOGGING_KEY   = 'enableLogging'
USE_WEB_ACCESS_KEY   = 'useWebAccess'
POLL_CYCLES_KEY      = 'pollCycleSecs'
KEEP_ALIVE_KEY       = 'keepAlive'
DEFAULT_QOS_KEY      = 'defaultQos'

ENABLE_TSDB_CLIENT_KEY = 'enableTsdbClient'
ENABLE_MQTT_CLIENT_KEY = 'enableMqttClient'
ENABLE_COAP_CLIENT_KEY = 'enableCoapClient'
ENABLE_COAP_SERVER_KEY = 'enableCoapServer'

ENABLE_SYSTEM_PERF_KEY = 'enableSystemPerformance'
ENABLE_SENSING_KEY     = 'enableSensing'

UPDATE_DISPLAY_ON_ACTUATION_KEY = 'updateDisplayOnActuation'

HUMIDITY_SIM_FLOOR_KEY   = 'humiditySimFloor'
HUMIDITY_SIM_CEILING_KEY = 'humiditySimCeiling'
PRESSURE_SIM_FLOOR_KEY   = 'pressureSimFloor'
PRESSURE_SIM_CEILING_KEY = 'pressureSimCeiling'
TEMP_SIM_FLOOR_KEY       = 'tempSimFloor'
TEMP_SIM_CEILING_KEY     = 'tempSimCeiling'

HANDLE_TEMP_CHANGE_ON_DEVICE_KEY = 'handleTempChangeOnDevice'
TRIGGER_HVAC_TEMP_FLOOR_KEY   = 'triggerHvacTempFloor'
TRIGGER_HVAC_TEMP_CEILING_KEY = 'triggerHvacTempCeiling'

RUN_FOREVER_KEY    = 'runForever'
TEST_EMPTY_APP_KEY = 'testEmptyApp'

STREAM_HOST_ADDR_KEY       = 'streamHostAddr'
STREAM_HOST_LABEL_KEY      = 'streamHostLabel'
STREAM_PORT_KEY            = 'streamPort'
STREAM_PROTOCOL_KEY        = 'streamProtocol'
STREAM_PATH_KEY            = 'streamPath'
STREAM_ENCODING_KEY        = 'streamEncoding'
STREAM_FRAME_WIDTH_KEY     = 'streamFrameWidth'
STREAM_FRAME_HEIGHT_KEY    = 'streamFrameHeight'
STREAM_FPS_KEY             = 'streamFps'
IMAGE_FILE_EXT_KEY         = 'imageFileExt'
VIDEO_FILE_EXT_KEY         = 'videoFileExt'
MIN_MOTION_PIXELS_DIFF_KEY = 'minMotionPixelsDiff'

IMAGE_ENCODING_KEY         = 'imageEncoding'
IMAGE_DATA_STORE_PATH      = 'imageDataStorePath'
VIDEO_DATA_STORE_PATH      = 'videoDataStorePath'
MIN_MOTION_PIXELS_DIFF_KEY = 'minMotionPixelsDiff'
MAX_MOTION_FRAMES_BEFORE_ACTION_KEY = 'maxMotionFramesBeforeAction'
MAX_CACHED_FRAMES_KEY      = 'maxCachedFrames'
STORE_INTERIM_FRAMES_KEY   = 'storeInterimFrames'
INCLUDE_RAW_IMAGE_DATA_IN_MSG_KEY = 'includeRawImageDataInMsg'
