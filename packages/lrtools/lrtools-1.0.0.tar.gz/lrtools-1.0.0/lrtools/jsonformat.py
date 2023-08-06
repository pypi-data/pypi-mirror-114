from vector_2d import Vector as Vector2d
from .track import *
from .utils import *
import json

def convert_ltype_to_trk(ltype: int) -> int:
	if ltype == 0:
		return LineType.Blue
	if ltype == 1:
		return LineType.Red
	if ltype == 2:
		return LineType.Scenery
	raise ValueError(f"Invalid line type {ltype}")

def load_json(filename, name="track"):
	track = Track()
	track.Name = name
	with open(filename, encoding="utf-8") as f:
		data = json.load(f)
	track.ver = int(data["version"].replace(".", ""))
	track.StartOffset = Vector2d(data["startPosition"]["x"], data["startPosition"]["y"])
	for line in data["lines"]:
		extra = {}
		if "id" in line:
			extra["ID"] = line["id"]
		if "flipped" in line:
			extra["inv"] = line["flipped"]
		if "multiplier" in line:
			extra["Multiplier"] = line["multiplier"]
		# Extension: 0b01 - left   0b10 - right
		if "leftExtended" in line:
			extra["Extension"] = line["rightExtended"] * 2 + line["leftExtended"]
		track.addLine(
			Line(
				convert_ltype_to_trk(line["type"]),
				Vector2d(line["x1"], line["y1"]),
				Vector2d(line["x2"], line["y2"]),
				**extra
			)
		)
	return track