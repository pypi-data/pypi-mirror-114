from collections import namedtuple

BERObject = namedtuple('BERObject', ['tag', 'content'])

class IncompleteBERError(ValueError):
	def __init__(self, expected_length=-1):
		super().__init__()
		self.expected_length = expected_length

def decode_ber(data):
	index = 0
	if len(data) < 2:
		raise IncompleteBERError(2)
	identifier = data[index]
	ber_class = identifier >> 6
	ber_constructed = bool(identifier & 0x20)
	ber_type = identifier & 0x1f
	index += 1
	if not data[index] & 0x80:
		length = data[index]
		index += 1
	elif data[index] == 0x80:
		raise ValueError('Indefinite form not implemented')
	elif data[index] == 0xff:
		raise ValueError('BER length invalid')
	else:
		num = data[index] & ~0x80
		index += 1
		if len(data) < index + num:
			raise IncompleteBERError(index + num)
		length = 0
		for octet in data[index:index + num]:
			length = length << 8 | octet
		index += num
	if len(data) < index + length:
		raise IncompleteBERError(index + length)
	ber_content = data[index: index + length]
	rest = data[index + length:]
	return BERObject((ber_class, ber_constructed, ber_type), ber_content), rest

def decode_ber_integer(data):
	if not data:
		return 0
	value = -1 if data[0] & 0x80 else 0
	for octet in data:
		value = value << 8 | octet
	return value

def encode_ber(obj):
	tag = (obj.tag[0] & 0b11) << 6 | (obj.tag[1] & 1) << 5 | (obj.tag[2] & 0b11111)
	length = len(obj.content)
	if length < 127:
		return bytes([tag, length]) + obj.content
	octets = []
	while length:
		octets.append(length & 0xff)
		length = length >> 8
	return bytes([tag, 0x80 | len(octets)]) + bytes(reversed(octets)) + obj.content

def encode_ber_integer(value):
	if value < 0 or value > 255:
		raise NotImplementedError('Encoding of integers greater than 255 is not implemented')
	return bytes([value])

class BERType:
	@classmethod
	def from_ber(cls, data):
		raise NotImplementedError()

	@classmethod
	def to_ber(cls, obj):
		raise NotImplementedError()

	def __bytes__(self):
		return type(self).to_ber(self)

class OctetString(BERType):
	ber_tag = (0, False, 4)

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		if obj.tag != cls.ber_tag:
			raise ValueError('Expected tag %s but found %s'%(cls.ber_tag, obj.tag))
		return obj.content, rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, bytes):
			raise TypeError()
		return encode_ber(BERObject(cls.ber_tag, obj))

class Integer(BERType):
	ber_tag = (0, False, 2)

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		if obj.tag != cls.ber_tag:
			raise ValueError()
		return decode_ber_integer(obj.content), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, int):
			raise TypeError()
		return encode_ber(BERObject(cls.ber_tag, encode_ber_integer(obj)))

class Boolean(BERType):
	ber_tag = (0, False, 1)

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		if obj.tag != cls.ber_tag:
			raise ValueError()
		return bool(decode_ber_integer(obj.content)), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, bool):
			raise TypeError()
		content = b'\xff' if obj else b'\x00'
		return encode_ber(BERObject(cls.ber_tag, content))

class Set(BERType):
	ber_tag = (0, True, 17)
	set_type = OctetString

	@classmethod
	def from_ber(cls, data):
		setobj, rest = decode_ber(data)
		if setobj.tag != cls.ber_tag:
			raise ValueError()
		objs = []
		data = setobj.content
		while data:
			obj, data = cls.set_type.from_ber(data)
			objs.append(obj)
		return list(objs), rest

	@classmethod
	def to_ber(cls, obj):
		content = b''
		for item in obj:
			content += cls.set_type.to_ber(item)
		return encode_ber(BERObject(cls.ber_tag, content))

class SequenceOf(Set):
	ber_tag = (0, True, 16)

class Sequence(BERType):
	ber_tag = (0, True, 16)
	sequence_fields = [
		#(Type, attr_name, default_value, optional?),
	]

	def __init__(self, *args, **kwargs):
		for index, spec in enumerate(type(self).sequence_fields):
			field_type, name, default, optional = spec
			if index < len(args):
				value = args[index]
			elif name in kwargs:
				value = kwargs[name]
			else:
				value = default() if callable(default) else default
			setattr(self, name, value)

	def __repr__(self):
		args = []
		for field_type, name, default, optional in type(self).sequence_fields:
			args.append('%s=%s'%(name, repr(getattr(self, name))))
		return '<%s(%s)>'%(type(self).__name__, ', '.join(args))

	@classmethod
	def from_ber(cls, data):
		seqobj, rest = decode_ber(data)
		if seqobj.tag != cls.ber_tag:
			raise ValueError()
		args = []
		data = seqobj.content
		for field_type, name, default, optional in cls.sequence_fields:
			try:
				obj, data = field_type.from_ber(data)
				args.append(obj)
			except ValueError as e:
				if not optional:
					raise e
				args.append(None)
		return cls(*args), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, cls):
			raise TypeError()
		content = b''
		for field_type, name, default, optional in cls.sequence_fields:
			if not optional or getattr(obj, name) is not None:
				content += field_type.to_ber(getattr(obj, name))
		return encode_ber(BERObject(cls.ber_tag, content))

class Choice(BERType):
	ber_tag = None

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		for subcls in cls.__subclasses__():
			if subcls.ber_tag == obj.tag:
				return subcls.from_ber(data)
		return None, rest

	@classmethod
	def to_ber(cls, obj):
		for subcls in cls.__subclasses__():
			if isinstance(obj, subcls):
				return subcls.to_ber(obj)
		raise TypeError()

class Wrapper(BERType):
	ber_tag = None
	wrapped_attribute = None
	wrapped_type = None
	wrapped_default = None
	wrapped_clsattrs = {}

	def __init__(self, *args, **kwargs):
		cls = type(self)
		attribute = cls.wrapped_attribute
		if args:
			setattr(self, attribute, args[0])
		elif kwargs:
			setattr(self, attribute, kwargs[attribute])
		else:
			setattr(self, attribute, cls.wrapped_default() if callable(cls.wrapped_default) else cls.wrapped_default)

	def __repr__(self):
		return '<%s(%s)>'%(type(self).__name__, repr(getattr(self, type(self).wrapped_attribute)))

	@classmethod
	def from_ber(cls, data):
		class WrappedType(cls.wrapped_type):
			ber_tag = cls.ber_tag
		for key, value in cls.wrapped_clsattrs.items():
			setattr(WrappedType, key, value)
		value, rest = WrappedType.from_ber(data)
		return cls(value), rest

	@classmethod
	def to_ber(cls, obj):
		class WrappedType(cls.wrapped_type):
			ber_tag = cls.ber_tag
		for key, value in cls.wrapped_clsattrs.items():
			setattr(WrappedType, key, value)
		if not isinstance(obj, cls):
			raise TypeError()
		return WrappedType.to_ber(getattr(obj, cls.wrapped_attribute))

def retag(cls, tag):
	class Overwritten(cls):
		ber_tag = tag
	return Overwritten

class Enum(BERType):
	ber_tag = (0, False, 10)
	enum_type = None

	@classmethod
	def from_ber(cls, data):
		obj, rest = decode_ber(data)
		if obj.tag != cls.ber_tag:
			raise ValueError()
		value = decode_ber_integer(obj.content)
		return cls.enum_type(value), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, cls.enum_type):
			raise TypeError()
		return encode_ber(BERObject(cls.ber_tag, encode_ber_integer(obj.value)))

def wrapenum(enumtype):
	class WrappedEnum(Enum):
		enum_type = enumtype
	return WrappedEnum
