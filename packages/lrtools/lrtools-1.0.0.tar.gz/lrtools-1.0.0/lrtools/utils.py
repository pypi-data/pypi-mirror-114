from enum import Enum
from .binary import *
byteorder = "little"

class TrackFeatures:
	redmultiplier = "REDMULTIPLIER"
	scenerywidth = "SCENERYWIDTH"
	six_one = "6.1"
	songinfo = "SONGINFO"
	ignorable_trigger = "IGNORABLE_TRIGGER"
	zerostart = "ZEROSTART"
	remount = "REMOUNT"
	frictionless = "FRICTIONLESS"

class LineType:
	Scenery = 0
	Blue = 1
	Red = 2

class TrackMetadata:
	startzoom = "STARTZOOM"
	ygravity = "YGRAVITY"
	xgravity = "XGRAVITY"
	gravitywellsize = "GRAVITYWELLSIZE"
	bgcolorR = "BGCOLORR"
	bgcolorG = "BGCOLORG"
	bgcolorB = "BGCOLORB"
	linecolorR = "LINECOLORR"
	linecolorG = "LINECOLORG"
	linecolorB = "LINECOLORB"
	triggers = "TRIGGERS"

class TriggerType:
	Zoom = 0
	BGChange = 1
	LineColor = 2

class TrackType(Enum):
	LRA_JSON = 0
	MODERN_JSON = 1
	LRA_TRK = 2
	LRACE_TRK = 3


# TRK utils
supported_features = [
	"REDMULTIPLIER",
	"SCENERYWIDTH",
	"6.1",
	"SONGINFO",
	"IGNORABLE_TRIGGER",
	"ZEROSTART",
]
	
REDMULTIPLIER_INDEX = 0
SCENERYWIDTH_INDEX = 1
SIX_ONE_INDEX = 2
SONGINFO_INDEX = 3
IGNORABLE_TRIGGER_INDEX = 4
ZEROSTART_INDEX = 5