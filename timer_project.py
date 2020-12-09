import time
import sys
from tkinter import *

def setup_timer():
	"""disappears the widgets from the first screen and places all the new widgets"""
	active_lbl.place_forget()
	recover_lbl.place_forget()

	active_time_entry.place_forget()
	recover_time_entry.place_forget()

	setup_btn.place_forget()

	root.config(bg="white")
	interval_type_lbl.config(text="", bg="white")
	interval_countdown_lbl.config(text="0", bg="white")
	elapsed_time_lbl.config(text="00:00", bg="white")

	# interval_type_lbl.place(x=340, y=100)
	# interval_countdown_lbl.place(x=380, y=400)
	# elapsed_time_lbl.place(x=340, y=750)
	interval_type_lbl.pack(pady=20)
	interval_countdown_lbl.pack(pady=50)

	start_button.place(x=100, y=600)
	pause_button.place(x=325, y=600)
	reset_button.place(x=580, y=600)

	elapsed_time_lbl.pack(side=BOTTOM)

	root.update()


def start_timer(seconds_passed, interval, interval_time):
	"""sets timer_paused to False and runs update_timer function"""
	global timer_paused
	timer_paused = False
	update_timer(seconds_passed, interval, interval_time)


def pause_timer(seconds_passed, interval, interval_time):
	"""reconfigs the start button to the time durations at time of pause"""
	global timer_paused
	timer_paused = True
	start_button.config(command=lambda: start_timer(seconds_passed, interval, interval_time))
	root.update()


def reset_timer():
	"""reruns the setup function"""
	setup_timer()
	pause_timer(0, 'active', int(active_time_entry.get()))


def update_timer(seconds_passed, interval, interval_time):
	"""changes formatting and increased elapsed time and decreases interval countdown"""
	pause_button.config(command=lambda: pause_timer(seconds_passed, interval, interval_time))
	phase = {'active': {'title': 'go!',
						'interval_duration': int(active_time_entry.get()),
						'color': 'green'},
			 'recover': {'title': 'rest',
						 'interval_duration': int(recover_time_entry.get()),
						 'color': 'pink'}}
 	#switches to the other interval at the end of the interval duration
	if interval_time < 1:
		if interval == 'active':
			interval = 'recover'
		else:
			interval = 'active'
		interval_time = phase[interval]['interval_duration']


	if seconds_passed < 120 and not timer_paused:
	# 	# divmod(firstvalue = seconds_passed//60, secondvalue = seconds_passed%60)
		mins,secs = divmod(seconds_passed,60)
		display = "{minutes}:{seconds}".format(minutes="{:0>2}".format(mins),
		                                       seconds="{:0>2}".format(secs))

		###changes the background color of the window and the widgets
		##based on the interval type
		root.config(bg=phase[interval]['color'])

		interval_type_lbl.config(text=phase[interval]['title'],
		                         bg=phase[interval]['color'])

		interval_countdown_lbl.config(text=interval_time,
		                              bg=phase[interval]['color'])
		elapsed_time_lbl.config(text=display,
		                        bg=phase[interval]['color'])

		root.update()
		root.after(1000, update_timer, seconds_passed+1, interval, interval_time-1)


timer_paused = False

# creating Tk window
root = Tk()
root.geometry("800x800")
root.title("Exercise Timer")

# Declaration of variables
active_time = StringVar()
recover_time = StringVar()

##Setting up the first screen
# setting the default value as 0
active_time.set("00")
recover_time.set("00")

#labeling the entry boxes
active_lbl = Label(root, text="active time", justify='center', font=("Arial", 50))
recover_lbl = Label(root, text="recover time", justify='center', font=("Arial", 50))

#creating the entry boxes for the interval time spans
active_time_entry = Entry(root, width=2, font=("Arial",50,""),
						  textvariable=active_time, justify='center')
recover_time_entry = Entry(root, width=2, font=("Arial",50,""),
						   textvariable=recover_time, justify='center')

# button to establish the interval times and setup the timer screen
setup_btn = Button(root, text='Set Up Timer', bd='5',
			 command=setup_timer,
			 font=("Arial", 60))

# placing the widgets
active_lbl.place(x=100,y=125)
recover_lbl.place(x=425,y=125)

active_time_entry.place(x=175,y=200)
recover_time_entry.place(x=500,y=200)

setup_btn.place(x=220, y=500)


####Establishing the widgets for placement on the timer screen
interval_type_lbl = Label(root, text="",
					  justify='center',
					  font=("Arial", 100))

interval_countdown_lbl = Label(root, text="0", justify='center', font=("Arial", 300))

elapsed_time_lbl = Label(root, text="00:00", justify='center', font=("Arial", 50))


start_button = Button(root, text='start', bd='5',
					  command= lambda: start_timer(0, 'active', int(active_time_entry.get())),
					  font=("Arial", 50))

pause_button = Button(root, text='pause', bd='5',
					  command= lambda: pause_timer(0, 'active', int(active_time_entry.get())),
					  font=("Arial", 50))

reset_button = Button(root, text='reset', bd='5',
					  command=reset_timer,
					  font=("Arial", 50))

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
root.mainloop()
