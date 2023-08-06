from vector_2d import Vector as Vector2d
from .utils import *

class Track:
	def __init__(self):
		# For saving call write.SaveTrack(<track>, filename)
		# For loading a track call load.LoadTrack(filename, name)
		# Setting Defualts
		self.YGravity=1
		self.XGravity=0
		self.GravityWellSize=10
		self.BGColorR=244
		self.BGColorG=245
		self.BGColorB=249
		self.LineColorR=0
		self.LineColorG=0
		self.LineColorB=0
		self.lines=[]
		self.Filename=""
		self.Name=""
		self.Remount=False
		self.ZeroStart=False
		self.frictionless=False
		self.ver=62
		self.StartOffset=Vector2d(0.0,0.0)
		self.Triggers=[]
		self.StartZoom=4.0
		self.current_id = 0
		self.Triggers = []
		self.song = ""
		self.song_offset = 0

	def addLine(self, line):
		self.lines.append(line)

class Line:
	def __init__(self, ltype, point1, point2, **kwargs):
		self.type = ltype
		self.point1 = point1
		self.point2 = point2
		if ltype in [LineType.Blue, LineType.Red]:
			self.Extension = kwargs.get("Extension", 0)
			self.inv = kwargs.get("inv", False)
			self.ID = kwargs["ID"]
		if ltype in [LineType.Red]:
			self.Multiplier = kwargs.get("Multiplier", 1)
		if ltype in [LineType.Scenery]:
			self.width = kwargs.get("width", 1)

