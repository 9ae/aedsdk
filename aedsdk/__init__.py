import inspect
from abc import ABCMeta, abstractmethod, abstractproperty
from decimal import *
class Interval:
	__metaclass__ = ABCMeta
	
	def __init__(self,duration=Decimal(0.0)):
		self.duration = duration
		self._prev = None
		self.events_end = []
		self.events_begin = []
		self.name = ''

	@property
	def prev(self):
		return self._prev
	
	@prev.setter
	def prev(self,value):
		self._prev = value
	
	def init_duration(self,value):
		self.duration = value
	
	@abstractmethod
	def meanwhile(self): pass

	def at_begin(self): 
		for act in self.events_begin:
			act()
	
	def at_end(self): 
		for act in self.events_end:
			act()
	
	def set_prop(self,name,val):
		pass
	
	def my_events(self):
		import re
		result = {}
		mystuff = self.__dict__
		for mys in mystuff:
			if re.match('events_',mys):
				result[mys] = getattr(self,mys)
		return result
	
	def register_actions(self,paradigm):
		for act_class in paradigm.atypes:
			action = act_class()
			action.set_executioner(self.exe)
			self.__setattr__('a_'+act_class.__name__,action)
	
	def set_executioner(self, exe):
		self.exe = exe
	
	def json(self):
		result = {'props':[]}
		result['type'] = type(self).__name__
		result['name'] = self.name
		return result
	
	def __str__(self):
		basic = self.name+" { duration:"+str(self.duration)
		return basic+" \n event chains: "+str(self.my_events())+" }"
	
class Action:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def detect(self): pass

	def set_prop(self,name,val):
		pass

	def set_executioner(self, exe):
		self.exe = exe
	
	def json(self):
		result = {'props':[]}
		result['type'] = type(self).__name__
		return result	
		
class Event:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def perform(self): pass
	
	def invoke(self):
		self.perform()

	def set_prop(self,name,val):
		pass

	def set_executioner(self, exe):
		self.exe = exe
	
	def json(self):
		result = {'props':[]}
		result['type'] = type(self).__name__
		return result	

class Paradigm(object):
	def __init__(self):
		self.atypes = []
		self.etypes = []
		self.itypes = []
		self.exe = None
		self.sort_classes()

	"""
	performed at the begining of an paradigm
	"""
	def bind_action_listeners(self): 
		action_names = []
		for aclass in self.atypes:
			action_names.append(['on_'+aclass.__name__,'events_'+aclass.__name__])
		# for each interval
		for iclass in self.itypes:
			for act_name in action_names:
				if hasattr(iclass,act_name[0]):
					self.__setattr__(act_name[1],[])
					# print iclass.__name__+' has '+act_name[1]
				else:
					pass
					# print act_name[0]+' not registered in '+iclass.__name__
		# > for each action
		# look for on_action
			
	def sort_classes(self):
			mystuff = self.__class__.__dict__
			good = True
			for key in mystuff:
					val = mystuff[key]
					if inspect.isclass(val):
							if issubclass(val,Interval):
									self.itypes.append(val)
							elif issubclass(val,Event):
									self.etypes.append(val)
							elif issubclass(val,Action):
									self.atypes.append(val)
							else:
									good = False
			return good
	
	def set_executioner(self, exe):
		self.exe = exe
		#for act_class in self.atypes:
		#	act_class.set_executioner(exe)
	
	def json(self):
		result = {'actions':[], 'intervals':[], 'events':[]}
		for a in self.atypes:
			result['actions'].append(a.json())
		for i in self.itypes:
			result['intervals'].append(i.json())
		for e in self.etypes:
			result['events'].append(e.json())
		return result
				
	def instantiate_name(self,name):
		return eval('self.'+name+'()')