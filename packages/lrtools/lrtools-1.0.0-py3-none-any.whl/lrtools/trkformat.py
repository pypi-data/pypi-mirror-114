from .binary import BinaryStream
from vector_2d import Vector as Vector2d
from .track import *
from .utils import *


def ParseFloat(f: str) -> float:
	ret = float(f) # will raise ValueError if not a valid float
	return ret

def ParseDouble(f: str) -> float:
	ret = float(f) # will raise ValueError if not a valid double
	return ret

def ParseInt(f: str) -> int:
	ret = int(f) # will raise ValueError if not a valid int
	return ret

def ReadString(br):
	return br.ReadBytes(br.ReadInt16()).decode("ascii")


def ParseMetadata(ret, br):
	count = br.ReadInt16()
	for i in range(count):
		metadata = ReadString(br).split('=')
		if metadata[0] == TrackMetadata.startzoom:
			#print(metadata[1])
			ret.StartZoom = ParseFloat(metadata[1])
		if metadata[0] == TrackMetadata.ygravity:
			ret.YGravity = ParseFloat(metadata[1])
		if metadata[0] == TrackMetadata.xgravity:
			ret.XGravity = ParseFloat(metadata[1])
		if metadata[0] == TrackMetadata.gravitywellsize:
			ret.GravityWellSize = ParseDouble(metadata[1])
		if metadata[0] == TrackMetadata.bgcolorR:
			ret.BGColorR = ParseInt(metadata[1])
		if metadata[0] == TrackMetadata.bgcolorG:
			ret.BGColorG = ParseInt(metadata[1])
		if metadata[0] == TrackMetadata.bgcolorB:
			ret.BGColorB = ParseInt(metadata[1])
		if metadata[0] == TrackMetadata.linecolorR:
			ret.LineColorR = ParseInt(metadata[1])
		if metadata[0] == TrackMetadata.linecolorG:
			ret.LineColorG = ParseInt(metadata[1])
		if metadata[0] == TrackMetadata.linecolorB:
			ret.LineColorB = ParseInt(metadata[1])
		if metadata[0] == TrackMetadata.triggers:
			triggers = metadata[1].split('&')
			#print(triggers)
			for t in triggers:
				tdata = t.split(':')
				try:
					ttype = ParseInt(tdata[0])
				except:
					raise Exception(
						"Unsupported trigger type")
				#GameTrigger newtrigger
				#int start
				#int end
				if ttype == TriggerType.Zoom:
					target = ParseFloat(tdata[1])
					start = ParseInt(tdata[2])
					end = ParseInt(tdata[3])
					newtrigger = {
						"Start" : start,
						"End" : end,
						"TriggerType" : TriggerType.Zoom,
						"ZoomTarget" : target,
					}
				elif ttype == TriggerType.BGChange:
					red = ParseInt(tdata[1])
					green = ParseInt(tdata[2])
					blue = ParseInt(tdata[3])
					start = ParseInt(tdata[4])
					end = ParseInt(tdata[5])
					newtrigger = {
						"Start" : start,
						"End" : end,
						"TriggerType" : TriggerType.BGChange,
						"backgroundRed" : red,
						"backgroundGreen" : green,
						"backgroundBlue" : blue,
					}
				elif ttype == TriggerType.LineColor:
					linered = ParseInt(tdata[1])
					linegreen = ParseInt(tdata[2])
					lineblue = ParseInt(tdata[3])
					start = ParseInt(tdata[4])
					end = ParseInt(tdata[5])
					newtrigger = {
						"Start" : start,
						"End" : end,
						"TriggerType" : TriggerType.LineColor,
						"lineRed" : linered,
						"lineGreen" : linegreen,
						"lineBlue" : lineblue,
					}
				else:
					raise Exception(
						"Unsupported trigger type")
				ret.Triggers.append(newtrigger)
	return ret

def load_trk(trackfile: str, trackname: str) -> Track:
	linetriggers = []
	addedlines = []
	ret = Track()
	ret.lines = []
	ret.Filename = trackfile
	ret.Name = trackname
	ret.Remount = False
	addedlines = {}
	location = trackfile
	with open(trackfile, "rb") as f:
		File = f
		_bytes = File.read()
		File.seek(0,0)
		#print(str(_bytes))
		br = BinaryStream(File)
		magic = br.ReadBytes(4)
		if magic != b"TRK\xf2":
			raise Exception("File was read as .trk but it is not valid")
		version = int.from_bytes(br.ReadByte(), byteorder)
		#print(_bytes)
		features = list(filter(None, ReadString(br).split(';')))
		if (version != 1):
			raise Exception("Unsupported version")
		redmultipier = False
		scenerywidth = False
		supports61 = False
		songinfo = False
		ignorabletrigger = False
		ret.ZeroStart = False
		ret.Remount = False
		ret.frictionless = False
		ret.song = ""
		ret.song_offset = 0
		for i in range(len(features)):
			if features[i] == TrackFeatures.redmultiplier:
				redmultipier = True
			elif features[i] == TrackFeatures.scenerywidth:
				scenerywidth = True
			elif features[i] == TrackFeatures.six_one:
				supports61 = True
			elif features[i] == TrackFeatures.songinfo:
				songinfo = True
			elif features[i] == TrackFeatures.ignorable_trigger:
				ignorabletrigger = True
			elif features[i] == TrackFeatures.zerostart:
				ret.ZeroStart = True
			elif features[i] == TrackFeatures.remount:
				ret.Remount = True
			elif features[i] == TrackFeatures.frictionless:
				ret.frictionless = True
			else:
				raise Exception("Unsupported feature")
		if (supports61):
			# this is useless to because this isn't actually LRA 
			# so physics doesnt matter
			ret.ver = 61
		else:
			ret.ver = 62

		if (songinfo):
			song = br.ReadStringSingleByteLength()
			try:
				pass
				print("Song found, parsing...")
				strings = song.split(b"\r\n")
				ret.song = strings[0].decode("utf-8")
				ret.song_offset = strings[1].decode("utf-8")
				print(ret.song)
			except:
				pass

		ret.StartOffset = Vector2d(br.ReadDouble(), br.ReadDouble())
		#print(hex(br.base_stream.tell()))
		lines = br.ReadInt32()
		#print("Lines:",lines)
		linetriggers = []
		for i in range(lines):
			#GameLine l
			ltype = int.from_bytes(br.ReadByte(), byteorder)
			lt = ltype & 0x1F
			#print("LineType:",lt)
			inv = (ltype >> 7) != 0
			lim = (ltype >> 5) & 0x3
			ID = -1
			prvID = -1
			nxtID = -1
			multiplier = 1
			linewidth = 1.0
			tr = None
			if (redmultipier):
				if (lt == LineType.Red):
					multiplier = int.from_bytes(br.ReadByte(), byteorder)
			if (lt == LineType.Blue or lt == LineType.Red):
				if (ignorabletrigger):
					# Read trigger and store as dictionary
					tr = {}
					zoomtrigger = br.ReadBoolean()
					if (zoomtrigger):
						tr["ZoomTrigger"] = True
						target = br.ReadSingle()
						frames = br.ReadInt16()
						tr["ZoomFrames"] = frames
						tr["ZoomTarget"] = target
					else:
						tr = None
				ID = br.ReadInt32()
				if ID > ret.current_id:
					ret.current_id = ID
				#print("ID:",ID)
				if (lim != 0):
					prvID = br.ReadInt32();# ignored
					nxtID = br.ReadInt32();# ignored
			if (lt == LineType.Scenery):
				if (scenerywidth):
					b = int.from_bytes(br.ReadByte(), byteorder)
					linewidth = b / 10.0
			x1 = br.ReadDouble()
			y1 = br.ReadDouble()
			x2 = br.ReadDouble()
			y2 = br.ReadDouble()
			#print(x1,y1,x2,y2)
			if (tr != None):
				tr["LineID"] = ID
				linetriggers.append(tr)
			if lt == LineType.Blue:
				ret.addLine(Line(lt, Vector2d(x1, y1), Vector2d(x2, y2), ID=ID, inv=inv, Extension=lim))
			elif lt == LineType.Red:
				if (redmultipier):
					ml = multiplier
				else:
					ml = 0
				ret.addLine(Line(lt, Vector2d(x1, y1), Vector2d(x2, y2), ID=ID, inv=inv, Extension=lim, Multiplier=ml))
			elif lt == LineType.Scenery:
				ret.addLine(Line(lt, Vector2d(x1, y1), Vector2d(x2, y2), width=linewidth))
			else:
				raise Exception(f"Invalid line type {lt} at line ID {ID}")
			#if (l["type"] == "StandardLine"):
				#if (l["ID"] not in list(addedlines.keys())):
				#addedlines[ID] = l
				#ret.lines.append(l)
			#else:
				#pass
				#ret.lines.append(l)
			#print(l)

		ret.Triggers = linetriggers
		if (br.base_stream.tell() != len(_bytes)):
			meta = br.ReadBytes(4)
			#print(meta)
			if (meta == b"META"):
				ret = ParseMetadata(ret, br)
			else:
				raise Exception("Expected metadata tag but got " + str(meta))
		return ret


def GetTrackFeatures(trk):
	ret = {}
	for el in vars(TrackFeatures).values():
		ret[el] = False
	if (trk.ZeroStart):
		ret[TrackFeatures.zerostart] = True
	if (trk.frictionless):
		ret[TrackFeatures.frictionless] = True
	for l in trk.lines:
		if (l.type == LineType.Scenery):
			if (abs(l.width - 1) > 0.0001):
				ret[TrackFeatures.scenerywidth] = True
		if (l.type == LineType.Red):
			if (l.Multiplier != 1):
				ret[TrackFeatures.redmultiplier] = True
		if (l.type == LineType.Blue):
			pass
			#if (l.Trigger != None)
			#	ret[TrackFeatures.ignorable_trigger] = true
	if (trk.ver == 61):
		ret[TrackFeatures.six_one] = True
	if (trk.Remount):
		ret[TrackFeatures.remount] = True
	if (trk.song):
		ret[TrackFeatures.songinfo] = True
	
	return ret



def save_trk(trk: Track, savename: str):
	directory = ""
	filename = directory + savename
	with open(filename, "wb") as f:
		bw = BinaryStream(f)
		bw.WriteBytes(b"TRK\xf2")
		bw.WriteBytes(bytes([1]))
		featurestring = ""
		lines = trk.lines
		featurelist = GetTrackFeatures(trk)
		songinfo = featurelist[TrackFeatures.songinfo]
		redmultiplier = featurelist[TrackFeatures.redmultiplier]
		zerostart = featurelist[TrackFeatures.zerostart]
		scenerywidth = featurelist[TrackFeatures.scenerywidth]
		six_one = featurelist[TrackFeatures.six_one]
		ignorable_trigger = featurelist[TrackFeatures.ignorable_trigger]
		remount = featurelist[TrackFeatures.remount]
		frictionless = featurelist[TrackFeatures.frictionless]
		featurestring = ""
		#print(featurelist)
		for feature in featurelist.items():
			#print(feature)
			if (feature[1]):
				#print(feature)
				featurestring += feature[0] + ";"
		#print(featurestring)
		WriteString(bw, featurestring)
		if (songinfo):
			bw.WriteStringSingleByteLength(trk.song + "\r\n" + str(trk.song_offset))
			# Don't write song info
			pass
		bw.WriteDouble(trk.StartOffset.x)
		bw.WriteDouble(trk.StartOffset.y)
		bw.WriteInt32(len(lines))
		for line in lines:
			#print(line)
			l = line
			type_ = line.type
			if (l.type == LineType.Blue or l.type == LineType.Red):
				if (l.inv):
					type_ |= 1 << 7
				ext = l.Extension
				type_ |= ((ext & 0x03) << 5); #bits: 2
				bw.WriteBytes(bytes([type_]))
				if (redmultiplier):
					if (l.type == LineType.Red):
						bw.WriteBytes(bytes([l.Multiplier]))
				if (ignorable_trigger):
					pass
					''' not required
					if (l.Trigger != null)
						if (l.Trigger.ZoomTrigger) # check other triggers here for at least one
						{
							bw.Write(l.Trigger.ZoomTrigger)
							if (l.Trigger.ZoomTrigger)
								bw.Write(l.Trigger.ZoomTarget)
								bw.Write((short)l.Trigger.ZoomFrames)
						else
							bw.Write(false)
					else
						bw.Write(false);#zoomtrigger=false
					'''
				bw.WriteInt32(l.ID)
				if (l.Extension != 0):
					# this was extension writing
					# but we no longer support this.
					bw.WriteBytes(b'\xff\xff\xff\xff')
					bw.WriteBytes(b'\xff\xff\xff\xff')
			else:
				bw.WriteBytes(bytes([type_]))
				if (scenerywidth):
					if (l.type == LineType.Scenery):
						b = bytes([int((round(l.width, 1) * 10))])
						bw.WriteBytes(b)
			bw.WriteDouble(line.point1.x)
			bw.WriteDouble(line.point1.y)
			bw.WriteDouble(line.point2.x)
			bw.WriteDouble(line.point2.y)
		bw.WriteBytes(b'META')
		
		metadata = []
		metadata.append(TrackMetadata.startzoom + "=" + str(int(trk.StartZoom)))
		#Only add if the values are different from default
		if (trk.YGravity != 1):
			metadata.append(TrackMetadata.ygravity + "=" + str(int(trk.YGravity)))
		if (trk.XGravity != 0):
			metadata.append(TrackMetadata.xgravity + "=" + str(int(trk.XGravity)))
		if (trk.GravityWellSize != 10):
			metadata.append(TrackMetadata.gravitywellsize + "=" + str(int(trk.GravityWellSize)))
		
		if (trk.BGColorR != 244):
			metadata.append(TrackMetadata.bgcolorR + "=" + str(int(trk.BGColorR)))
		if (trk.BGColorG != 245):
			metadata.append(TrackMetadata.bgcolorG + "=" + str(int(trk.BGColorG)))
		if (trk.BGColorB != 249):
			metadata.append(TrackMetadata.bgcolorB + "=" + str(int(trk.BGColorB)))
		
		if (trk.LineColorR != 0):
			metadata.append(TrackMetadata.linecolorR + "=" + str(int(trk.LineColorR)))
		if (trk.LineColorG != 0):
			metadata.append(TrackMetadata.linecolorG + "=" + str(int(trk.LineColorG)))
		if (trk.LineColorB != 0):
			metadata.append(TrackMetadata.linecolorB + "=" + str(int(trk.LineColorB)))
		triggerstring = ""
		for i in range(len(trk.Triggers)):
			t = trk.Triggers[i]
			if (i != 0): triggerstring += "&"
			
			if t["TriggerType"] == TriggerType.Zoom:
				triggerstring += str(TriggerType.Zoom)
				triggerstring += ":"
				triggerstring += str(t["ZoomTarget"])
				triggerstring += ":"
			if t["TriggerType"] == TriggerType.BGChange:
				triggerstring += str(TriggerType.BGChange)
				triggerstring += ":"
				triggerstring += str(t["backgroundRed"])
				triggerstring += ":"
				triggerstring += str(t["backgroundGreen"])
				triggerstring += ":"
				triggerstring += str(t["backgroundBlue"])
				triggerstring += ":"
			if t["TriggerType"] == TriggerType.LineColor:
				triggerstring += str(TriggerType.LineColor)
				triggerstring += ":"
				triggerstring += str(t["lineRed"])
				triggerstring += ":"
				triggerstring += str(t["lineGreen"])
				triggerstring += ":"
				triggerstring += str(t["lineBlue"])
				triggerstring += ":"
			triggerstring += str(t["Start"])
			triggerstring += ":"
			triggerstring += str(t["End"])
		if (len(trk.Triggers) > 0): # If here are not trigger don't add triggers entry
			metadata.append(TrackMetadata.triggers + "=" + str(triggerstring))
		
		bw.WriteInt16(len(metadata))
		for string in metadata:
			WriteString(bw, string)
		return filename



def WriteString(bw, string):
	#bw.WriteBytes(len(string).to_bytes((len(string).bit_length()), 'little'))
	bw.WriteUInt16(len(string))
	bw.WriteBytes(str.encode(string, "ascii"))