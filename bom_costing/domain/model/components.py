#!/usr/bin/python

import copy
from ..errors import DuplicateError
from costs import Cost

class Bom:
	def __init__(self):
		self.__components=[]

	def add(self, component):
		if component in self.__components: 
			raise DuplicateError(component)
		self.__components.append(component)

	def cost(self, cost):
		for each in self.__components:
			each.cost(cost)	

	def is_costed(self):
		return 0
	
	def is_costed_part(self, bom_part): 
		return self.__first_costable(bom_part) and (self.__is_leaf(bom_part) or bom_part.costable())

	def __first_costable(self, bom_part):
		position=self.__components.index(bom_part)
		return 0==len([each for each in self.__components[:position] if each.is_costed()])

	def __is_leaf(self, bom_part):
		return self.__components[-1]==bom_part

	def export(self, level, exporter):
		level.export_bom(self.__data(), exporter)

	def __data(self):
		return copy.deepcopy(self.__components)


class BomPart:
	def __init__(self, part, quantity, bom):
		self.__part=part
		self.__quantity=quantity
		self.__bom=bom

	def cost(self, cost):
		if(self.is_costed()): 
			cost.add(self.__part.cost(self.__quantity))

	def is_costed(self): 
		return self.__part.is_costed()  or self.__bom.is_costed_part(self)

	def costable(self):
		return self.__part.costable()

	def export(self, level, exporter):
		exporter.export_part(self.__data(level))

	def __data(self, level):
		cost=Cost()
		self.cost(cost)
		return [level, self.__part, self.__quantity, cost]
