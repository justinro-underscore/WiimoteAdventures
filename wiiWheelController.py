import cwiid
import time
import math
import random
import pyautogui

# Turns the wiimote into a steering wheel (just like Mario Kart!)
class WiiWheelController:
  def __init__(self, pitchThreshold, debug=False):
    self.pitchThreshold = pitchThreshold # Determines the threshold for the pitch
    self.debug = debug # If true, show debug statements rather than 

  # Code adapted from https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/
  # Sets up the Wiimote Connection
  # Returns an instance of the wiimote
  def connectToWiimote(self):
    print("Press 1+2 on your Wiimote to connect...")
    self.wm = None
    i = 1
    while not self.wm:
      try:
        self.wm = cwiid.Wiimote()
      except RuntimeError:
        if i > 10:
          quit()
          break
        print("Error connecting, please try again...")
        print("Connection attempt " + str(i))
        i += 1
    print("Connected to Wiimote!")
    self.wm.led = 15 # Show that we are connected

  # Presses a direction key (either key up or key down)
  # direction can be ['left', 'right', 'up', 'down']
  def _key(self, direction, keyDown):
    if self.debug:
      print('keyDown' if keyDown else 'keyUp' + ' ' + direction)
    else:
      pyautogui.keyDown(direction) if keyDown else pyautogui.keyUp(direction)

  # Presses a direction key down
  def keyDown(self, direction): self._key(direction, True)

  # Presses a direction key up
  def keyUp(self, direction): self._key(direction, False)

  # Checks the pitch of the wiimote to determine which direction to steer
  def checkSteering(self):
    pitch = self.wm.state['acc'][1] - 125
    # Steer left
    if pitch < -self.pitchThreshold:
      if self.steerDir != -1:
        if self.steerDir == -1:
          self.keyUp('left')
        self.steerDir = -1
        self.keyDown('right')
    # Steer right
    elif pitch > self.pitchThreshold:
      if self.steerDir != 1:
        if self.steerDir == 1:
          self.keyUp('right')
        self.steerDir = 1
        self.keyDown('left')
    # Steer straight
    else:
      if self.steerDir != 0:
        if self.steerDir == 1:
          self.keyUp('left')
        elif self.steerDir == -1:
          self.keyUp('right')
        self.steerDir = 0

  # Checks the 2 and A buttons of the wiimote to determine which direction to accelerate
  # 2 goes forward
  # A goes back
  # Pressing both causes the car to stop
  def checkAcceleration(self):
    buttonsRaw = self.wm.state['buttons']
    buttons = [buttonsRaw & cwiid.BTN_2, buttonsRaw & cwiid.BTN_A] # [0] is forward, [1] is back

    # Stops the car
    def reset():
      if self.accelDir != 0:
        if self.accelDir == 1:
          self.keyUp('up')
        elif self.accelDir == -1:
          self.keyUp('down')
        self.accelDir = 0

    # Stop the car if both buttons pressed
    if buttons[0] == buttons[1]:
      reset()
    # Go forward
    elif buttons[0]:
      if self.accelDir != 1:
        self.accelDir = 1
        self.keyDown('up')
    # Go backwards
    elif buttons[1]:
      if self.accelDir != -1:
        self.accelDir = -1
        self.keyDown('down')

  # Runs the program
  def run(self):
    self.connectToWiimote()
    self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    time.sleep(0.01) # Let the system boot up

    self.steerDir = 0 # Direction to steer (-1 is left, 1 is right)
    self.accelDir = 0 # Direction to accelerate (-1 is back, 1 is forwards)
    while True:
      self.checkSteering()
      self.checkAcceleration()
      time.sleep(0.01)

# Run it!
controller = WiiWheelController(8)
controller.run()
