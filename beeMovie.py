# Made for Collin
# Simply rumbles the Wiimote with the Bee Movie
#   script in morse code
#   Cuz why not

import sys
import cwiid
import time
import math

morseDict = {
    ' ': ",",
    'a': ".-",
    'b': "-...",
    'c': "-.-.",
    'd': "-..",
    'e': ".",
    'f': "..-.",
    'g': "--.",
    'h': "....",
    'i': "..",
    'j': ".---",
    'k': "-.-",
    'l': ".-..",
    'm': "--",
    'n': "-.",
    'o': "---",
    'p': ".--.",
    'q': "--.-",
    'r': ".-.",
    's': "...",
    't': "-",
    'u': "..-",
    'v': "...-",
    'w': ".--",
    'x': "-..-",
    'y': "-.--",
    'z': "--..",
    '1': ".----",
    '2': "..---",
    '3': "...--",
    '4': "....-",
    '5': ".....",
    '6': "-....",
    '7': "--...",
    '8': "---..",
    '9': "----.",
    '0': "-----"
}

beeMovieScript = "According to all known laws \
of aviation, \
there is no way a bee \
should be able to fly. \
Its wings are too small to get \
its fat little body off the ground. \
The bee, of course, flies anyway \
because bees don't care \
what humans think is impossible. \
Yellow, black. Yellow, black. \
Yellow, black. Yellow, black. \
Ooh, black and yellow! \
Let's shake it up a little. \
Barry! Breakfast is ready! \
Coming! \
Hang on a second. \
Hello? \
Barry? \
Adam? \
Can you believe this is happening? \
I can't. I'll pick you up. \
Looking sharp. \
Use the stairs. Your father \
paid good money for those. \
Sorry. I'm excited. \
Here's the graduate. \
We're very proud of you, son. \
A perfect report card, all B's. \
Very proud. \
Ma! I got a thing going here. \
You got lint on your fuzz. \
Ow! That's me! \
Wave to us! We'll be in row 118,000. \
Bye!"

# Code adapted from https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/
# Sets up the Wiimote Connection
# Returns an instance of the wiimote
def connectToWiimote():
    print("Press 1+2 on your Wiimote to connect...")
    wm = None
    i = 1
    while not wm:
        try:
            wm = cwiid.Wiimote()
        except RuntimeError:
            if i > 10:
                quit()
                break
            print("Error connecting, please try again...")
            print("Connection attempt " + str(i))
            i += 1
    print("Connected to Wiimote!")

    wm.led = 1
    return wm

# Converts a string to morse code
# Takes in the string to be converted
def convertToMorse(str):
    str = str.lower()
    finalStr = ""
    for i in str:
        finalStr += morseDict.get(i, "") + " "
    resultArr = finalStr.split(" ")
    return resultArr

# Converts morse code to rumble
# Takes in the wiimote object, an array of words
#   Plus the string, if you want to show the words
def morseToRumble(wm, wordArr, str=""):
    index = 0
    for word in wordArr:
        for i in word:
            if i == ',':
                time.sleep(0.1)
            else:
                wm.rumble = True
                time.sleep(0.1)
                if i == '-':
                    time.sleep(0.2)
                wm.rumble = False
                time.sleep(0.1)
        if index < len(str):
            sys.stdout.write(str[index])
            sys.stdout.flush()
        index += 1
        time.sleep(0.2)

# Runs the program with a string
def run(str):
    wm = connectToWiimote()
    arr = convertToMorse(str)
    morseToRumble(wm, arr, str)

run(beeMovieScript)
