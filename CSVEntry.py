#!/bin/python3
import re

class CSVEntry:
	def __init__(self, data: str):
		data = data.split(",")
		self.profile_name = data[0]
		self.watch_duration = data[2]
		self.show_title = str(episode_to_title(data[4].strip()))

def episode_to_title(episode: str) -> str:
	episode = re.sub(': Season \d.*', '', episode)
	episode = re.sub(': Staffel \d.*', '', episode)
	episode = re.sub(': Chapter \d.*', '', episode)
	episode = re.sub(': Series \d.*', '', episode)
	episode = re.sub(': Part (I|II|III|IV|V).*', '', episode)
	episode = re.sub(': Part \d.*', '', episode)
	episode = re.sub(': Teil \d.*', '', episode)
	episode = re.sub(': Book \d.*', '', episode)
	episode = re.sub(': Buch \d.*', '', episode)
	episode = re.sub(': Volume \d.*', '', episode)
	episode = re.sub(': Miniserie: .*', '', episode)
	episode = re.sub(': Limited Series.*', '', episode)
	episode = re.sub('DEATH NOTE: Death Note.*', 'Death Note', episode)
	episode = re.sub('3 %', '3%', episode)
	episode = re.sub(': Sword Art Online II:.*', '', episode)
	episode = re.sub(': Stranger Things \d.*', '', episode)
	episode = re.sub(': Black Butler.*', '', episode)
	episode = re.sub(': Black Butler II.*', '', episode)
	episode = re.sub('^(Trailer|Teaser):', '', episode)
	episode = re.sub('Élite-Kurzgeschichten:.*', 'Élite-Kurzgeschichten', episode)
	episode = re.sub(': Avatar – Der Herr der Elemente.*', '', episode)
	episode = re.sub('\(Trailer\)$', '', episode)
	episode = re.sub('(Staffel|Teil) \d \((Trailer|Teaser|Clip|Rückblick)( \d)?\): ', '', episode)
	episode = re.sub('(Season|Teil|Teaser) \d (Trailer|Recap|Clip|Teaser): ', '', episode)
	episode = re.sub('(DAHMER: )?Monster: Die Geschichte von Jeffrey Dahmer.*', 'Monster: Die Geschichte von Jeffrey Dahmer', episode)
	return episode