from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

def cursorX():
    x, y = win32api.GetCursorPos()
    return x

def cursorY():
    x, y = win32api.GetCursorPos()
    return y

def click(x, y, pause=0.5):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(pause)

def roundReadyToStart():
    if (pyautogui.pixel(1824, 994)[2] == 255):
        return True
    else:
        return False

def startRound():
    if (roundReadyToStart()):
        click(1824, 994)
        time.sleep(0.5)
    else:
        print("Can't start round")

def cantPlaceTower():
    x, y = win32api.GetCursorPos()
    if (pyautogui.pixel(x, y)[2] == 255):
        return False
    else:
        return True

def placeTower():
    tries = 0
    maxTries = 10
    while cantPlaceTower() and tries < maxTries:
        win32api.SetCursorPos((random.randint(minX, maxX), random.randint(minY, maxY)))
        time.sleep(0.5)
        tries += 1
    if (tries >= maxTries):
        print("UNABLE TO PLACE MONKEY")
        time.sleep(5)
    else:
        click(cursorX(), cursorY())

minX = 90
maxX = 1550
minY = 100
maxY = 1000

while True:
    if (roundReadyToStart()):
        startRound()

    if (pyautogui.pixel(1791, 178)[2] >= 200):
        click(1791, 178)
        win32api.SetCursorPos((random.randint(minX, maxX), random.randint(minY, maxY)))
        placeTower()
    