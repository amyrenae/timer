import time
import sys
from tkinter import *
from tkinter import messagebox


# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry("400x300")

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

#creating the entry boxes for the interval time spans
active_time_entry = Entry(root, width=2, font=("Arial",30,""),
                          textvariable=active_time, justify='center')
active_time_entry.place(x=10,y=40)

active_lbl = Label(root, text="active time", justify='center', font=("Arial", 24))
active_lbl.place(x=10,y=5)
# active_time_entry.pack(side=LEFT, expand=True)

recover_time_entry = Entry(root, width=2, font=("Arial",30,""),
                           textvariable=recover_time, justify='center')
recover_time_entry.place(x=180,y=40)

recover_lbl = Label(root, text="recover time", justify='center', font=("Arial", 24))
recover_lbl.place(x=180,y=5)


def update_timer(seconds_passed, interval, interval_time):

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


	if seconds_passed < 60:
	# 	# divmod(firstvalue = seconds_passed//60, secondvalue = seconds_passed%60)
		mins,secs = divmod(seconds_passed,60)

		minutes = "{:0>2}".format(mins)
		seconds = "{:0>2}".format(secs)

		display = "{minutes}:{seconds}".format(minutes=minutes, seconds=seconds)

		active_time_entry.place_forget()
		active_lbl.place_forget()

		recover_lbl.place_forget()
		recover_time_entry.place_forget()


		timer_label.config(text=display, font=("Arial", 100),
		                   bg=phase[interval]['color'])
		timer_label.place(x=60, y=100)

		interval_countdown_label.config(text=interval_time)

		interval_type_lbl.config(text=phase[interval]['title'],
		                         bg=phase[interval]['color'])


		root.config(bg=phase[interval]['color'])

		# updating the GUI window after decrementing the
		# seconds_passed value every time
		root.update()
		root.after(1000, update_timer, seconds_passed+1, interval, interval_time-1)



# button widget
btn = Button(root, text='Start Interval Timer', bd='5',
			 command= lambda: update_timer(0, 'active', int(active_time_entry.get())),
			 font=("Arial", 20))
btn.place(x=70, y=120)


timer_label = Label(root, text="00:00", justify='center', font=("Arial", 50))
timer_label.place(x=110, y=150)

interval_countdown_label = Label(root, text="0", justify='center', font=("Arial", 32))
interval_countdown_label.place(x=70, y=250)

interval_type_lbl = Label(root, text="",
                          justify='center',
                          font=("Arial", 100))
interval_type_lbl.place(x=60, y=20)

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
root.mainloop()
