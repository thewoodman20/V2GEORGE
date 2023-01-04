def classy_music(request):
   wb.open('https://www.youtube.com/watch?v=53nwh1aHCU8')

#need to add a pause function which activates the insert hotkey on my keyboard


import pyautogui
import webbrowser as wb
import time


def music(request):
    song_request = request
    if "play" in song_request:
        x = song_request.index("play")
        while int(x) != -1:
            del(song_request[0])
            x -= 1
        song_request = ' '.join(song_request)
    elif "Play" in song_request:
        x = song_request.index("Play")
        while int(x) != -1:
            del(song_request[0])
            x -= 1
        song_request = ' '.join(song_request)
    else:
        song_request = ' '.join(song_request)
    wb.open("www.google.com")
    time.sleep(1)
    pyautogui.typewrite(f'{song_request}\n', interval=.01)
        
