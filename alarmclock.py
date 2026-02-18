from tkinter import *
import datetime
import time
import winsound
from threading import Thread
import os

# ---------------- WINDOW ----------------
root = Tk()
root.title("Alarm Clock - Python 3.14")
root.geometry("500x540")
root.configure(bg="#121212")
root.resizable(False, False)

alarm_running = False
snooze_minutes = 5

# ---------------- DEFAULT SOUND ----------------
default_sound = "default_alarm.wav"

if os.path.exists(default_sound):
    selected_sound = default_sound
else:
    selected_sound = None

# ---------------- LIVE CLOCK ----------------
def update_clock():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    live_clock.config(text=now)
    root.after(1000, update_clock)

# ---------------- START ALARM ----------------
def start_alarm():
    global alarm_running
    if not alarm_running:
        alarm_running = True
        t = Thread(target=alarm)
        t.daemon = True
        t.start()

# ---------------- ALARM LOGIC ----------------
def alarm():
    global alarm_running

    set_time = f"{hour.get()}:{minute.get()}:{second.get()}"
    set_datetime = datetime.datetime.strptime(set_time, "%H:%M:%S").time()

    while alarm_running:
        now = datetime.datetime.now()
        today_alarm = datetime.datetime.combine(now.date(), set_datetime)

        if today_alarm < now:
            today_alarm += datetime.timedelta(days=1)

        remaining = today_alarm - now
        total_seconds = int(remaining.total_seconds())

        hrs = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        countdown_label.config(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")

        if total_seconds <= 0:
            play_sound()
            break

        time.sleep(1)

# ---------------- PLAY SOUND ----------------
def play_sound():
    global selected_sound

    if selected_sound and os.path.exists(selected_sound):
        winsound.PlaySound(selected_sound,
                           winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    else:
        # Fallback beep
        for _ in range(10):
            winsound.Beep(1000, 500)

# ---------------- STOP ----------------
def stop_alarm():
    global alarm_running
    alarm_running = False
    winsound.PlaySound(None, winsound.SND_PURGE)
    countdown_label.config(text="--:--:--")

# ---------------- SNOOZE ----------------
def snooze():
    winsound.PlaySound(None, winsound.SND_PURGE)
    new_time = datetime.datetime.now() + datetime.timedelta(minutes=snooze_minutes)
    hour.set(new_time.strftime("%H"))
    minute.set(new_time.strftime("%M"))
    second.set(new_time.strftime("%S"))
    start_alarm()

# ---------------- UI ----------------
Label(root, text="⏰ ALARM CLOCK",
      font=("Segoe UI", 22, "bold"),
      fg="#00ADB5",
      bg="#121212").pack(pady=10)

live_clock = Label(root,
                   font=("Consolas", 34, "bold"),
                   fg="#EEEEEE",
                   bg="#121212")
live_clock.pack()
update_clock()

# -------- Time Selection --------
frame = Frame(root, bg="#121212")
frame.pack(pady=20)

hour = StringVar(root)
minute = StringVar(root)
second = StringVar(root)

hours = [f"{i:02d}" for i in range(24)]
minutes = [f"{i:02d}" for i in range(60)]
seconds = [f"{i:02d}" for i in range(60)]

hour.set("00")
minute.set("00")
second.set("00")

OptionMenu(frame, hour, *hours).pack(side=LEFT, padx=5)
OptionMenu(frame, minute, *minutes).pack(side=LEFT, padx=5)
OptionMenu(frame, second, *seconds).pack(side=LEFT, padx=5)

# -------- Buttons --------
Button(root, text="SET ALARM",
       font=("Segoe UI", 12, "bold"),
       bg="#00ADB5",
       fg="black",
       width=22,
       command=start_alarm).pack(pady=6)

Button(root, text="STOP",
       font=("Segoe UI", 11),
       bg="#393E46",
       fg="white",
       width=22,
       command=stop_alarm).pack(pady=6)

Button(root, text="SNOOZE (5 min)",
       font=("Segoe UI", 11),
       bg="#FF9800",
       fg="black",
       width=22,
       command=snooze).pack(pady=6)

# -------- Sound Info --------

# -------- Countdown --------
Label(root, text="Countdown",
      font=("Segoe UI", 13),
      fg="#AAAAAA",
      bg="#121212").pack(pady=(25,5))

countdown_label = Label(root,
                        text="--:--:--",
                        font=("Consolas", 34, "bold"),
                        fg="#FF5722",
                        bg="#121212")
countdown_label.pack()

root.mainloop()
