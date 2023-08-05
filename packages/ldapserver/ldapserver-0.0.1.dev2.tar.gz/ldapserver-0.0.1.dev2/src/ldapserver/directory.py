from .util import encode_attribute, AttributeDict
from .dn import DN
from .ldap import *

class BaseDirectory:
	'''Base class for LDAP directories'''

	def search(self, baseobj, scope, filter):
		'''Perform search

		:param baseobj: Distinguished name of the LDAP entry relative to which the search is
		                to be performed
		:type baseobj: str
		:param scope: Search scope
		:type scope: SearchScope
		:param filter: Filter object
		:type filter: Filter

		:returns: Iterable of dn, attributes tuples'''
		return []

class FilterMixin:
	'''Mixin for :any:`BaseDirectory` that implements :any:`BaseDirectory.search` by calling appropirate `filter_*` methods'''
	def search(self, baseobj, scope, filter):
		dn_res = self.filter_dn(baseobj, scope)
		filter_res = self.search_filter(filter)
		return self.search_fetch(self.filter_and(dn_res, filter_res))

	def search_fetch(self, result):
		'''
		'''
		return []

	def search_filter(self, expr):
		'''
		'''
		if isinstance(expr, FilterAnd):
			return self.filter_and(*[self.search_filter(subexpr) for subexpr in expr.filters])
		elif isinstance(expr, FilterOr):
			return self.filter_or(*[self.search_filter(subexpr) for subexpr in expr.filters])
		elif isinstance(expr, FilterNot):
			return self.filter_not(self.search_filter(expr.filter))
		elif isinstance(expr, FilterEqual):
			return self.filter_equal(expr.attribute.lower(), expr.value)
		elif isinstance(expr, FilterPresent):
			return self.filter_present(expr.attribute.lower())
		else:
			return False

	def filter_present(self, attribute):
		'''
		'''
		return False

	def filter_equal(self, attribute, value):
		'''
		'''
		return False

	def filter_and(self, *subresults):
		'''
		'''
		filtered = []
		for subres in subresults:
			if subres is True:
				continue
			if subres is False:
				return False
			filtered.append(subres)
		if not filtered:
			return True
		if len(filtered) == 1:
			return filtered[0]
		return self._filter_and(*filtered)

	def _filter_and(self, *subresults):
		'''
		'''
		return False

	def filter_or(self, *subresults):
		'''
		'''
		filtered = []
		for subres in subresults:
			if subres is True:
				return True
			if subres is False:
				continue
			filtered.append(subres)
		if not filtered:
			return False
		if len(filtered) == 1:
			return filtered[0]
		return self._filter_or(*filtered)

	def _filter_or(self, *subresults):
		'''
		'''
		return False

	def filter_not(self, subresult):
		'''
		'''
		if subresult is True:
			return False
		if subresult is False:
			return True
		return self._filter_not(subresult)

	def _filter_not(self, subresult):
		'''
		'''
		return False

	def filter_dn(self, baseobj, scope):
		'''
		'''
		return False

class SimpleFilterMixin(FilterMixin):
	def filter_present(self, attribute):
		if attribute in ['objectclass', 'structuralobjectclass', 'subschemasubentry']:
			return True
		return FilterPresent(attribute)

	def filter_equal(self, attribute, value):
		if attribute == 'objectclass':
			return value.lower() in [s.lower() for s in self.objectclasses]
		elif attribute == 'structuralobjectclass':
			return value.lower() == self.structuralobjectclass.lower()
		return FilterEqual(attribute, value)

	def _filter_and(self, *subresults):
		return FilterAnd(subresults)

	def _filter_or(self, *subresults):
		return FilterOr(subresults)

	def _filter_not(self, subresult):
		return FilterNot(subresult)

	def filter_dn(self, base, scope):
		base = DN(base)
		if scope == SearchScope.baseObject:
			if base[1:] != self.dn_base or len(base[0]) != 1 or base[0][0].attribute != self.rdn_attr:
				return False
			return self.filter_equal(self.rdn_attr, base[0][0].value)
		elif scope == SearchScope.singleLevel:
			return base == self.dn_base
		elif scope == SearchScope.wholeSubtree:
			if self.dn_base.in_subtree_of(base):
				return True
			if base[1:] != self.dn_base or len(base[0]) != 1 or base[0][0].attribute != self.rdn_attr:
				return False
			return self.filter_equal(self.rdn_attr, base[0][0].value)
		else:
			return False

class RootDSE(BaseDirectory, AttributeDict):
	def search(self, baseobj, scope, filter):
		if baseobj or scope != SearchScope.baseObject:
			return []
		if not isinstance(filter, FilterPresent) or filter.attribute.lower() != 'objectclass':
			return []
		attrs = {}
		for name, values in self.items():
			if callable(values):
				values = values()
			if not isinstance(values, list):
				values = [values]
			if values:
				attrs[name] = [encode_attribute(value) for value in values]
		return [('', attrs)]

class Subschema(BaseDirectory, AttributeDict):
	def __init__(self, *args, dn='cn=Subschema', **kwargs):
		super().__init__(*args, **kwargs)
		self.dn = DN(dn)
		for key, value in self.dn[0]:
			self.setdefault(key, [encode_attribute(value)])
		self.setdefault('objectClass', ['top', 'subentry', 'subschema', 'extensibleObject'])
		#if 'subschema' not in self['objectClass']:
		#	self['objectClass'].append('subschema')
		self.setdefault('structuralObjectClass', ['subentry'])

	def search(self, baseobj, scope, filter):
		if DN(baseobj) != self.dn or scope != SearchScope.baseObject:
			return []
		if not isinstance(filter, FilterEqual):
			return []
		if filter.attribute.lower() != 'objectclass' or filter.value.lower() != b'subschema':
			print('filter mismatch2')
			return []
		return [(str(self.dn), {key: [encode_attribute(value) for value in values] for key, values in self.items()})]

def eval_ldap_filter(obj, expr):
	'''Return whether LDAP filter expression matches attribute dictionary'''
	if expr is True:
		return True
	elif expr is False:
		return False
	elif isinstance(expr, FilterAnd):
		for subexpr in expr.filters:
			if not eval_ldap_filter(obj, subexpr):
				return False
		return True
	elif isinstance(expr, FilterOr):
		for subexpr in expr.filters:
			if eval_ldap_filter(obj, subexpr):
				return True
		return False
	elif isinstance(expr, FilterNot):
		return not eval_ldap_filter(obj, expr.filter)
	elif isinstance(expr, FilterEqual):
		return expr.value in obj.get(expr.attribute, [])
	elif isinstance(expr, FilterPresent):
		return bool(obj.get(expr.attribute, []))
	else:
		return False

class StaticDirectory(BaseDirectory):
	def __init__(self):
		self.objects = {} # dn -> attribute dict

	def add(self, dn, attributes):
		tmp = AttributeDict()
		for key, values in attributes.items():
			tmp[key] = [encode_attribute(value) for value in values]
		self.objects[DN(dn)] = tmp

	def search(self, baseobj, scope, filter):
		baseobj = DN(baseobj)
		for dn, attributes in self.objects.items():
			if scope == SearchScope.baseObject:
				if baseobj != dn:
					continue
			elif scope == SearchScope.singleLevel:
				if not dn.is_direct_child_of(baseobj):
					continue
			elif scope == SearchScope.wholeSubtree:
				if not dn.in_subtree_of(baseobj):
					continue
			else:
				continue
			if not eval_ldap_filter(attributes, filter):
				continue
			yield str(dn), attributes
