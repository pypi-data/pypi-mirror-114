# Enums/constants/attributes are mostly named after RFCs
# pylint: disable=invalid-name
import enum

from . import asn1

class LDAPString(asn1.OctetString):
	@classmethod
	def from_ber(cls, data):
		raw, rest = super().from_ber(data)
		return raw.decode(), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, str):
			raise TypeError()
		return super().to_ber(obj.encode())

class LDAPOID(LDAPString):
	pass

class AttributeValueAssertion(asn1.Sequence):
	sequence_fields = [
		(LDAPString, 'attributeDesc', None, False),
		(asn1.OctetString, 'assertionValue', None, False),
	]

def escape_filter_assertionvalue(s):
	allowed_bytes = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'+,-./:;<=>?@[\\]^_`{|}~ '
	res = []
	for byte in s:
		if byte not in allowed_bytes:
			res += b'\\%02X'%byte
		else:
			res.append(byte)
	return bytes(res).decode()

class Filter(asn1.Choice):
	'''Base class for filters in SEARCH operations'''

	def get_filter_string(self):
		raise NotImplementedError()

class FilterAnd(asn1.Wrapper, Filter):
	'''AND conjunction of multiple filters ``(&filters...)``

	.. py:attribute:: filters
		:type: list
		:value: []

		List of :any:`Filter` objects
	'''
	ber_tag = (2, True, 0)
	wrapped_attribute = 'filters'
	wrapped_type = asn1.Set
	wrapped_clsattrs = {'set_type': Filter}

	def __init__(self, filters=None):
		super().__init__(filters=filters)

	def get_filter_string(self):
		return '(&%s)'%(''.join([subfilter.get_filter_string() for subfilter in self.filters]))

class FilterOr(asn1.Wrapper, Filter):
	'''OR conjunction of multiple filters ``(|filters...)``

	.. py:attribute:: filters
		:type: list
		:value: []

		List of :any:`Filter` objects
	'''
	ber_tag = (2, True, 1)
	wrapped_attribute = 'filters'
	wrapped_type = asn1.Set
	wrapped_clsattrs = {'set_type': Filter}

	def __init__(self, filters=None):
		super().__init__(filters=filters)

	def get_filter_string(self):
		return '(|%s)'%(''.join([subfilter.get_filter_string() for subfilter in self.filters]))

class FilterNot(asn1.Sequence, Filter):
	'''Negation of a filter ``(!filter)``

	.. py:attribute:: filter
		:type: Filter
	'''

	ber_tag = (2, True, 2)
	sequence_fields = [
		(Filter, 'filter', None, False)
	]

	def __init__(self, filter=None):
		super().__init__(filter=filter)

	def get_filter_string(self):
		return '(!%s)'%self.filter.get_filter_string()

class FilterEqual(asn1.Sequence, Filter):
	'''Attribute equal filter ``(attribute=value)``

	.. py:attribute:: attribute
		:type: str
	.. py:attribute:: value
		:type: bytes
	'''
	ber_tag = (2, True, 3)
	sequence_fields = [
		(LDAPString, 'attribute', None, False),
		(asn1.OctetString, 'value', None, False)
	]

	def __init__(self, attribute=None, value=None):
		super().__init__(attribute=attribute, value=value)

	def get_filter_string(self):
		return '(%s=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class FilterGreaterOrEqual(AttributeValueAssertion, Filter):
	ber_tag = (2, True, 5)

	def get_filter_string(self):
		return '(%s>=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class FilterLessOrEqual(AttributeValueAssertion, Filter):
	ber_tag = (2, True, 6)

	def get_filter_string(self):
		return '(%s<=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class FilterPresent(asn1.Wrapper, Filter):
	'''Attribute present filter ``(attribute=*)``

	.. py:attribute:: attribute
		:type: str
	'''
	ber_tag = (2, False, 7)
	wrapped_attribute = 'attribute'
	wrapped_type = LDAPString
	wrapped_default = None

	def __init__(self, attribute=None):
		super().__init__(attribute=attribute)

	def get_filter_string(self):
		return '(%s=*)'%(self.attribute)

class FilterApproxMatch(AttributeValueAssertion, Filter):
	ber_tag = (2, True, 8)

	def get_filter_string(self):
		return '(%s~=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class FilterExtensibleMatch(asn1.Sequence, Filter):
	ber_tag = (2, True, 9)
	sequence_fields = [
		(asn1.retag(LDAPString, (2, False, 1)), 'matchingRule', None, True),
		(asn1.retag(LDAPString, (2, False, 2)), 'type', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 3)), 'matchValue', None, False),
		(asn1.retag(asn1.Boolean, (2, False, 4)), 'dnAttributes', None, True),
	]

	def get_filter_string(self):
		return '(%s:=%s)'%(self.attribute, escape_filter_assertionvalue(self.value))

class SearchScope(enum.Enum):
	''':any:`enum.Enum` of `scope` values in SEARCH operations'''
	#: Search is constrained to the base object
	baseObject = 0
	#: Search is constrained to the immediate subordinates of the base object
	singleLevel = 1
	#: Search is constrained to the base object and to all its subordinates
	wholeSubtree = 2

class DerefAliases(enum.Enum):
	neverDerefAliases = 0
	derefInSearching = 1
	derefFindingBaseObj = 2
	derefAlways = 3

class LDAPResultCode(enum.Enum):
	success                      = 0
	operationsError              = 1
	protocolError                = 2
	timeLimitExceeded            = 3
	sizeLimitExceeded            = 4
	compareFalse                 = 5
	compareTrue                  = 6
	authMethodNotSupported       = 7
	strongerAuthRequired         = 8
	# -- 9 reserved --
	referral                     = 10
	adminLimitExceeded           = 11
	unavailableCriticalExtension = 12
	confidentialityRequired      = 13
	saslBindInProgress           = 14
	noSuchAttribute              = 16
	undefinedAttributeType       = 17
	inappropriateMatching        = 18
	constraintViolation          = 19
	attributeOrValueExists       = 20
	invalidAttributeSyntax       = 21
	# -- 22-31 unused --
	noSuchObject                 = 32
	aliasProblem                 = 33
	invalidDNSyntax              = 34
	# -- 35 reserved for undefined isLeaf --
	aliasDereferencingProblem    = 36
	# -- 37-47 unused --
	inappropriateAuthentication  = 48
	invalidCredentials           = 49
	insufficientAccessRights     = 50
	busy                         = 51
	unavailable                  = 52
	unwillingToPerform           = 53
	loopDetect                   = 54
	# -- 55-63 unused --
	namingViolation              = 64
	objectClassViolation         = 65
	notAllowedOnNonLeaf          = 66
	notAllowedOnRDN              = 67
	entryAlreadyExists           = 68
	objectClassModsProhibited    = 69
	# -- 70 reserved for CLDAP --
	affectsMultipleDSAs          = 71
	# -- 72-79 unused --
	other                        = 80

class LDAPResult(asn1.Sequence):
	ber_tag = (5, True, 1)
	sequence_fields = [
		(asn1.wrapenum(LDAPResultCode), 'resultCode', None, False),
		(LDAPString, 'matchedDN', '', False),
		(LDAPString, 'diagnosticMessage', '', False),
	]

class AttributeSelection(asn1.SequenceOf):
	set_type = LDAPString

class AuthenticationChoice(asn1.Choice):
	pass

class SimpleAuthentication(asn1.Wrapper, AuthenticationChoice):
	ber_tag = (2, False, 0)
	wrapped_attribute = 'password'
	wrapped_type = asn1.OctetString
	wrapped_default = b''

	def __repr__(self):
		if not self.password:
			return '<%s(EMPTY PASSWORD)>'%(type(self).__name__)
		return '<%s(PASSWORD HIDDEN)>'%(type(self).__name__)

class SaslCredentials(asn1.Sequence, AuthenticationChoice):
	ber_tag = (2, True, 3)
	sequence_fields = [
		(LDAPString, 'mechanism', None, False),
		(asn1.OctetString, 'credentials', None, True),
	]

class AttributeValueSet(asn1.Set):
	set_type = asn1.OctetString

class PartialAttribute(asn1.Sequence):
	sequence_fields = [
		(LDAPString, 'type', None, False),
		(AttributeValueSet, 'vals', lambda: [], False),
	]

class PartialAttributeList(asn1.SequenceOf):
	set_type = PartialAttribute

class Attribute(asn1.Sequence):
	# Constrain: vals must not be empty
	sequence_fields = [
		(LDAPString, 'type', None, False),
		(AttributeValueSet, 'vals', lambda: [], False),
	]

class AttributeList(asn1.SequenceOf):
	set_type = Attribute

class ProtocolOp(asn1.Choice):
	pass

class BindRequest(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 0)
	sequence_fields = [
		(asn1.Integer, 'version', 3, False),
		(LDAPString, 'name', '', False),
		(AuthenticationChoice, 'authentication', lambda: SimpleAuthentication(), False)
	]

class BindResponse(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 1)
	sequence_fields = [
		(asn1.wrapenum(LDAPResultCode), 'resultCode', None, False),
		(LDAPString, 'matchedDN', '', False),
		(LDAPString, 'diagnosticMessage', '', False),
		(asn1.retag(asn1.OctetString, (2, False, 7)), 'serverSaslCreds', None, True)
	]

class UnbindRequest(asn1.Sequence, ProtocolOp):
	ber_tag = (1, False, 2)

class SearchRequest(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 3)
	sequence_fields = [
		(LDAPString, 'baseObject', '', False),
		(asn1.wrapenum(SearchScope), 'scope', SearchScope.wholeSubtree, False),
		(asn1.wrapenum(DerefAliases), 'derefAliases', DerefAliases.neverDerefAliases, False),
		(asn1.Integer, 'sizeLimit', 0, False),
		(asn1.Integer, 'timeLimit', 0, False),
		(asn1.Boolean, 'typesOnly', False, False),
		(Filter, 'filter', lambda: FilterPresent('objectClass'), False),
		(AttributeSelection, 'attributes', lambda: [], False)
	]

	@classmethod
	def from_ber(cls, data):
		return super().from_ber(data)

class SearchResultEntry(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 4)
	sequence_fields = [
		(LDAPString, 'objectName', '', False),
		(PartialAttributeList, 'attributes', lambda: [], False),
	]

class SearchResultDone(LDAPResult, ProtocolOp):
	ber_tag = (1, True, 5)

class ModifyOperation(enum.Enum):
	add = 0
	delete = 1
	replace = 2

class ModifyChange(asn1.Sequence):
	sequence_fields = [
		(asn1.wrapenum(ModifyOperation), 'operation', None, False),
		(PartialAttribute, 'modification', None, False),
	]

class ModifyChanges(asn1.SequenceOf):
	set_type = ModifyChange

class ModifyRequest(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 6)
	sequence_fields = [
		(LDAPString, 'object', None, False),
		(ModifyChanges, 'changes', None, False),
	]

class ModifyResponse(LDAPResult, ProtocolOp):
	ber_tag = (1, True, 7)

class AddRequest(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 8)
	sequence_fields = [
		(LDAPString, 'entry', None, False),
		(AttributeList, 'attributes', None, False),
	]

class AddResponse(LDAPResult, ProtocolOp):
	ber_tag = (1, True, 9)

class DelRequest(asn1.Wrapper, ProtocolOp):
	ber_tag = (1, False, 10)
	wrapped_attribute = 'dn'
	wrapped_type = LDAPString
	wrapped_default = None

class DelResponse(LDAPResult, ProtocolOp):
	ber_tag = (1, True, 11)

class ModifyDNRequest(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 12)
	sequence_fields = [
		(LDAPString, 'entry', None, False),
		(LDAPString, 'newrdn', None, False),
		(asn1.Boolean, 'deleteoldrdn', None, False),
		(asn1.retag(LDAPString, (2, False, 0)), 'newSuperior', None, True),
	]

class ModifyDNResponse(LDAPResult, ProtocolOp):
	ber_tag = (1, True, 13)

class CompareRequest(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 14)
	sequence_fields = [
		(LDAPString, 'entry', None, False),
		(AttributeValueAssertion, 'ava', None, False),
	]

class CompareResponse(LDAPResult, ProtocolOp):
	ber_tag = (1, True, 15)

class AbandonRequest(asn1.Wrapper, ProtocolOp):
	ber_tag = (1, False, 16)
	wrapped_attribute = 'messageID'
	wrapped_type = asn1.Integer
	wrapped_default = None

class ExtendedRequest(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 23)
	sequence_fields = [
		(asn1.retag(LDAPOID, (2, False, 0)), 'requestName', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 1)), 'requestValue', None, True),
	]

class ExtendedResponse(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 24)
	sequence_fields = [
		(asn1.wrapenum(LDAPResultCode), 'resultCode', None, False),
		(LDAPString, 'matchedDN', '', False),
		(LDAPString, 'diagnosticMessage', '', False),
		(asn1.retag(LDAPOID, (2, False, 10)), 'responseName', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 11)), 'responseValue', None, True),
	]

class IntermediateResponse(asn1.Sequence, ProtocolOp):
	ber_tag = (1, True, 25)
	sequence_fields = [
		(asn1.retag(LDAPOID, (2, False, 0)), 'responseName', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 1)), 'responseValue', None, True),
	]

class Control(asn1.Sequence):
	sequence_fields = [
		(LDAPOID, 'controlType', None, False),
		(asn1.Boolean, 'criticality', None, True),
		(asn1.OctetString, 'controlValue', None, True),
	]

class Controls(asn1.SequenceOf):
	ber_tag = (2, True, 0)
	set_type = Control

class LDAPMessage(asn1.Sequence):
	sequence_fields = [
		(asn1.Integer, 'messageID', None, False),
		(ProtocolOp, 'protocolOp', None, False),
		(Controls, 'controls', None, True)
	]

class ShallowLDAPMessage(asn1.BERType):
	ber_tag = (0, True, 16)

	def __init__(self, messageID=None, protocolOpType=None, data=None):
		self.messageID = messageID
		self.protocolOpType = protocolOpType
		self.data = data

	def decode(self):
		return LDAPMessage.from_ber(self.data)

	@classmethod
	def from_ber(cls, data):
		seq, rest = asn1.decode_ber(data)
		data = data[:len(data)-len(rest)]
		if seq.tag != cls.ber_tag:
			raise ValueError()
		content = seq.content
		messageID, content = asn1.Integer.from_ber(content)
		op, content = asn1.decode_ber(content)
		for subcls in ProtocolOp.__subclasses__():
			if subcls.ber_tag == op.tag:
				return cls(messageID, subcls, data), rest
		return cls(messageID, None, data), rest

	@classmethod
	def to_ber(cls, obj):
		if not isinstance(obj, cls):
			raise TypeError()
		return obj.data

# Extended Operation Values

EXT_STARTTLS_OID = '1.3.6.1.4.1.1466.20037'
EXT_WHOAMI_OID = '1.3.6.1.4.1.4203.1.11.3'
EXT_PASSWORD_MODIFY_OID = '1.3.6.1.4.1.4203.1.11.1'

class PasswdModifyRequestValue(asn1.Sequence):
	sequence_fields = [
		(asn1.retag(LDAPString, (2, False, 0)), 'userIdentity', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 1)), 'oldPasswd', None, True),
		(asn1.retag(asn1.OctetString, (2, False, 2)), 'newPasswd', None, True),
	]

class PasswdModifyResponseValue(asn1.Sequence):
	sequence_fields = [
		(asn1.retag(asn1.OctetString, (2, False, 0)), 'genPasswd', None, True),
	]
