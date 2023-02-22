#!/bin/python3
from datetime import timedelta

class TVShow:
	def __init__(self, name):
		self.name = name
		self.watch_time = timedelta(hours=0, minutes=0, seconds=0)
		self.number_views = 0
	
	def __eq__(self, item: str):
		return self.name == item

	def __str__(self):
		return self.name + " was viewed " + str(self.number_views) + " times for a total of " + str(self.watch_time)
