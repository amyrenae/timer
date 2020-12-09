import time
import sys
from tkinter import *
from tkinter import messagebox


# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry("800x800")

# Using title() to display a message in
# the dialogue box of the message in the
# title bar.
root.title("Exercise Timer")

# Declaration of variables
active_time = StringVar()
recover_time = StringVar()

# setting the default value as 0
active_time.set("00")
recover_time.set("00")

active_lbl = Label(root, text="active time", justify='center', font=("Arial", 30))
active_lbl.place(x=10,y=5)
# active_lbl.grid(row=0, column=0)

#creating the entry boxes for the interval time spans
active_time_entry = Entry(root, width=2, font=("Arial",30,""),
                          textvariable=active_time, justify='center')
active_time_entry.place(x=10,y=40)
# active_time_entry.grid(row=1, column=0)

recover_lbl = Label(root, text="recover time", justify='center', font=("Arial", 30))
recover_lbl.place(x=400,y=5)
# recover_lbl.grid(row=0, column=2)

recover_time_entry = Entry(root, width=2, font=("Arial",30,""),
                           textvariable=recover_time, justify='center')
recover_time_entry.place(x=400,y=40)
# recover_time_entry.grid(row=1, column=2)



timer_label = Label(root, text="00:00", justify='center', font=("Arial", 50))
interval_countdown_label = Label(root, text="0", justify='center', font=("Arial", 200))
interval_type_lbl = Label(root, text="",
                      justify='center',
                      font=("Arial", 100))

# go_back = Button(root, text='pause', bd='5',
#                       command= lambda: pause_timer(0, 'active', int(active_time_entry.get())),
#                       font=("Arial", 20))

timer_paused = False


def reset_timer():
	setup_timer()
	pause_timer(0, 'active', int(active_time_entry.get()))


def start_timer(seconds_passed, interval, interval_time):
	global timer_paused
	timer_paused = False
	update_timer(seconds_passed, interval, interval_time)


def pause_timer(seconds_passed, interval, interval_time):
	global timer_paused
	timer_paused = True
	start_button.config(command=lambda: start_timer(seconds_passed, interval, interval_time))
	root.update()


def setup_timer():
	setup_btn.place_forget()

	active_time_entry.place_forget()
	active_lbl.place_forget()

	recover_lbl.place_forget()
	recover_time_entry.place_forget()



	interval_type_lbl.config(text="", bg="white")
	# interval_type_lbl.place(x=340, y=100)
	interval_type_lbl.pack()

	interval_countdown_label.config(text="0", bg="white")
	# interval_countdown_label.place(x=380, y=400)
	interval_countdown_label.pack()


	root.config(bg="white")

	start_button.place(x=100, y=700)
	pause_button.place(x=350, y=700)
	reset_button.place(x=600, y=700)

	timer_label.config(text="00:00", bg="white")
	# timer_label.place(x=340, y=750)
	timer_label.pack(side=BOTTOM)

	root.update()


def update_timer(seconds_passed, interval, interval_time):

	pause_button.config(command=lambda: pause_timer(seconds_passed, interval, interval_time))
	phase = {'active': {'title': 'go!',
							 'interval_duration': int(active_time_entry.get()),
							 'color': 'green'},
			 'recover': {'title': 'rest',
				  		 'interval_duration': int(recover_time_entry.get()),
				  		 'color': 'pink'}}

	if interval_time < 1:
		if interval == 'active':
			interval = 'recover'
		else:
			interval = 'active'

		interval_time = phase[interval]['interval_duration']


	if seconds_passed < 120 and not timer_paused:
	# 	# divmod(firstvalue = seconds_passed//60, secondvalue = seconds_passed%60)
		mins,secs = divmod(seconds_passed,60)

		minutes = "{:0>2}".format(mins)
		seconds = "{:0>2}".format(secs)

		display = "{minutes}:{seconds}".format(minutes=minutes, seconds=seconds)


		timer_label.config(text=display,
		                   bg=phase[interval]['color'])
		# timer_label.place(x=60, y=100)

		interval_countdown_label.config(text=interval_time,
		                                bg=phase[interval]['color'])

		interval_type_lbl.config(text=phase[interval]['title'],
		                         bg=phase[interval]['color'])


		root.config(bg=phase[interval]['color'])

		# updating the GUI window after decrementing the
		# seconds_passed value every time
		root.update()
		# if timer_paused == False:
		root.after(1000, update_timer, seconds_passed+1, interval, interval_time-1)



start_button = Button(root, text='start', bd='5',
                      command= lambda: start_timer(0, 'active', int(active_time_entry.get())),
                      font=("Arial", 20))

pause_button = Button(root, text='pause', bd='5',
                      command= lambda: pause_timer(0, 'active', int(active_time_entry.get())),
                      font=("Arial", 20))

reset_button = Button(root, text='reset', bd='5',
                      command=reset_timer,
                      font=("Arial", 20))
# button widget
setup_btn = Button(root, text='Set Up Timer', bd='5',
			 command=setup_timer,
			 font=("Arial", 20))
setup_btn.place(x=380, y=120)
# setup_btn.grid(row=3, column=1)


# timer_label = Label(root, text="00:00", justify='center', font=("Arial", 50))
# timer_label.place(x=110, y=150)

# interval_countdown_label = Label(root, text="0", justify='center', font=("Arial", 32))
# interval_countdown_label.place(x=70, y=250)

# interval_type_lbl = Label(root, text="",
#                           justify='center',
#                           font=("Arial", 100))
# interval_type_lbl.place(x=60, y=20)

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
root.mainloop()
