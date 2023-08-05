from .ldap import LDAPResultCode

class LDAPError(Exception):
	'''Base class for all LDAP errors'''

	result_code = None

	def __init__(self, message=''):
		self.code = self.result_code
		self.message = message

#class LDAPSuccess(LDAPError):
#	result_code = LDAPResultCode.success

class LDAPOperationsError(LDAPError):
	result_code = LDAPResultCode.operationsError

class LDAPProtocolError(LDAPError):
	result_code = LDAPResultCode.protocolError

class LDAPTimeLimitExceeded(LDAPError):
	result_code = LDAPResultCode.timeLimitExceeded

class LDAPSizeLimitExceeded(LDAPError):
	result_code = LDAPResultCode.sizeLimitExceeded

#class LDAPCompareFalse(LDAPError):
#	result_code = LDAPResultCode.compareFalse

#class LDAPCompareTrue(LDAPError):
#	result_code = LDAPResultCode.compareTrue

class LDAPAuthMethodNotSupported(LDAPError):
	result_code = LDAPResultCode.authMethodNotSupported

class LDAPStrongerAuthRequired(LDAPError):
	result_code = LDAPResultCode.strongerAuthRequired

#class LDAPReferral(LDAPError):
#	result_code = LDAPResultCode.referral

class LDAPAdminLimitExceeded(LDAPError):
	result_code = LDAPResultCode.adminLimitExceeded

class LDAPUnavailableCriticalExtension(LDAPError):
	result_code = LDAPResultCode.unavailableCriticalExtension

class LDAPConfidentialityRequired(LDAPError):
	result_code = LDAPResultCode.confidentialityRequired

#class LDAPSaslBindInProgress(LDAPError):
#	result_code = LDAPResultCode.saslBindInProgress

class LDAPNoSuchAttribute(LDAPError):
	result_code = LDAPResultCode.noSuchAttribute

class LDAPUndefinedAttributeType(LDAPError):
	result_code = LDAPResultCode.undefinedAttributeType

class LDAPInappropriateMatching(LDAPError):
	result_code = LDAPResultCode.inappropriateMatching

class LDAPConstraintViolation(LDAPError):
	result_code = LDAPResultCode.constraintViolation

class LDAPAttributeOrValueExists(LDAPError):
	result_code = LDAPResultCode.attributeOrValueExists

class LDAPInvalidAttributeSyntax(LDAPError):
	result_code = LDAPResultCode.invalidAttributeSyntax

class LDAPNoSuchObject(LDAPError):
	result_code = LDAPResultCode.noSuchObject

class LDAPAliasProblem(LDAPError):
	result_code = LDAPResultCode.aliasProblem

class LDAPInvalidDNSyntax(LDAPError):
	result_code = LDAPResultCode.invalidDNSyntax

class LDAPAliasDereferencingProblem(LDAPError):
	result_code = LDAPResultCode.aliasDereferencingProblem

class LDAPInappropriateAuthentication(LDAPError):
	result_code = LDAPResultCode.inappropriateAuthentication

class LDAPInvalidCredentials(LDAPError):
	result_code = LDAPResultCode.invalidCredentials

class LDAPInsufficientAccessRights(LDAPError):
	result_code = LDAPResultCode.insufficientAccessRights

class LDAPBusy(LDAPError):
	result_code = LDAPResultCode.busy

class LDAPUnavailable(LDAPError):
	result_code = LDAPResultCode.unavailable

class LDAPUnwillingToPerform(LDAPError):
	result_code = LDAPResultCode.unwillingToPerform

class LDAPLoopDetect(LDAPError):
	result_code = LDAPResultCode.loopDetect

class LDAPNamingViolation(LDAPError):
	result_code = LDAPResultCode.namingViolation

class LDAPObjectClassViolation(LDAPError):
	result_code = LDAPResultCode.objectClassViolation

class LDAPNotAllowedOnNonLeaf(LDAPError):
	result_code = LDAPResultCode.notAllowedOnNonLeaf

class LDAPNotAllowedOnRDN(LDAPError):
	result_code = LDAPResultCode.notAllowedOnRDN

class LDAPEntryAlreadyExists(LDAPError):
	result_code = LDAPResultCode.entryAlreadyExists

class LDAPObjectClassModsProhibited(LDAPError):
	result_code = LDAPResultCode.objectClassModsProhibited

class LDAPAffectsMultipleDSAs(LDAPError):
	result_code = LDAPResultCode.affectsMultipleDSAs

class LDAPOther(LDAPError):
	result_code = LDAPResultCode.other
