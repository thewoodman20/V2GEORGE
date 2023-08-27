import time
from gtts import gTTS
from playsound import playsound
import utils

def timer(request):
    seconds = 0

    grandfather = {
        "hour": 3600,
        "minute": 60,
        "second": 1
    }

    for type in grandfather.keys():
        if type in request:
            try:
                seconds += grandfather[type] * \
                    int(request[request.index(type) - 1]) #error when the code adds a hyphen - print valye says "set a 1-minute timer"
            except ValueError:
                print("invalid input")
                timer(request)
        elif type + "s" in request:
            try:
                seconds += grandfather[type] * \
                    int(request[request.index(type + "s") - 1])
            except ValueError:
                print("invalid input")
                timer(request)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        utils.pas(str(f"Starting your {hours} hour timer now")) 
    elif minutes > 0:
        utils.pas (str(f"Starting your {minutes} minute timer now")) 
    else: 
        utils.pas (str(f"Starting your {seconds} second timer now")) 
    if seconds > 0:
        for i in range(seconds, 0, -1):  # i in range() is counting the items in a list that starts from seconds and ends at 0 decreasing in intervals of 1. This could be changed for example -2 would decrease 2x the rate
            m, s = divmod(i, 60)
            h, m = divmod(m, 60)
            print(f"{h:02d}:{m:02d}:{s:02d}", end='\r')
            time.sleep(1)

        print("00:00:00", end="\r")
        utils.pas('\n' + "The timer is complete.")
    else:
        print("inval2")