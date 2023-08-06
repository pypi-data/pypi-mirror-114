from struct import *

class BinaryStream:
	def __init__(self, base_stream):
		self.base_stream = base_stream

	def ReadByte(self):
		return self.base_stream.read(1)

	def ReadBytes(self, length):
		return self.base_stream.read(length)

	def ReadChar(self):
		return self.unpack('b')

	def ReadUChar(self):
		return self.unpack('B')

	def ReadBool(self):
		return self.unpack('?')

	def ReadInt16(self):
		return self.unpack('h', 2)

	def ReadUInt16(self):
		return self.unpack('H', 2)

	def ReadInt32(self):
		return self.unpack('i', 4)

	def ReadUInt32(self):
		return self.unpack('I', 4)

	def ReadInt64(self):
		return self.unpack('q', 8)

	def ReadUInt64(self):
		return self.unpack('Q', 8)

	def ReadFloat(self):
		return self.unpack('f', 4)

	def ReadSingle(self):
		return self.unpack('f', 4)

	def ReadDouble(self):
		return self.unpack('d', 8)

	def ReadString(self):
		length = self.ReadUInt16()
		#print(length)
		return self.unpack(str(length) + 's', length)

	def ReadStringSingleByteLength(self):
		length = int.from_bytes(self.ReadByte(), "little")
		print(length)
		return self.unpack(str(length) + 's', length)

	def WriteBytes(self, value):
		self.base_stream.write(value)

	def WriteChar(self, value):
		self.pack('c', value)

	def WriteUChar(self, value):
		self.pack('C', value)

	def WriteBool(self, value):
		self.pack('?', value)

	def WriteUInt8(self, value):
		self.pack('b', value)
	
	def WriteInt16(self, value):
		self.pack('h', value)

	def WriteUInt16(self, value):
		self.pack('H', value)

	def WriteInt32(self, value):
		self.pack('i', value)

	def WriteUInt32(self, value):
		self.pack('I', value)

	def WriteInt64(self, value):
		self.pack('q', value)

	def WriteUInt64(self, value):
		self.pack('Q', value)

	def WriteFloat(self, value):
		self.pack('f', value)

	def WriteDouble(self, value):
		self.pack('d', value)

	def WriteString(self, value):
		length = len(value)
		self.WriteUInt16(length)
		self.pack(str(length) + 's', value)

	def WriteStringSingleByteLength(self, value):
		length = len(value)
		self.WriteUInt8(length)
		self.pack(str(length) + 's', value.encode("utf-8"))
	
	def pack(self, fmt, data):
		return self.WriteBytes(pack(fmt, data))

	def unpack(self, fmt, length = 1):
		return unpack(fmt, self.ReadBytes(length))[0]