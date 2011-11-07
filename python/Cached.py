#!/usr/bin/env python
import logging
logger = logging.getLogger(__name__)

class Cached(object):
	# contains the shared cache
	__cache = {}
	@classmethod
	def _key(*args, **kwargs):
		return (repr(args), repr(kwargs))
	def key(self, *arguments, **keywords):
		# return (self, repr(arguments), repr(keywords))
		return Cached._key(self.__class__, *arguments, **keywords)
	@property
	def cache(self):
		# logger.debug("accessing cache")
		return self.__cache
	@cache.setter
	def cache(self, other):
		logger.debug(str(self) + ": updating cache: %s" % str(self.__cache))

class CachedCall(Cached):
	__cache = {}
	def _cached(self, *args, **kwargs):
		# a stub
		pass
	def __call__(self, *arguments, **keywords):
		key = self.key(*arguments, **keywords)
		try:
			ret = self.__cache[key]
			logger.debug("CachedCall: hit: %s" % str(key))
		except KeyError:
			logger.debug("CachedCall: miss: %s" % str(key))
			ret = self.__cache[key] = self._cached(*arguments, **keywords)
		return ret

def _CachedNewFactory(cls, *args, **kwargs):
	return cls(*args, **kwargs)

class CachedNew(Cached):
	__cache = {}
	@classmethod
	def _key(*args, **kwargs):
		return hash(str(args) + str(kwargs))
	def __new__(subCached, *args, **kwargs):
		key = CachedNew._key(subCached, *args, **kwargs)
		if key in CachedNew.__cache:
			logger.debug("CachedNew: hit: %s" % str(key))
		else:
			logger.debug("CachedNew: miss: %s" % str(key))
			CachedNew.__cache[key] = ret = super(CachedNew, subCached).__new__(subCached, *args, **kwargs)
			return ret
	def __init__(self, *args, **kwargs):
		#key = CachedNew._key('prd')
		#self.__cache[key] = self
		#logger.debug("CachedNew: updated: %s: %s" % (str(key), str(self.__cache[key])))
		#logger.debug("CachedNew: updated")
		pass


