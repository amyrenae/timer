from tkinter import *
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError
import sys
import threading

sys.path.insert(0, '/Users/amyveggeberg/Desktop/super/')
from loginz import wyze

client = Client(email=wyze['email'], password=wyze['password'])

try:
    response = client.devices_list()
except WyzeApiError as e:
    print(f"Got an error: {e}")


def setup_input_screen():
    #clear previous buttons (if reverting)
    global timer_paused
    timer_paused = True

    # disappear all countdowntimer screen widgets
    # previous_screen_button.place_forget()
    previous_screen_button.grid_forget()
    interval_type_lbl.pack_forget()
    interval_countdown_lbl.pack_forget()
    delay_timer_cntdown_lbl.place_forget()
    start_button.place_forget()
    pause_button.place_forget()
    reset_button.place_forget()
    elapsed_time_lbl.pack_forget()

    root.config(bg="white")

    active_time.set("00")
    recovery_time.set("00")
    delay_start.set("10")

    active_time_entry.config(textvariable=active_time)
    recovery_time_entry.config(textvariable=recovery_time)
    delay_start_entry.config(textvariable=delay_start)

    active_lbl.place(x=500, y=195)
    active_time_entry.place(x=675, y=185)
    recovery_lbl.place(x=425, y=330)
    recovery_time_entry.place(x=675, y=320)
    delay_lbl.place(x=525, y=467)
    delay_start_entry.place(x=675, y=460)

    setup_btn.pack(side=BOTTOM, pady=150)

    root.update()


def setup_timer_screen():
    """sets up timer screen"""
    # disappear previous screens widgets
    delay_lbl.place_forget()
    active_lbl.place_forget()
    recovery_lbl.place_forget()

    delay_start_entry.place_forget()
    active_time_entry.place_forget()
    recovery_time_entry.place_forget()

    setup_btn.pack_forget()

    # reset configs to white/basic text
    root.config(bg="white")
    interval_type_lbl.config(text="", bg="white")
    interval_countdown_lbl.config(text="0", bg="white")
    elapsed_time_lbl.config(text="00:00", bg="white")

    phases = {'active': {'title': 'go!',
                    'interval_duration': int(active_time_entry.get()),
                    'color': 'green',
                    'hex': '00FF00'},
         'recovery': {'title': 'rest',
                      'interval_duration': int(recovery_time_entry.get()),
                      'color': 'pink',
                      'hex': 'FF0000'}}

    active_input = int(active_time_entry.get())
    delay_input = int(delay_start_entry.get())
    start_button.config(command=lambda: start_timer(delay_input,
                                                    0,
                                                    'active',
                                                    active_input,
                                                    phases))
    root.columnconfigure(0, weight=1, minsize=95)
    root.columnconfigure(1, weight=1, minsize=95)
    root.columnconfigure(2, weight=1, minsize=95)

    root.rowconfigure(0, weight=1, minsize=30)
    root.rowconfigure(1, weight=1, minsize=80)
    root.rowconfigure(2, weight=1, minsize=110)

    # previous_screen_button.place(x=10, y=10)
    previous_screen_button.grid(row=0, column=0, sticky="nw")

    # interval_type_lbl.pack(pady=20)
    interval_type_lbl.grid(row=0, column=1)
    # interval_countdown_lbl.pack(pady=25)
    interval_countdown_lbl.grid(row=1, column=1, sticky="nsew")

    # pause_button.place(x=299, y=600)#100
    pause_button.grid(row=2, column=0, sticky="ne")
    # start_button.place(x=524, y=587)#325
    start_button.grid(row=2, column=1, sticky="n", pady=5)
    # reset_button.place(x=754, y=600)#555
    reset_button.grid(row=2, column=2, sticky="nw")

    # elapsed_time_lbl.pack(side=BOTTOM)
    elapsed_time_lbl.grid(row=2, column=1, sticky="s")

    root.update()


def start_timer(delay, seconds_passed, interval_type, interval_time, phases):
    """sets timer_paused to False and runs update_timer function"""
    global timer_paused

    #loops through the amount time left on the delay display
    if delay >= 1:
        delay_timer_cntdown_lbl.config(text=delay)
        delay_timer_cntdown_lbl.place(x=750, y=200)
        root.update()
        root.after(1000, start_timer, delay-1,
                   seconds_passed, interval_type, interval_time, phases)
    else:
        delay_timer_cntdown_lbl.place_forget()
        root.update()
        timer_paused = False
        t1 = threading.Thread(target=change_lights, args=(phases[interval_type]['hex'],))
        t1.start()
        update_timer(seconds_passed, interval_type, interval_time, phases)


def pause_timer(seconds_passed, interval_type, interval_time, phases):
    """pauses the timer and sets the start button to start where left off"""
    global timer_paused
    timer_paused = True
    start_button.config(command=lambda: start_timer(int(delay_start_entry.get()),
                                                    seconds_passed,
                                                    interval_type,
                                                    interval_time,
                                                    phases))
    root.update()


def reset_timer(phases):
    """resets the timer screen"""
    setup_timer_screen()
    pause_timer(0, 'active', int(active_time_entry.get()), phases)


def update_timer(seconds_passed, interval_type, interval_time, phases):
    """changes formatting and increased elapsed time and decreases interval countdown"""
    # new_interval = False
    pause_button.config(command=lambda: pause_timer(seconds_passed,
                                                    interval_type,
                                                    interval_time,
                                                    phases))

    if seconds_passed < 480 and not timer_paused:
        # seconds_passed//60, secondvalue = seconds_passed%60)
        mins, secs = divmod(seconds_passed, 60)
        display = "{minutes}:{seconds}".format(minutes="{:0>2}".format(mins),
                                               seconds="{:0>2}".format(secs))
        # changes the background color of the window and the widgets
        # based on the interval type
        interval_type_lbl.config(text=phases[interval_type]['title'],
                                 bg=phases[interval_type]['color'])
        interval_countdown_lbl.config(text=interval_time,
                                      bg=phases[interval_type]['color'])
        elapsed_time_lbl.config(text=display,
                                bg=phases[interval_type]['color'])

        root.config(bg=phases[interval_type]['color'])
        root.update()

        seconds_passed += 1
        interval_time -= 1
    #switches to the other interval at the end of the interval duration
        if interval_time < 1:
            if interval_type == 'active':
                interval_type = 'recovery'
            else:
                interval_type = 'active'
            interval_time = phases[interval_type]['interval_duration']
            t1 = threading.Thread(target=change_lights, args=(phases[interval_type]['hex'],))
            t1.start()

        root.after(1000, update_timer, seconds_passed, interval_type, interval_time, phases)


def change_lights(hex_a):
        bulb = response[4]
        client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color=hex_a)


timer_paused = False
# delay_duration = 10
# creating Tk window
root = Tk()
root.geometry("1200x800")
root.title("Exercise Timer")

##### INPUT SCREEN WIDGETS #####
# Declaration of variables
active_time = StringVar()
recovery_time = StringVar()
delay_start = StringVar()

# setting the default value as 0
active_time.set("00")
recovery_time.set("00")
delay_start.set("10")

# entry box labels
active_lbl = Label(root, text="active", justify='center', font=("Arial", 60))
recovery_lbl = Label(root, text="recovery", justify='center', font=("Arial", 60))
delay_lbl = Label(root, text="delay start", justify='center', font=("Arial", 30))

# interval time entry boxes
active_time_entry = Entry(root, width=2, font=("Arial", 70, ""),
                          textvariable=active_time, justify='center')
recovery_time_entry = Entry(root, width=2, font=("Arial", 70, ""),
                            textvariable=recovery_time, justify='center')
delay_start_entry = Entry(root, width=2, font=("Arial", 35, ""),
                            textvariable=delay_start, justify='center')

# button to set the interval times and changes to/sets up the timer screen
setup_btn = Button(root, text='Set Up Timer', bd='5',
                   command=setup_timer_screen,
                   font=("Arial", 60))


#### TIMER SCREEN WIDGETS ####
interval_type_lbl = Label(root, text="",
                          justify='center',
                          font=("Arial", 100))
# countdown displays
interval_countdown_lbl = Label(root, text="0", justify='center', font=("Arial", 350))
delay_timer_cntdown_lbl = Label(root, text="", justify='center', font=("Arial", 50))
elapsed_time_lbl = Label(root, text="00:00", justify='center', font=("Arial", 50))

# buttons
start_button = Button(root, text='start', bd='20',
                      command=lambda: start_timer(int(delay_start_entry.get()),
                                                  0,
                                                  'active',
                                                  int(active_time_entry.get()),
                                                  phases),
                      font=("Arial", 70), bg='grey')

pause_button = Button(root, text='pause', bd='7',
                      command=lambda: pause_timer(0,
                                                  'active',
                                                  int(active_time_entry.get()),
                                                  phases),
                      font=("Arial", 50),
                      bg='grey')

reset_button = Button(root, text='reset', bd='7', command=lambda: reset_timer(phases),
                      font=("Arial", 50),
                      bg='grey')

previous_screen_button = Button(root, text='previous screen', bd='5',
                                command=setup_input_screen,
                                font=("Arial", 20))

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
setup_input_screen()
root.mainloop()
