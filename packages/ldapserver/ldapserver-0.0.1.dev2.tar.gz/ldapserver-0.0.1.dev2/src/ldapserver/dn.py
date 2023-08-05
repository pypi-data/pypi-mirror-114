from string import hexdigits as HEXDIGITS

from .util import encode_attribute

DN_ESCAPED = ('"', '+', ',', ';', '<', '>')
DN_SPECIAL = DN_ESCAPED + (' ', '#', '=')

def parse_assertion(expr, case_ignore_attrs=None):
	case_ignore_attrs = case_ignore_attrs or []
	hexdigit = None
	escaped = False
	tokens = []
	token = b''
	for c in expr:
		if hexdigit is not None:
			if c not in HEXDIGITS:
				raise ValueError('Invalid hexpair: \\%c%c'%(hexdigit, c))
			token += bytes.fromhex('%c%c'%(hexdigit, c))
			hexdigit = None
		elif escaped:
			escaped = False
			if c in DN_SPECIAL or c == '\\':
				token += c.encode()
			elif c in HEXDIGITS:
				hexdigit = c
			else:
				raise ValueError('Invalid escape: \\%c'%c)
		elif c == '\\':
			escaped = True
		elif c == '=':
			tokens.append(token)
			token = b''
		else:
			token += c.encode()
	tokens.append(token)
	if len(tokens) != 2:
		raise ValueError('Invalid assertion in RDN: "%s"'%expr)
	name = tokens[0].decode().lower()
	value = tokens[1]
	if not name or not value:
		raise ValueError('Invalid assertion in RDN: "%s"'%expr)
	# TODO: handle hex strings
	if name in case_ignore_attrs:
		value = value.lower()
	return (name, value)

def parse_rdn(rdn, case_ignore_attrs=None):
	escaped = False
	assertions = []
	token = ''
	for c in rdn:
		if escaped:
			escaped = False
			token += c
		elif c == '+':
			assertions.append(parse_assertion(token, case_ignore_attrs=case_ignore_attrs))
			token = ''
		else:
			if c == '\\':
				escaped = True
			token += c
	assertions.append(parse_assertion(token, case_ignore_attrs=case_ignore_attrs))
	if not assertions:
		raise ValueError('Invalid RDN "%s"'%rdn)
	return tuple(sorted(assertions))

def parse_dn(dn, case_ignore_attrs=None):
	if not dn:
		return tuple()
	escaped = False
	rdns = []
	rdn = ''
	for c in dn:
		if escaped:
			escaped = False
			rdn += c
		elif c == ',':
			rdns.append(parse_rdn(rdn, case_ignore_attrs=case_ignore_attrs))
			rdn = ''
		else:
			if c == '\\':
				escaped = True
			rdn += c
	rdns.append(parse_rdn(rdn, case_ignore_attrs=case_ignore_attrs))
	return tuple(rdns)

# >>> parse_dn('OU=Sales+CN=J.  Smith,DC=example,DC=net', case_ignore_attrs=['cn', 'ou', 'dc'])
# ((('cn', b'j.  smith'), ('ou', b'sales')), (('dc', b'example'),), (('dc', b'net'),))

def escape_dn_value(value):
	if isinstance(value, int):
		value = str(value)
	if isinstance(value, str):
		value = value.encode()
	res = ''
	for c in value:
		c = bytes((c,))
		try:
			s = c.decode()
		except UnicodeDecodeError:
			s = '\\'+c.hex()
		if s in DN_SPECIAL:
			s = '\\'+s
		res += s
	return res

def build_assertion(assertion):
	name, value = assertion
	return '%s=%s'%(escape_dn_value(name.encode()), escape_dn_value(value))

def build_rdn(assertions):
	return '+'.join(map(build_assertion, assertions))

def build_dn(rdns):
	return ','.join(map(build_rdn, rdns))

class DN(tuple):
	def __new__(cls, *args):
		if len(args) == 1 and isinstance(args[0], str):
			return super().__new__(cls, [RDN(*rdn) for rdn in parse_dn(args[0])])
		elif len(args) == 1 and isinstance(args[0], DN):
			return args[0]
		else:
			return super().__new__(cls, [RDN(rdn) for rdn in args])

	def __repr__(self):
		return '<DN(%s)>'%repr(str(self))

	def __str__(self):
		return build_dn(self)

	def __bytes__(self):
		return str(self).encode()

	def __add__(self, value):
		if isinstance(value, DN):
			return DN(*(tuple(self) + tuple(value)))
		else:
			raise ValueError()

	def __getitem__(self, key):
		if isinstance(key, slice):
			return DN(*super().__getitem__(key))
		return super().__getitem__(key)

	def strip_common_suffix(self, value):
		value = DN(value)
		minlen = min(len(self), len(value))
		for i in range(minlen):
			if self[-1 - i] != value[-1 - i]:
				return self[:-i or None], value[:-i or None]
		return self[:-minlen], value[:-minlen]

	def is_direct_child_of(self, base):
		rchild, rbase = self.strip_common_suffix(DN(base))
		return not rbase and len(rchild) == 1

	def in_subtree_of(self, base):
		rchild, rbase = self.strip_common_suffix(DN(base))
		return not rbase

class RDN(tuple):
	def __new__(cls, *args, **kwargs):
		if not kwargs and len(args) == 1 and isinstance(args[0], str):
			return super().__new__(cls, [RDNAssertion(ava) for ava in parse_rdn(args[0])])
		elif not kwargs and len(args) == 1 and isinstance(args[0], cls):
			return args[0]
		else:
			assertions = []
			for key, value in args + tuple(kwargs.items()):
				assertion = RDNAssertion(key, value)
				if assertion not in assertions:
					assertions.append(assertion)
			assertions.sort()
			return super().__new__(cls, assertions)

	def __repr__(self):
		return '<RDN(%s)>'%repr(str(self))

	def __str__(self):
		return build_rdn(self)

class RDNAssertion(tuple):
	def __new__(cls, *args):
		if len(args) == 1 and isinstance(args[0], RDNAssertion):
			return args[0]
		elif len(args) == 1 and isinstance(args[0], str):
			return super().__new__(cls, parse_assertion(args[0]))
		else:
			key, value = args
			value = encode_attribute(value)
			if not isinstance(key, str):
				raise ValueError('Key in RDN assertion "%s=%s" has invalid type'%(repr(key), repr(value)))
			if not isinstance(value, bytes):
				raise ValueError('Value in RDN assertion "%s=%s" has invalid type'%(key, repr(value)))
			return super().__new__(cls, (key.lower(), value))

	def __repr__(self):
		return '<RDNAssertion(%s)>'%repr(str(self))

	def __str__(self):
		return build_assertion(self)

	@property
	def attribute(self):
		return self[0]

	@property
	def value(self):
		return self[1]
