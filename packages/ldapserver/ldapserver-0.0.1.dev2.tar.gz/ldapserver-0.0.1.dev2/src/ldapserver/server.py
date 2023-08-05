import traceback
import hashlib
import secrets
import socket
import ssl
from socketserver import BaseRequestHandler

from .ldap import *
from .asn1 import IncompleteBERError
from .directory import RootDSE, BaseDirectory
from .exceptions import *

def decode_msg(shallowmsg):
	try:
		return shallowmsg.decode()[0]
	except:
		traceback.print_exc()
		raise LDAPProtocolError()

def reject_critical_controls(controls=None, supported_oids=[]):
	for control in controls or []:
		if not control.criticality:
			continue
		if control.controlType not in supported_oids:
			raise LDAPUnavailableCriticalExtension()

class BaseLDAPRequestHandler(BaseRequestHandler):
	def setup(self):
		super().setup()
		self.keep_running = True

	def handle(self):
		self.on_connect()
		buf = b''
		while self.keep_running:
			try:
				shallowmsg, buf = ShallowLDAPMessage.from_ber(buf)
				for respmsg in self.handle_message(shallowmsg):
					self.request.sendall(LDAPMessage.to_ber(respmsg))
			except IncompleteBERError:
				chunk = self.request.recv(5)
				if not chunk:
					self.keep_running = False
					self.on_disconnect()
					self.request.close()
				else:
					buf += chunk
		self.on_disconnect()
		self.request.close()

	def handle_message(self, shallowmsg):
		'''Handle an LDAP request

		:param shallowmsg: Half-decoded LDAP message to handle
		:type shallowmsg: ShallowLDAPMessage
		:returns: Response messages
		:rtype: iterable of LDAPMessage objects
		'''
		msgtypes = {
			BindRequest: (self.handle_bind, BindResponse),
			UnbindRequest: (self.handle_unbind, None),
			SearchRequest: (self.handle_search, SearchResultDone),
			ModifyRequest: (self.handle_modify, ModifyResponse),
			AddRequest: (self.handle_add,  AddResponse),
			DelRequest: (self.handle_delete, DelResponse),
			ModifyDNRequest: (self.handle_modifydn, ModifyDNResponse),
			CompareRequest: (self.handle_compare, CompareResponse),
			AbandonRequest: (self.handle_abandon, None),
			ExtendedRequest: (self.handle_extended, ExtendedResponse),
		}
		handler, response_type = msgtypes.get(shallowmsg.protocolOpType, (None, None))
		try:
			if handler is None:
				raise LDAPProtocolError()
			try:
				msg = decode_msg(shallowmsg)
			except ValueError:
				self.on_recv_invalid(shallowmsg)
				raise LDAPProtocolError()
			self.on_recv(msg)
			for args in handler(msg.protocolOp, msg.controls):
				response, controls = args if isinstance(args, tuple) else (args, None)
				yield LDAPMessage(shallowmsg.messageID, response, controls)
		except LDAPError as e:
			if response_type is not None:
				respmsg = LDAPMessage(shallowmsg.messageID, response_type(e.code, diagnosticMessage=e.message))
				self.on_send(respmsg)
				yield respmsg
		except Exception as e:
			if response_type is not None:
				respmsg = LDAPMessage(shallowmsg.messageID, response_type(LDAPResultCode.other))
				self.on_send(respmsg)
				yield respmsg
			self.on_exception(e)

	def on_connect(self):
		pass

	def on_disconnect(self):
		pass

	def on_send(self, msg):
		pass

	def on_recv(self, msg):
		pass

	def on_recv_invalid(self, shallowmsg):
		pass

	def on_exception(self, e):
		traceback.print_exc()

	def handle_bind(self, op, controls=None):
		reject_critical_controls(controls)
		raise LDAPAuthMethodNotSupported()

	def handle_unbind(self, op, controls=None):
		reject_critical_controls(controls)
		self.keep_running = False

	def handle_search(self, op, controls=None):
		reject_critical_controls(controls)
		yield SearchResultDone(LDAPResultCode.success)

	def handle_modify(self, op, controls=None):
		reject_critical_controls(controls)
		raise LDAPInsufficientAccessRights()

	def handle_add(self, op, controls=None):
		reject_critical_controls(controls)
		raise LDAPInsufficientAccessRights()

	def handle_delete(self, op, controls=None):
		reject_critical_controls(controls)
		raise LDAPInsufficientAccessRights()

	def handle_modifydn(self, op, controls=None):
		reject_critical_controls(controls)
		raise LDAPInsufficientAccessRights()

	def handle_compare(self, op, controls=None):
		reject_critical_controls(controls)
		raise LDAPInsufficientAccessRights()

	def handle_abandon(self, op, controls=None):
		reject_critical_controls(controls)

	def handle_extended(self, op, controls=None):
		reject_critical_controls(controls)
		raise LDAPProtocolError()

class SimpleLDAPRequestHandler(BaseLDAPRequestHandler):
	'''
	.. py:attribute:: rootdse

		Special single-object :any:`BaseDirectory` that contains information
		about the server, such as supported extentions and SASL authentication
		mechansims. Attributes can be accessed in a dict-like fashion.
	'''

	def setup(self):
		super().setup()
		self.rootdse = RootDSE()
		self.rootdse['objectClass'] = [b'top']
		self.rootdse['supportedSASLMechanisms'] = self.get_sasl_mechanisms
		self.rootdse['supportedExtension'] = self.get_extentions
		self.rootdse['supportedLDAPVersion'] = [b'3']
		self.bind_object = None
		self.bind_sasl_state = None

	def get_extentions(self):
		'''Get supported LDAP extentions

		:returns: OIDs of supported LDAP extentions
		:rtype: list of bytes objects

		Called whenever the root DSE attribute "supportedExtension" is queried.'''
		res = []
		if self.supports_starttls:
			res.append(EXT_STARTTLS_OID.encode())
		if self.supports_whoami:
			res.append(EXT_WHOAMI_OID.encode())
		if self.supports_password_modify:
			res.append(EXT_PASSWORD_MODIFY_OID.encode())
		return res

	def get_sasl_mechanisms(self):
		'''Get supported SASL mechanisms

		:returns: Names of supported SASL mechanisms
		:rtype: list of bytes objects

		SASL mechanism name are typically all-caps, like "EXTERNAL".
		
		Called whenever the root DSE attribute "supportedSASLMechanisms" is queried.'''
		res = []
		if self.supports_sasl_anonymous:
			res.append(b'ANONYMOUS')
		if self.supports_sasl_plain:
			res.append(b'PLAIN')
		if self.supports_sasl_external:
			res.append(b'EXTERNAL')
		return res

	def handle_bind(self, op, controls=None):
		reject_critical_controls(controls)
		if op.version != 3:
			raise LDAPProtocolError('Unsupported protocol version')
		auth = op.authentication
		# Resume ongoing SASL dialog
		if self.bind_sasl_state and isinstance(auth, SaslCredentials) \
				and auth.mechanism == self.bind_sasl_state[0]:
			mechanism, iterator = self.bind_sasl_state
			self.bind_sasl_state = None
			resp_code = LDAPResultCode.saslBindInProgress
			try:
				resp = iterator.send(auth.credentials)
				self.bind_sasl_state = (mechanism, iterator)
			except StopIteration as e:
				resp_code = LDAPResultCode.success
				self.bind_object, resp = e.value
			yield BindResponse(resp_code, serverSaslCreds=resp)
			return
		# If auth type or SASL method changed, abort SASL dialog
		self.bind_sasl_state = None
		if isinstance(auth, SimpleAuthentication):
			self.bind_object = self.do_bind_simple(op.name, auth.password)
			yield BindResponse(LDAPResultCode.success)
		elif isinstance(auth, SaslCredentials):
			ret = self.do_bind_sasl(auth.mechanism, auth.credentials)
			if isinstance(ret, tuple):
				self.bind_object, resp = ret
				yield BindResponse(LDAPResultCode.success, serverSaslCreds=resp)
				return
			iterator = iter(ret)
			resp_code = LDAPResultCode.saslBindInProgress
			try:
				resp = next(iterator)
				self.bind_sasl_state = (auth.mechanism, iterator)
			except StopIteration as e:
				resp_code = LDAPResultCode.success
				self.bind_object, resp = e.value
			yield BindResponse(resp_code, serverSaslCreds=resp)
		else:
			yield from super().handle_bind(op, controls)

	def do_bind_simple(self, dn='', password=b''):
		'''Do LDAP BIND with simple authentication

		:param dn: Distinguished name of object to be authenticated or empty
		:type dn: str
		:param password: Password, may be empty
		:type password: bytes

		:returns: Bind object
		:rtype: obj

		Delegates implementation to :any:`do_bind_simple_anonymous`,
		:any:`do_bind_simple_unauthenticated` or :any:`do_bind_simple_authenticated`
		according to `RFC 4513`_.'''
		if not dn and not password:
			return self.do_bind_simple_anonymous()
		if not password:
			return self.do_bind_simple_unauthenticated(dn)
		return self.do_bind_simple_authenticated(dn, password)

	def do_bind_simple_anonymous(self):
		'''Do LDAP BIND with simple anonymous authentication (`RFC 4513 5.1.1.`_)

		:raises LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_simple`. Always returns None.'''
		return None

	def do_bind_simple_unauthenticated(self, dn):
		'''Do LDAP BIND with simple unauthenticated authentication (`RFC 4513 5.1.2.`_)

		:param dn: Distinguished name of the object to be authenticated
		:type dn: str

		:raises LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_simple`. The default implementation always raises an
		:any:`LDAPInvalidCredentials` exception.'''
		raise LDAPInvalidCredentials()

	def do_bind_simple_authenticated(self, dn, password):
		'''Do LDAP BIND with simple name/password authentication (`RFC 4513 5.1.3.`_)

		:param dn: Distinguished name of the object to be authenticated
		:type dn: str
		:param password: Password for object
		:type dn: bytes

		:raises LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_simple`. The default implementation always raises an
		`LDAPInvalidCredentials` exception.'''
		raise LDAPInvalidCredentials()

	def do_bind_sasl(self, mechanism, credentials=None, dn=None):
		'''Do LDAP BIND with SASL authentication (RFC 4513 and 4422)

		:param mechanism: Name of the selected SASL mechanism
		:type mechanism: str
		:param credentials: Initial client response
		:type credentials: bytes, optional
		:param dn: Distinguished name in LDAP BIND request, should be ignored for
		           SASL authentication
		:type dn: str, optional

		:returns: Bind object and final server challenge, only returns on success
		:rtype: Tuple (obj, bytes/None)

		The call only returns if authentication succeeded. In any other case,
		an appropriate :any:`LDAPError` is raised.

		Some SASL methods require additional challenge-response round trips. These
		can be achieved with the `yield` statement:

		    client_response = yield server_challenge

		Generally all server challenges and client responses can always be absent
		(indicated by None), empty (empty bytes object) or consist of any number
		of bytes. Whether a challenge or response may or must be absent or present
		is defined by the individual SASL mechanism.

		IANA list of SASL mechansims: https://www.iana.org/assignments/sasl-mechanisms/sasl-mechanisms.xhtml
		'''
		if not mechanism:
			# Request to abort current negotiation (RFC4513 5.2.1.2)
			raise LDAPAuthMethodNotSupported()
		if mechanism == 'ANONYMOUS' and self.supports_sasl_anonymous:
			if credentials is not None:
				credentials = credentials.decode()
			return self.do_bind_sasl_anonymous(trace_info=credentials), None
		if mechanism == 'PLAIN' and self.supports_sasl_plain:
			if credentials is None:
				raise LDAPProtocolError('Unsupported protocol version')
			authzid, authcid, password = credentials.split(b'\0', 2)
			return self.do_bind_sasl_plain(authcid.decode(), password.decode(), authzid.decode() or None), None
		if mechanism == 'EXTERNAL' and self.supports_sasl_external:
			if credentials is not None:
				credentials = credentials.decode()
			return self.do_bind_sasl_external(authzid=credentials), None
		raise LDAPAuthMethodNotSupported()

	supports_sasl_anonymous = False

	def do_bind_sasl_anonymous(self, trace_info=None):
		'''Do LDAP BIND with SASL "ANONYMOUS" mechanism (RFC 4505)

		:param trace_info: Trace information, either an email address or an
		                   opaque string that does not contain the '@' character
		:type trace_info: str, optional

		:raises LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_sasl`. The default implementation raises an
		:any:`LDAPAuthMethodNotSupported` exception.'''
		raise LDAPAuthMethodNotSupported()

	supports_sasl_plain = False

	def do_bind_sasl_plain(self, identity, password, authzid=None):
		'''Do LDAP BIND with SASL "PLAIN" mechanism (RFC 4616)

		:param identity: Authentication identity (authcid)
		:type identity: str
		:param password: Password (passwd)
		:type password: str
		:param authzid: Authorization identity
		:type authzid: str, optional

		:raises LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_sasl`. The default implementation raises an
		:any:`LDAPAuthMethodNotSupported` exception.'''
		raise LDAPAuthMethodNotSupported()

	supports_sasl_external = False

	def do_bind_sasl_external(self, authzid=None):
		'''Do LDAP BIND with SASL "EXTERNAL" mechanism (RFC 4422 and 4513)

		:param authzid: Authorization identity
		:type authzid: str, optional

		:raises LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		EXTERNAL is commonly used for TLS client certificate authentication or
		system user based authentication on UNIX sockets.

		Calld by :any:`do_bind_sasl`. The default implementation raises an
		:any:`LDAPAuthMethodNotSupported` exception.'''
		raise LDAPAuthMethodNotSupported()

	def handle_search(self, op, controls=None):
		for dn, attributes in self.do_search(op.baseObject, op.scope, op.filter):
			attributes = [PartialAttribute(name, values) for name, values in attributes.items()]
			yield SearchResultEntry(dn, attributes)
		yield SearchResultDone(LDAPResultCode.success)

	def do_search(self, baseobj, scope, filter):
		'''Do LDAP SEARCH operation

		:param baseobj: Distinguished name of the LDAP entry relative to which the search is
		                to be performed
		:type baseobj: str
		:param scope: Search scope
		:type scope: SearchScope
		:param filter: Filter object
		:type filter: Filter

		:raises LDAPError: on error

		:returns: Iterable of dn, attributes tuples

		The default implementation returns matching objects from the root dse.'''
		return self.rootdse.search(baseobj, scope, filter)

	def handle_unbind(self, op, controls=None):
		reject_critical_controls(controls)
		self.keep_running = False
		return []

	def handle_extended(self, op, controls=None):
		reject_critical_controls(controls)
		if op.requestName == EXT_STARTTLS_OID and self.supports_starttls:
			# StartTLS (RFC 4511)
			yield ExtendedResponse(LDAPResultCode.success, responseName=EXT_STARTTLS_OID)
			try:
				self.do_starttls()
			except Exception as e:
				traceback.print_exc()
				self.keep_running = False
		elif op.requestName == EXT_WHOAMI_OID and self.supports_whoami:
			# "Who am I?" Operation (RFC 4532)
			identity = (self.do_whoami() or '').encode()
			yield ExtendedResponse(LDAPResultCode.success, responseValue=identity)
		elif op.requestName == EXT_PASSWORD_MODIFY_OID and self.supports_password_modify:
			# Password Modify Extended Operation (RFC 3062)
			newpw = None
			if op.requestValue is None:
				newpw = self.do_passwd()
			else:
				decoded, _ = PasswdModifyRequestValue.from_ber(op.requestValue)
				newpw = self.do_passwd(decoded.userIdentity, decoded.oldPasswd, decoded.newPasswd)
			if newpw is None:
				yield ExtendedResponse(LDAPResultCode.success)
			else:
				encoded = PasswdModifyResponseValue.to_ber(PasswdModifyResponseValue(newpw))
				yield ExtendedResponse(LDAPResultCode.success, responseValue=encoded)
		else:
			yield from super().handle_extended(op, controls)

	#: :any:`ssl.SSLContext` for StartTLS
	ssl_context = None

	@property
	def supports_starttls(self):
		'''
		'''
		return self.ssl_context is not None and not isinstance(self.request, ssl.SSLSocket)

	def do_starttls(self):
		'''Do StartTLS extended operation (RFC 4511)

		Called by `handle_extended()` if :any:`supports_starttls` is True. The default
		implementation uses `ssl_context`.

		Note that the (success) response to the request is sent before this method
		is called. If a call to this method fails, the LDAP connection is
		immediately terminated.'''
		self.request = self.ssl_context.wrap_socket(self.request, server_side=True)

	#:
	supports_whoami = False

	def do_whoami(self):
		'''Do "Who am I?" extended operation (RFC 4532)

		:returns: Current authorization identity (authzid) or empty string for anonymous sessions
		:rtype: str

		Called by `handle_extended()` if `supports_whoami` is True. The default
		implementation always returns an empty string.'''
		return ''

	#:
	supports_password_modify = False

	def do_password_modify(self, user=None, old_password=None, new_password=None):
		'''Do password modify extended operation (RFC 3062)
		
		:param user: User the request relates to, may or may not be a
		             distinguished name. If absent, the request relates to the
		             user currently associated with the LDAP connection
		:type user: str, optional
		:param old_password: Current password of user
		:type old_password: bytes, optional
		:param new_password: Desired password for user
		:type new_password: bytes, optional
		
		Called by `handle_extended()` if :any:`supports_password_modify` is True. The
		default implementation always raises an :any:`LDAPUnwillingToPerform` error.'''
		raise LDAPUnwillingToPerform()
