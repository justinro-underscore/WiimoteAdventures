# Makes the Wiimote into a lightsaber
# Makes lightsaber noises when you swing it around

###########################
##  HOW TO MAKE IT WORK  ##
###########################

# Simply run python3 lightsaberRunner.py in your terminal of choice, then press buttons
#   1 + 2 on the wiimote to connect. Once connected, all the LEDs should turn on.
#   Press 'B' to activate/deactivate the lightsaber, press 'A' to hit things, and
#   swing the lightsaber wildly to make "waa waa" noises

import cwiid
import time
import math
import random
import pygame

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

    wm.led = 15 # Obviously we can't have a real light saber, so these lights will have to do
    return wm

# Sets up the sounds for use with the lightsaber
# Sounds retreived from JoshHarrisVFX https://www.youtube.com/watch?v=odZUuVfv8Ko
# The variable sounds would work much better as a global variable but that would involve
#   setting up pygame before everything else and that seems like a bad practice.
#   This whole setup should probably be cleaned up and refactored but I don't care
#   too much about the cleanliness of this project
def setUpSounds():
    # Initialize pygame
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()
    sounds = {
        "open": pygame.mixer.Sound("Lightsaber_Sounds/open.wav"),
        "medHum": pygame.mixer.Sound("Lightsaber_Sounds/medHum.wav"),
        "close": pygame.mixer.Sound("Lightsaber_Sounds/close.wav"),
        "heavySwing1": pygame.mixer.Sound("Lightsaber_Sounds/heavySwing1.wav"),
        "heavySwing2": pygame.mixer.Sound("Lightsaber_Sounds/heavySwing2.wav"),
        "lightSwing1": pygame.mixer.Sound("Lightsaber_Sounds/lightSwing1.wav"),
        "lightSwing2": pygame.mixer.Sound("Lightsaber_Sounds/lightSwing2.wav"),
        "hit1": pygame.mixer.Sound("Lightsaber_Sounds/hit1.wav"),
        "hit2": pygame.mixer.Sound("Lightsaber_Sounds/hit2.wav"),
    }
    return sounds

# Gets the magnitude of the coordinates passed in
def getMagnitude(x, y, z):
    x_2 = math.pow(x, 2)
    y_2 = math.pow(y, 2)
    z_2 = math.pow(z, 2)
    mag = math.sqrt(x_2 + y_2 + z_2)
    return mag

# Checks the buttons of the wiimote
# Takes in the buttons byteword, buttonStates which tells whether or not a button
#   is being pressed or not, activated - a boolean which tells whether or not the
#   lightsaber is activated, and sounds, the dictionary from before
def checkButtons(buttons, buttonStates, activated, sounds):
    # B button handles turning on and off the lightsaber
    if buttons & cwiid.BTN_B:
        if not buttonStates['b']:
            activated = not activated
            if activated:
                sounds["open"].play()
                sounds["medHum"].set_volume(0.5)
                sounds["medHum"].play(-1, 0, 2000)
            else:
                sounds["medHum"].fadeout(1000)
                sounds["close"].play()
            buttonStates['b'] = True
    elif buttonStates['b']: # Handles the button being pressed down
        buttonStates['b'] = False

    # A buttons handles the hit sound (because I can't actually make it detect
    #   when it hits things)
    if buttons & cwiid.BTN_A:
        if not buttonStates['a']:
            num = random.randint(1, 3)
            if num == 1:
                sounds["hit1"].play()
            else:
                sounds["hit2"].play()
            buttonStates['a'] = True
    elif buttonStates['a']:
        buttonStates['a'] = False

    return buttonStates, activated

# Checks if we should do anything with the accelerometer
# Takes in the accelerometer data, the old magnitude, and the sounds dict
def checkAcc(acc, oldMag, sounds):
    newMag = getMagnitude(acc[0], acc[1], acc[2])
    checkMag = newMag - oldMag
    if checkMag > 60: # If its a large swing
        num = random.randint(1, 3)
        if num == 1:
            sounds["heavySwing1"].play()
        else:
            sounds["heavySwing2"].play()
    elif checkMag > 20: # If it's a small swing
        num = random.randint(1, 3)
        if num == 1:
            sounds["lightSwing1"].play()
        else:
            sounds["lightSwing2"].play()
    # print("Mag: {:.2f}".format(math.fabs(newMag - oldMag)))
    return newMag

# Runs the program
def run():
    wm = connectToWiimote()
    wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

    sounds = setUpSounds()

    activated = False
    buttonStates = {
        'a': False,
        'b': False
    }
    oldMag = 0
    counter = 0
    while True:
        buttons = wm.state['buttons']
        bPressed, activated = checkButtons(buttons, buttonStates, activated, sounds)
        if activated and counter >= 20:
            acc = [wm.state['acc'][0], wm.state['acc'][1], wm.state['acc'][2]]
            oldMag = checkAcc(acc, oldMag, sounds)
            counter = 0
        counter += 1
        time.sleep(0.01)

# Run it!
run()
