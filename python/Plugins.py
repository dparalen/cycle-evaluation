#!/usr/bin/env python
# simple plugin architecture based upon:
#   http://martyalchin.com/2008/jan/10/simple-plugin-framework/

class PluginMount(type):
	def __init__(cls, name, bases, attrs):
		if not hasattr(cls, 'plugins'):
			cls.plugins = []
		else:
			cls.plugins.append(cls)


class Evaluation(object):
	# evaluation plugins superclass
	# all subtypes conforming to this type should provide following
	# attributes:
	#   thousand_seeds
	#   hundred_seeds
	#   scaled_epsilon
	#   non_scaled_epsilon
	#   time
	#   one_ap_filter
	#   four_ap_filter
	#   sixteen_ap_filter
	# __init__ methods will be called without parameters
	pass

class Evaluation3D(Evaluation):
	__metaclass__ = PluginMount

class Evaluation2D(Evaluation):
	__metaclass__ = PluginMount

class Thousand(object):
	# denotes a Thousand property
	pass

class Hundred(object):
	# denotes a Hundred property
	pass

class Scaled(object):
	# denotes a Scaled property
	pass

class NonScaled(object):
	# denotes a Non-Scaled property
	pass
