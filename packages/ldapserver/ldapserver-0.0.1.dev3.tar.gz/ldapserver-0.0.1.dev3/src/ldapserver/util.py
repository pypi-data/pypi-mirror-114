def encode_attribute(value):
	if isinstance(value, bool):
		value = b'TRUE' if value else b'FALSE'
	if isinstance(value, int):
		value = str(value)
	if isinstance(value, str):
		value = value.encode()
	if not isinstance(value, bytes):
		value = bytes(value)
	return value

class CaseInsensitiveKey(str):
	def __hash__(self):
		return hash(self.lower())

	def __eq__(self, value):
		return self.lower() == value.lower()

class CaseInsensitiveDict(dict):
	def __init__(self, *args, **kwargs):
		if len(args) == 1 and isinstance(args[0], dict):
			kwargs = {CaseInsensitiveKey(k): v for k, v in args[0].items()}
			args = []
		else:
			kwargs = {CaseInsensitiveKey(k): v for k, v in kwargs.items()}
			args = [(CaseInsensitiveKey(k), v) for k, v in args]
		super().__init__(*args, **kwargs)

	def __contains__(self, key):
		return super().__contains__(CaseInsensitiveKey(key))

	def __setitem__(self, key, value):
		super().__setitem__(CaseInsensitiveKey(key), value)

	def __getitem__(self, key):
		return super().__getitem__(CaseInsensitiveKey(key))

	def get(self, key, default=None):
		if key in self:
			return self[key]
		return default

class AttributeDict(CaseInsensitiveDict):
	def __getitem__(self, key):
		if key not in self:
			self[key] = []
		return super().__getitem__(key)

