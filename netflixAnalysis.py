#!/bin/python3
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import timedelta
import os
from Profile import Profile
from CSVEntry import CSVEntry

def generate_data_watch_time(num_entries: int) -> tuple[tuple[str], tuple[int]]:
	data = ()
	ind = ()

	profile = profiles[selected_user.get()]

	if overall_checked.get()==True:
		watchlist = profile.sort_watchlist_by_watch_time()[-num_entries:]
	else:
		watchlist = profile.sort_watchlist_by_watch_time()[-num_entries-1:-1]

	for show in watchlist:
		data = data + (show.watch_time.total_seconds(),)
		ind = ind + (show.name,)
	return (data, ind)
	
def generate_data_number_views(num_entries: int) -> tuple[tuple[str], tuple[int]]:
	data = ()
	ind = ()

	profile = profiles[selected_user.get()]

	if overall_checked.get()==True:
		watchlist = profile.sort_watchlist_by_number_views()[-num_entries:]
	else:
		watchlist = profile.sort_watchlist_by_number_views()[-num_entries-1:-1]

	for show in watchlist:
		data = data + (show.number_views,)
		ind = ind + (show.name,)
	return (data, ind)

def generate_data() -> tuple[tuple[str], tuple[int]]:
	global num_shows_to_display
	if selected_metric.get() == "WatchTime":
		return generate_data_watch_time(num_shows_to_display)
	else:
		return generate_data_number_views(num_shows_to_display)

def update_figure(event = ""):
	global f
	global ax
	global canvas

	ax.clear()

	data, ind = generate_data()

	ax.barh(ind, data)
	if(selected_metric.get()=="WatchTime"):
		ax.xaxis.set_major_formatter(lambda x, pos: str(timedelta(seconds=x)))
		ax.set_xlabel("watch time")
	else:
		ax.set_xlabel("number of views")

	# Add x, y gridlines
	ax.grid(visible=True, color ='grey',
			linestyle ='-.', linewidth = 0.5,
			alpha = 0.2)

	#add annotation to bars
	if(selected_metric.get()=="WatchTime"):
		for bar in ax.patches:
			annotate_bar(bar, str(timedelta(seconds=bar.get_width())))
	else:
		for bar in ax.patches:
			annotate_bar(bar, str(bar.get_width()))

	canvas.draw()
	canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)

def annotate_bar(bar, text: str):
	global ax
	max_width = max([bar.get_width() for bar in ax.patches])
 
	#annotate inside the bar unless the bar is very small, then annotate to the right of the bar
	if bar.get_width() > 0.15*max_width:
		ax.text(bar.get_width(), 
			bar.get_y() + bar.get_height()/2.0,
			text,
			fontweight ='bold',
			va = 'center',
			ha = 'right',
			color ='white')
	else:
		ax.text(bar.get_width(), 
			bar.get_y() + bar.get_height()/2.0,
			text,
			fontweight ='bold',
			va = 'center',
			ha = 'left',
			color ='black')

def select_file() -> str:
	filetypes = (('csv file', '*.csv'),( 'All files', '*.*'))

	filename = tk.filedialog.askopenfilename(
		title='Select Netflix viewing activity file',
		initialdir='.',
		filetypes=filetypes
	)
	return filename

def create_ui():
	global selected_user
	global selected_metric
	global overall_checked
	#create user combobox
	possible_users = [profile.name for profile in profiles.values()]
	selected_user = tk.StringVar(window)
	selected_user.set(possible_users[0])
	user_combobox = ttk.Combobox(window, textvariable=selected_user)
	user_combobox['values'] = possible_users
	user_combobox['state'] = 'readonly'
	user_combobox.bind('<<ComboboxSelected>>', update_figure)
	user_combobox.pack(pady=10)

	#create metric combobox
	possible_metrics = ["WatchTime", "NumberViews"]
	selected_metric = tk.StringVar(window)
	selected_metric.set(possible_metrics[0])
	metric_combobox = ttk.Combobox(window, textvariable=selected_metric)
	metric_combobox['values'] = possible_metrics
	metric_combobox['state'] = 'readonly'
	metric_combobox.bind('<<ComboboxSelected>>', update_figure)
	metric_combobox.pack()

	#create checkbox overall
	overall_checked = tk.BooleanVar(window)
	overall_checked.set(False)
	overall_checkbutton = tk.Checkbutton(window, 
									 text="show Overall?", 
									 variable=overall_checked, 
									 onvalue=True, 
									 offvalue=False, 
									 command=update_figure)
	overall_checkbutton.pack()

csv_entries = []
profiles = {}
num_shows_to_display = 20

#read netflix viewing activity file
filename = "Content_Interaction/ViewingActivity.csv"
if not os.path.exists(filename):
	filename = select_file()
with open(filename) as file:
	for line in file.readlines()[1:]:
		line = line.replace('"', "")
		csv_entries.append(CSVEntry(line.strip()))

#process file entries
for entry in csv_entries:
	if entry.profile_name not in profiles:
		profiles[entry.profile_name] = Profile(entry.profile_name)
	profiles[entry.profile_name].add_episode(entry)

# #print stats for shows per profile
# for profile in profiles.values(): 
# 	print("--------------------------------------------------------------------------")
# 	print(profile)
# 	for show in profile.sort_watchlist_by_watch_time():
# 	#for show in profile.sort_watchlist_by_number_views():
# 		print(show)

# #write episode titles to file. useful to find more regex 
# with open("titles", "w") as file:
# 	for entry in csv_entries:
# 		file.write(entry.show_title + "\n")

#create window
window = tk.Tk()
window.title("Netflix watch history analyser")
window.geometry("1500x800")
create_ui()

# display figure
f = Figure(figsize=(16, 9), dpi=100, layout='constrained')
ax = f.add_subplot(1, 1, 1)
canvas = FigureCanvasTkAgg(f, master=window)
update_figure()
window.mainloop()
