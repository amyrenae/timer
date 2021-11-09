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
    # previous_screen_btn.place_forget()
    timer_screen_widgets = [previous_screen_btn, interval_type_lbl,
                            interval_countdown_lbl, delay_timer_cntdown_lbl,
                            start_btn, pause_btn, reset_btn, elapsed_time_lbl]

    for widget in timer_screen_widgets:
        widget.grid_forget()

    root.config(bg="white")

    active_time.set("00")
    recover_time.set("00")
    delay_start.set("10")

    active_time_ent.config(textvariable=active_time)
    recover_time_ent.config(textvariable=recover_time)
    delay_start_ent.config(textvariable=delay_start)

    root.columnconfigure(0, weight=1, minsize=95)
    root.columnconfigure(1, weight=1, minsize=95)
    root.columnconfigure(2, weight=1, minsize=95)
    root.columnconfigure(3, weight=1, minsize=95)

    root.rowconfigure(0, weight=1, minsize=30)
    root.rowconfigure(1, weight=1, minsize=80)
    root.rowconfigure(2, weight=1, minsize=110)

    active_lbl.grid(row=1, column=1, sticky="ne", pady=10)
    active_time_ent.grid(row=1, column=2, sticky="nw")
    recover_lbl.grid(row=1, column=1, sticky="e")
    recover_time_ent.grid(row=1, column=2, sticky="w")
    delay_lbl.grid(row=1, column=1, sticky="se", pady=5)
    delay_start_ent.grid(row=1, column=2, sticky="sw")
    setup_btn.grid(row=2, column=1, columnspan=2)

    # active_lbl.place(x=500, y=195)
    # active_time_ent.place(x=675, y=185)
    # recover_lbl.place(x=425, y=330)
    # recover_time_ent.place(x=675, y=320)
    # delay_lbl.place(x=525, y=467)
    # delay_start_ent.place(x=675, y=460)

    # setup_btn.pack(side=BOTTOM, pady=150)

    root.update()


def setup_timer_screen():
    """sets up timer screen"""
    # disappear previous screens widgets
    setup_screen_widgets = [delay_lbl, active_lbl, recover_lbl,
                            delay_start_ent, active_time_ent,
                            recover_time_ent, setup_btn]

    for widget in setup_screen_widgets:
        widget.grid_forget()


    # reset configs to white/basic text
    root.config(bg="white")
    interval_type_lbl.config(text="", bg="white")
    interval_countdown_lbl.config(text="0", bg="white")
    elapsed_time_lbl.config(text="00:00", bg="white")

    phases = {'active': {'title': 'go!',
                         'interval_duration': int(active_time_ent.get()),
                         'color': 'green',
                         'hex': '00FF00'},
             'recovery': {'title': 'rest',
                          'interval_duration': int(recover_time_ent.get()),
                          'color': 'pink',
                          'hex': 'FF0000'},
             'paused': {'hex': 'FDF4DC'}}

    t1 = threading.Thread(target=change_lights, args=(phases['paused']['hex'],))
    t1.start()

    active_input = int(active_time_ent.get())
    delay_input = int(delay_start_ent.get())
    start_btn.config(command=lambda: start_timer(delay_input,
                                                    0,
                                                    'active',
                                                    active_input,
                                                    phases))
    reset_btn.config(command=lambda: reset_timer(phases))

    root.columnconfigure(0, weight=1, minsize=425)
    root.columnconfigure(1, weight=1, minsize=350)
    root.columnconfigure(2, weight=1, minsize=425)

    root.rowconfigure(0, weight=1, minsize=30)
    root.rowconfigure(1, weight=1, minsize=80)
    root.rowconfigure(2, weight=1, minsize=110)

    previous_screen_btn.grid(row=0, column=0, sticky="nw")
    interval_type_lbl.grid(row=0, column=1)
    interval_countdown_lbl.grid(row=1, column=1, sticky="n")
    pause_btn.grid(row=2, column=0, sticky="ne", pady=10)
    start_btn.grid(row=2, column=1, sticky="n")
    reset_btn.grid(row=2, column=2, sticky="nw", pady=10)
    elapsed_time_lbl.grid(row=2, column=1, sticky="s", pady=1)

    # previous_screen_btn.place(x=10, y=10)
    # interval_type_lbl.pack(pady=20)
    # interval_countdown_lbl.pack(pady=25)
    # pause_btn.place(x=299, y=600)#100
    # start_btn.place(x=524, y=587)#325
    # reset_btn.place(x=754, y=600)#555
    # elapsed_time_lbl.pack(side=BOTTOM)

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
    t1 = threading.Thread(target=change_lights, args=(phases['paused']['hex'],))
    t1.start()
    start_btn.config(command=lambda: start_timer(int(delay_start_ent.get()),
                                                 seconds_passed,
                                                 interval_type,
                                                 interval_time,
                                                 phases))

    root.update()


def reset_timer(phases):
    """resets the timer screen"""
    setup_timer_screen()
    pause_timer(0, 'active', int(active_time_ent.get()), phases)


def update_timer(seconds_passed, interval_type, interval_time, phases):
    """changes formatting and increased elapsed time and decreases interval countdown"""
    pause_btn.config(command=lambda: pause_timer(seconds_passed,
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

        root.after(990, update_timer, seconds_passed, interval_type, interval_time, phases)


def change_lights(hex_a):
        bulb = response[2]
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
recover_time = StringVar()
delay_start = StringVar()

# setting the default value as 0
active_time.set("00")
recover_time.set("00")
delay_start.set("10")

# entry box labels
active_lbl = Label(root, text="active", justify='center', font=("Arial", 60),
                   bg='white')
recover_lbl = Label(root, text="recover", justify='center', font=("Arial", 60),
                    bg='white')
delay_lbl = Label(root, text="delay start", justify='center', font=("Arial", 30),
                  bg='white')

# interval time entry boxes
active_time_ent = Entry(root, width=2, font=("Arial", 70, ""),
                        textvariable=active_time, justify='center')
recover_time_ent = Entry(root, width=2, font=("Arial", 70, ""),
                         textvariable=recover_time, justify='center')
delay_start_ent = Entry(root, width=2, font=("Arial", 35, ""),
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
start_btn = Button(root, text='start', bd='10',
                   command=lambda: start_timer(int(delay_start_ent.get()),
                                               0,
                                               'active',
                                               int(active_time_ent.get()),
                                               phases),
                   relief='sunken',
                   font=("Arial", 70), bg='grey')

pause_btn = Button(root, text='pause', bd='10',
                   command=lambda: pause_timer(0,
                                               'active',
                                               int(active_time_ent.get()),
                                               phases),
                   font=("Arial", 50),
                   bg='grey')

reset_btn = Button(root, text='reset', bd='10', command=lambda: reset_timer(phases),
                   font=("Arial", 50),
                   bg='grey')

previous_screen_btn = Button(root, text='previous screen', bd='5',
                             command=setup_input_screen,
                             font=("Arial", 20))

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
setup_input_screen()
root.mainloop()
