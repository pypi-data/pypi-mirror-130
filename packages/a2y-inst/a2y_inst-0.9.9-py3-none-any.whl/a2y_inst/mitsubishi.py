import serial as _serial
from a2y_handy import int_2_bool_list, bool_list_2_int
from typing import Union as _Union, List as _List
from a2y_HslCommunication import MelsecMcAsciiNet as _AsciiNet, OperateResult as _OperateResult
from a2y_HslCommunication import MelsecMcNet as _BinaryNet


class FX(_serial.Serial):
	VALID_CHARS = b'0123456789ABCDEF'

	def __init__(self, port, baudrate=9600):
		_serial.Serial.__init__(self, port, baudrate=baudrate, parity=_serial.PARITY_EVEN, bytesize=7, timeout=0.5)

	@staticmethod
	def ToValidChars(value, length=2):
		VCS = FX.VALID_CHARS
		result = bytearray()
		if isinstance(value, int):
			for i in range(length):
				result.append(VCS[value & 0xF])
				value = (value >> 4)
			result.reverse()

		return result

	@staticmethod
	def ToBytes(values):
		values = bytes(values)
		l = len(values)
		i = 0
		result = []
		while i < l:
			D = int(values[i:i+2], 16)
			result.append(D)
			i += 2
		return result

	@staticmethod
	def ToD(values):
		Bytes = FX.ToBytes(values)
		l = len(Bytes)
		i = 0
		result = []
		while i < l:
			value = Bytes[i] + (Bytes[i+1] << 8)
			result.append(value)
			i += 2

		return result

	@staticmethod
	def CalculateCRC(msg, append_etx=True, skip_stx=True):
		crc = 0
		meet_etx = False
		for c in msg:
			c &= 0x7F
			if c != 2 or (not skip_stx):
				crc += c
			if c == 3:
				meet_etx = True
				break
		if (not meet_etx) and append_etx:
			crc += 3
		crc &= 0xFF
		return FX.ToValidChars(crc)

	@staticmethod
	def AddHead(msg):
		msg.insert(0, 2)

	@staticmethod
	def AppendTail(msg):
		msg.append(3)
		crc = FX.CalculateCRC(msg)
		msg.extend(crc)

	@staticmethod
	def MakeMsg(body):
		msg = bytearray(body)
		FX.AddHead(msg)
		FX.AppendTail(msg)
		return msg

	@staticmethod
	def MakeReadBytesMsg(address, count):
		if count > 0x40:
			raise ValueError('Read too much')
		body = bytearray(b'0')
		if isinstance(address, int):
			address = FX.ToValidChars(address, 4)
		elif isinstance(address, str):
			address = address.upper().encode()
		elif isinstance(address, bytes):
			address = address.upper()
		body.extend(address)
		body.extend(FX.ToValidChars(count))
		return FX.MakeMsg(body)

	@staticmethod
	def MakeWriteBytesMsg(address, values, cmd=b'1'):
		count = len(values)
		if count > 0x40:
			raise ValueError('Write too much')
		body = bytearray(cmd)
		if isinstance(address, int):
			address = FX.ToValidChars(address, 4)
		elif isinstance(address, str):
			address = address.upper().encode()
		elif isinstance(address, bytes):
			address = address.upper()
		body.extend(address)
		body.extend(FX.ToValidChars(count))
		for value in values:
			body.extend(FX.ToValidChars(value))
		return FX.MakeMsg(body)

	@staticmethod
	def MakeForceMsg(address, shift, value):
		address = FX.ToValidChars((address+shift), 4)
		mAddress = bytearray(4)
		mAddress[0] = address[2]
		mAddress[1] = address[3]
		mAddress[2] = address[0]
		mAddress[3] = address[1]
		body = bytearray(b'7' if value else b'8')
		body.extend(mAddress)
		return FX.MakeMsg(body)

	@staticmethod
	def MakeSetMMsg(address, value=True):
		if address >= 1024:
			raise ValueError('M address out of range')
		return FX.MakeForceMsg(address, 0x800, value)

	@staticmethod
	def MakeSetYMsg(address, value=True):
		if address >= 0x80:
			raise ValueError('Y address out of range')
		return FX.MakeForceMsg(address, 0x500, value)

	@staticmethod
	def MakeReadDMsg(address, count):
		if count > 0x20:
			raise ValueError('Read too much D')
		if address >= 8256 or (1024 <= address < 8000) or address < 0:
			raise ValueError('D address out of range')
		if address >= 8000:
			shift = 0xE00
			address -= 8000
			if address + count > 256:
				raise ValueError('D last address out of range')
		else:
			shift = 0x1000
			if address + count > 1024:
				raise ValueError('D last address out of range')
		address = shift + address * 2
		count *= 2
		return FX.MakeReadBytesMsg(address, count)

	@staticmethod
	def MakeWriteDMsg(address, values):
		if address >= 512:
			raise ValueError('D address out of range')
		count = len(values)
		if count > 0x20:
			raise ValueError('Read too much D')
		if address + count > 512:
			raise ValueError('D last address out of range')
		address = 0x1000 + address * 2
		Vs = []
		for value in values:
			Vs.append(value & 0xFF)
			Vs.append((value >> 8) & 0xFF)
		return FX.MakeWriteBytesMsg(address, Vs)

	@staticmethod
	def _make_set_multi_coil_uint8_message(address, addr_shift, values):
		return FX.MakeWriteBytesMsg(address + addr_shift, values)

	@staticmethod
	def _make_set_multi_coil_uint16_message(address, addr_shift, values: _Union[list, tuple]):
		address *= 2
		uint8_values = list()
		for value in values:
			uint8_values.append(value & 0xFF)
			uint8_values.append(value >> 8)

		return FX._make_set_multi_coil_uint8_message(address, addr_shift, uint8_values)

	def set_multi_coil_uint8(self, name, values):
		assert name[0] == 'B'
		assert name[1] in 'XYM'
		address = int(name[2:], 8)
		addr_shift = [0x80, 0xA0, 0x100]['XYM'.index(name[1])]
		msg = FX._make_set_multi_coil_uint8_message(address, addr_shift, values)
		self.write(msg)
		self.ReceiveACK()

	def set_multi_coil_uint16(self, name, values: list):
		assert name[0] == 'W'
		assert name[1] in 'XYM'
		address = int(name[2:], 8)
		addr_shift = [0x80, 0xA0, 0x100]['XYM'.index(name[1])]
		msg = FX._make_set_multi_coil_uint16_message(address, addr_shift, values)
		self.write(msg)
		self.ReceiveACK()

	def set_coil_uint8(self, name, value: int):
		self.set_multi_coil_uint8(name, [value])

	def set_coil_uint16(self, name, value: int):
		self.set_multi_coil_uint16(name, [value])

	@staticmethod
	def MakeProgramMsg(address, values):
		Vs = []
		for value in values:
			Vs.append(value & 0xFF)
			Vs.append((value >> 8) & 0xFF)
		return FX.MakeWriteBytesMsg(address*2, Vs, b'P')

	def ReadOne(self):
		data = self.read()
		if len(data) == 0:
			raise IOError('Read FX timeout')
		if isinstance(data, str):
			c = ord(data)
		else:
			c = data[0]
		if c == 0x15:  # NAK
			raise IOError('FX NAK')
		return c

	def Read(self, size):
		data = self.read(size)
		if len(data) != size:
			raise IOError('Read FX timeout')
		msg = bytearray()
		for c in data:
			if isinstance(c, str):
				c = ord(c)
			if c == 0x15: # NACK
				raise IOError('FX NAK')
			msg.append(c)
		return msg

	def Receive(self):
		c = self.ReadOne()
		while c != 2:
			c = self.ReadOne()

		msg = bytearray()
		c = self.ReadOne()
		while c != 3:
			msg.append(c)
			c = self.ReadOne()

		crc = self.Read(2)
		CRC = FX.CalculateCRC(msg)
		if crc != CRC:
			raise IOError('FX CRC error')

		return msg

	def ReceiveACK(self):
		c = self.ReadOne()
		while c != 6:
			c = self.ReadOne()

	def ReadD(self, address, count):
		msg = FX.MakeReadDMsg(address, count)
		self.write(msg)
		feedback = self.Receive()
		result = FX.ToD(feedback)
		return result

	def get_multi_uint16(self, name, count):
		assert name[0] == 'D'
		address = int(name[1:])
		return self.ReadD(address, count)

	def ReadOneD(self, address):
		return self.ReadD(address, 1)[0]

	def ReadUInt32(self, address):
		low, high = self.ReadD(address, 2)
		return (high << 16) | low

	def WriteD(self, address, values):
		msg = FX.MakeWriteDMsg(address, values)
		self.write(msg)
		self.ReceiveACK()

	def set_multi_uint16(self, name, values):
		assert name[0] == 'D'
		address = int(name[1:])
		self.WriteD(address, values)

	def WriteOneD(self, address, value):
		self.WriteD(address, [value])

	def WriteUInt32(self, address, value):
		high = (value >> 16) & 0xFFFF
		low = (value & 0xFFFF)
		return self.WriteD(address, [low, high])

	def Program(self, address, values):
		msg = FX.MakeProgramMsg(address, values)
		self.write(msg)
		self.ReceiveACK()

	def Stop(self):
		msg = FX.MakeMsg(bytearray(b'S'))
		self.write(msg)
		self.ReceiveACK()

	def Run(self):
		msg = FX.MakeMsg(bytearray(b'R'))
		self.write(msg)
		self.ReceiveACK()

	def Erase(self, KBth):
		body = bytearray(b'e')
		body.extend(FX.ToValidChars(KBth))
		msg = FX.MakeMsg(body)
		self.write(msg)
		self.ReceiveACK()

	def ReadM(self, address):
		if address >= 1024:
			raise ValueError('M address out of range')
		major = 0x100 + address // 8
		minor = address % 8
		msg = FX.MakeReadBytesMsg(major, 1)
		self.write(msg)
		feedback = self.Receive()
		value = FX.ToBytes(feedback)[0]
		return (value & (1 << minor)) != 0

	def ReadMGroup(self, group_index):
		if group_index >= 1024 / 8:
			raise ValueError('M Group Index out of range. Only 0~127 are accepted.')
		msg = FX.MakeReadBytesMsg(0x100+group_index, 1)
		self.write(msg)
		feedback = self.Receive()
		values = FX.ToBytes(feedback)[0]
		result = [False]*8
		for i in range(8):
			result[i] = ((values & (1 << i)) != 0)
		return result

	def SetM(self, address):
		msg = FX.MakeSetMMsg(address)
		self.write(msg)
		self.ReceiveACK()

	def ResetM(self, address):
		msg = FX.MakeSetMMsg(address, False)
		self.write(msg)
		self.ReceiveACK()

	def ReadXByte(self, address):
		if address >= (0xA0 - 0x80) // 8:
			raise ValueError('X address out of range')
		major = 0x80 + address * 8
		msg = FX.MakeReadBytesMsg(major, 1)
		self.write(msg)
		feedback = self.Receive()
		value = FX.ToBytes(feedback)[0]
		return value

	def _read_coil_bytes(self, address, count, addr_shift):
		major = addr_shift + address * 8
		msg = FX.MakeReadBytesMsg(major, count)
		self.write(msg)
		feedback = self.Receive()
		values = FX.ToBytes(feedback)
		return values

	def ReadXBytes(self, address, count):
		return self._read_coil_bytes(address, count, 0x80)

	def ReadXByteAsBoolList(self, address):
		value = self.ReadXByte(address)
		return int_2_bool_list(value, 8)

	def _read_coil(self, address, addr_shift):
		major = addr_shift + address // 8
		minor = address % 8
		msg = FX.MakeReadBytesMsg(major, 1)
		self.write(msg)
		feedback = self.Receive()
		value = FX.ToBytes(feedback)[0]
		return (value & (1 << minor)) != 0

	def ReadX(self, address):
		if address >= (0xA0 - 0x80):
			raise ValueError('X address out of range')

		return self._read_coil(address, 0x80)

	def ReadY(self, address):
		if address >= 0xC0 - 0xA0:
			raise ValueError('X address out of range')

		return self._read_coil(address, 0xA0)

	def ReadYBytes(self, address, count):
		return self._read_coil_bytes(address, count, 0xA0)

	def ReadMBytes(self, address, count):
		return self._read_coil_bytes(address, count, 0x100)

	def SetY(self, address):
		msg = FX.MakeSetYMsg(address)
		self.write(msg)
		self.ReceiveACK()

	def ResetY(self, address):
		msg = FX.MakeSetYMsg(address, False)
		self.write(msg)
		self.ReceiveACK()

	def get_coil(self, name):
		address = int(name[1:], 8)
		if name[0] == 'X':
			value = self.ReadX(address)
		elif name[0] == 'Y':
			value = self.ReadY(address)
		elif name[0] == 'M':
			value = self.ReadM(address)
		else:
			raise ValueError('Coil name not supported yet...')
		return value

	def reset_coil(self, name):
		address = int(name[1:], 8)
		if name[0] == 'Y':
			self.ResetY(address)
		elif name[0] == 'M':
			self.ResetM(address)
		else:
			raise ValueError('Coil name not supported yet...')

	def set_coil(self, name: str, value: bool = True):
		if not value:
			self.reset_coil(name)
			return

		address = int(name[1:], 8)
		if name[0] == 'Y':
			self.SetY(address)
		elif name[0] == 'M':
			self.SetM(address)
		else:
			raise ValueError('Coil name not supported yet...')

	def get_multi_coil_uint8(self, name: str, count: int):
		if name[0] != 'B':
			raise ValueError('Not a valid name for coil uint8: %s. It should start with a "B".' % name)

		coil_type = name[1]
		address = int(name[2:], 8)
		if coil_type == 'X':
			result = self.ReadXBytes(address, count)
		elif coil_type == 'Y':
			result = self.ReadYBytes(address, count)
		elif coil_type == 'M':
			result = self.ReadMBytes(address, count)
		else:
			raise ValueError('Coil name not supported yet...')
		return result

	def get_coil_uint8(self, name: str):
		return self.get_multi_coil_uint8(name, 1)[0]

	def get_multi_coil_uint16(self, name: str, count: int):
		if name[0] != 'W':
			raise ValueError('Not a valid name for coil uint16: %s. It should start with a "W"' % name)

		address = int(name[2:], 8) * 2
		name = 'B' + name[1] + oct(address)[2:]
		byte_result = self.get_multi_coil_uint8(name, count*2)
		result = list()
		for i in range(count):
			idx = i * 2
			word = byte_result[idx] + (byte_result[idx+1] << 8)
			result.append(word)

		return result

	def get_coil_uint16(self, name):
		return self.get_multi_coil_uint16(name, 1)[0]


class Qna3EException(Exception):
	def __init__(self, result: _OperateResult):
		desc = f'Error: Qna3E communication failed: Code {result.ErrorCode}, {result.Message}'
		Exception.__init__(self, desc)


class Qna3E:
	"""
		适用于三菱 FX-5U、L、Q 系列 PLC 以太网通信，使用 QNA 3E 协议，二进制或 ASCII 码格式，TCP 连接方式。
	"""
	def __init__(self, host: str, port: int, mode: str = 'binary'):
		"""
		:param host: PLC 的 IP 地址或域名地址（如果有的话）
		:param port: PLC 配置的 TCP 通信端口号。最好是设立一个专门的端口号（信道），不要与触摸屏等其他客户端共用。
		:param mode: 如果传入 'ASCII'（不区分大小写），表示帧格式为 ASCII 码，否则，帧格式为二进制。这必须要与 PLC 设置一致。默认二进制。
		"""
		if mode.lower().startswith('ascii'):
			self.connection = _AsciiNet(ipAddress=host, port=port)
		else:
			self.connection = _BinaryNet(ipAddress=host, port=port)
		self.connection.SetPersistentConnection()

	def get_coil(self, address) -> bool:
		result = self.connection.ReadBool(address, length=1)
		# 如果读取结果成功，result.IsSuccess是True,反之result.IsSuccess是False,
		# result内有3个属性
		# 1.result.IsSuccess显示读取结果
		# 2.result.ErrorCode错误代码
		# 3.result.Message错误信息
		# 4.result.Content返回结果
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content[0]

	def get_coil_uint16(self, address) -> int:
		result = self.connection.ReadBool(address, length=16)
		if not result.IsSuccess:
			raise Qna3EException(result)
		bool_list = result.Content
		value = bool_list_2_int(bool_list)
		return value

	def get_int32(self, name: str):
		result = self.connection.ReadInt32(address=name, length=1)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content[0]

	def get_multi_int32(self, name: str, count: int):
		result = self.connection.ReadInt32(address=name, length=count)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def get_int16(self, address) -> int:
		result = self.connection.ReadInt16(address, length=1)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content[0]

	def get_multi_int16(self, address: str, count: int) -> _List[int]:
		result = self.connection.ReadInt16(address, length=count)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def get_uint16(self, address, length):
		result = self.connection.ReadUInt16(address, length=length)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def get_uint32(self, name: str) -> int:
		result = self.connection.ReadUInt32(name, length=1)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content[0]

	def get_multi_uint32(self, name: str, count: int):
		result = self.connection.ReadUInt32(name, length=count)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def get_uint64(self, address, length):
		result = self.connection.ReadUInt64(address, length=length)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def get_int64(self, address, length):
		result = self.connection.ReadInt64(address, length=length)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def get_float(self, address, length):
		result = self.connection.ReadFloat(address, length=length)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def get_double(self, address, length):
		result = self.connection.ReadDouble(address, length=length)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def get_string(self, address, length):
		result = self.connection.ReadString(address, length=length)
		if not result.IsSuccess:
			raise Qna3EException(result)
		return result.Content

	def set_coil(self, address: str, value: bool):
		result = self.connection.WriteBool(address, value)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_int16(self, address, value):
		result = self.connection.WriteInt16(address, value)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_int32(self, name: str, value: int):
		result = self.connection.WriteInt32(address=name, value=[value])
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_multi_int32(self, name: str, values: _List[int]):
		result = self.connection.WriteInt32(name, values)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_int64(self, address, value):
		result = self.connection.WriteInt64(address, value)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_uint16(self, address, value):
		result = self.connection.WriteUInt16(address, value)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_uint32(self, address: str, value: int):
		result = self.connection.WriteUInt32(address, value)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_multi_uint32(self, address: str, values: _List[int]):
		result = self.connection.WriteUInt32(address, values)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_uint64(self, address, value):
		result = self.connection.WriteUInt64(address, value)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_float(self, address, value):
		result = self.connection.WriteFloat(address, value)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_double(self, address, value):
		result = self.connection.WriteDouble(address, value)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def set_string(self, address, value, length=None):
		result = self.connection.WriteString(address, value, length=length)
		if not result.IsSuccess:
			raise Qna3EException(result)

	def write_UnicodeString(self, address, value, length=None):
		result = self.connection.WriteUnicodeString(address, value, length=length)
		if not result.IsSuccess:
			raise Qna3EException(result)
