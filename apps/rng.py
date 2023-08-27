import random


from gtts import gTTS
from playsound import playsound

def speak(audio):
    speech = gTTS(audio)
    with open('speech.mp3', 'wb') as f:
        speech.write_to_fp(f)
    playsound('C:/Users/georg/OneDrive/Documents/Repos/V2GEORGE/speech.mp3') #specify the file path of the mp3 file 

def pas(output):  #print and speak function
    print(output)
    speak(output)

def coin(request):
    num_of_coins = 1
    if "coins" in request:
        try:
            num_of_coins = int(request[request.index("coins") - 1])
        except ValueError:
            num_of_coins = 1
    for _ in range(num_of_coins):
        pas("Heads" if random.randint(0, 1) == 0 else "Tails")

def dice(request):
    num_of_dice = 1
    multiplier = 1
    for word in request:
        if parse_dice_string(word) == None:
            continue
        else:
            num_of_dice, multiplier = parse_dice_string(word)
            if num_of_dice <= 1:
                try:
                    num_of_dice = int(request[request.index(word) - 1])
                except ValueError:
                    num_of_dice = 1
            break
    for _ in range(num_of_dice):
        pas(random.randint(1, multiplier))


def parse_dice_string(dice_string):
    if dice_string == "dice":
        return 1, 6
    else:
        dice_string = dice_string.split('d')
        if len(dice_string) == 2:
            try:
                return 1 if dice_string[0] == '' else int(dice_string[0]), int(dice_string[1])
            except ValueError:
                return None
        else:
            return None


def rng(request):  # TODO: add flip coin and roll dice
    num_range = []

    for word in request:
        try:
            num = int(word)
            num_range.append(num)
        except ValueError:
            continue

    if len(num_range) >= 2:
        pas(random.randint(num_range[0], num_range[1]))
    else:
        pas("Couldn't compute range.")