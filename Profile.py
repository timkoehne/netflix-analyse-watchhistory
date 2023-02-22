#!/bin/python3
from datetime import datetime, timedelta
from TVShow import TVShow
from CSVEntry import CSVEntry

class Profile:
	def __init__(self, name: str):
		self.name = name
		self.watched_list = {}

	def __eq__(self, item: str):
		return self.name == item

	def __str__(self):
		return self.name

	def add_episode(self, csv: CSVEntry):
		if csv.show_title not in self.watched_list:
			self.watched_list[csv.show_title] = TVShow(csv.show_title)
		duration = datetime.strptime(csv.watch_duration, "%H:%M:%S")
		self.watched_list[csv.show_title].watch_time += timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
		self.watched_list[csv.show_title].number_views += 1
	
	def calculate_overall(self, list):
		overall = TVShow("Overall")
		overall.number_views = sum(x.number_views for x in self.watched_list.values())
		overall.watch_time = sum((x.watch_time for x in self.watched_list.values()), timedelta())
		list.append(overall)
		return list

	def sort_watchlist_by_watch_time(self):
		list = sorted(self.watched_list.values(), key=lambda x: x.watch_time)
		list = self.calculate_overall(list)
		return list

	def sort_watchlist_by_number_views(self):
		list = sorted(self.watched_list.values(), key=lambda x: x.number_views)
		list = self.calculate_overall(list)
		return list
