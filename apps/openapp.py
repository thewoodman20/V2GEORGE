import pyautogui
import time

def openapp(request):
    application = request
    if "open" in application:
        x = application.index("open")
        while int(x) != -1:
            del(application[0])
            x -= 1
    application = ' '.join(application)
    pyautogui.hotkey('win', 'r')
    time.sleep(.5)
    pyautogui.typewrite(str(application),0.01)
    time.sleep(.5)
    print(application)
    pyautogui.hotkey('enter')
  

