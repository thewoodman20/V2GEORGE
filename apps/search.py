import pyautogui
import webbrowser as wb
import time

def search(request):
    search_request = request
    if "search" in search_request:
        x = search_request.index("search")
        while int(x) != -1:
            del(search_request[0])
            x -= 1
        search_request = ' '.join(search_request)
    elif "Search" in search_request:
        x = search_request.index("Search")
        while int(x) != -1:
            del(search_request[0])
            x -= 1
        search_request = ' '.join(search_request)
    else:
        search_request = ' '.join(search_request)
    wb.open("www.google.com")
    time.sleep(1)
    pyautogui.typewrite(f'{search_request}\n', interval=.01)