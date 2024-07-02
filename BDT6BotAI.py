from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
from enum import Enum

class PlacableTower(Enum):
    Dart_Monkey = 0
    Bomb_Shooter = 1
    Sniper_Monkey = 2
    Wizard_Monkey = 3
    Ninja_Monkey = 4
    Druid_Monkey = 5

class TowerCard():
    def __init__(self, type: PlacableTower, cords, scrollAmount, colorInt, colorAmount, colorCheckOffset):
        self.type = type
        self.cords = cords
        self.scrollAmount = scrollAmount
        self.colorInt = colorInt
        self.colorAmount = colorAmount
        self.colorCheckOffset = colorCheckOffset

placableTowers = []
placableTowers.append(TowerCard(PlacableTower.Dart_Monkey, [1791, 178], 0, 2, 200, 0))
placableTowers.append(TowerCard(PlacableTower.Bomb_Shooter, [1865, 305], 0, 2, 200, -50))
placableTowers.append(TowerCard(PlacableTower.Sniper_Monkey, [1786, 586], 0, 1, 200, 5))



class Tower():
    def __init__(self, cords):
        self.cords = cords
        self.upgrades = [0, 0, 0]
    def upgraded(self, upgradePath):
        self.upgrades[upgradePath] += 1
        

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

def cantPlaceTower(zOffset):
    x, y = win32api.GetCursorPos()
    if (pyautogui.pixel(x, y + zOffset)[2] == 255):
        return False
    else:
        return True

def canBuyTower(towerPlacing: TowerCard):
    if (pyautogui.pixel(towerPlacing.cords[0], towerPlacing.cords[1])[towerPlacing.colorInt] >= towerPlacing.colorAmount):
        click(towerPlacing.cords[0], towerPlacing.cords[1])
        win32api.SetCursorPos((random.randint(minX, maxX), random.randint(minY, maxY)))
        placeTower(towerPlacing)
        return True
    return False

def selectTower():
    towerPlacing = random.choice(placableTowers)
    print(f"Trying to place {towerPlacing.type}")
    roundActive = True  
    placed = False
    while roundActive and not placed:
        placed = canBuyTower(towerPlacing)
        if (roundReadyToStart()):
            roundActive = False
            placed = canBuyTower(towerPlacing)
        

def placeTower(towerPlacing: TowerCard):
    tries = 0
    maxTries = 20
    while cantPlaceTower(towerPlacing.colorCheckOffset) and tries < maxTries:
        win32api.SetCursorPos((random.randint(minX, maxX), random.randint(minY, maxY)))
        time.sleep(0.3)
        tries += 1
    if (tries >= maxTries):
        print("UNABLE TO PLACE MONKEY")
        time.sleep(1)
    else:
        click(cursorX(), cursorY())
        towers.append(Tower([cursorX(), cursorY()]))

def upgradeTower():
    tower = random.choice(towers)
    cords = tower.cords
    xLocations = [270, 1490]
    allYLocations = [480, 620, 780]
    yLocations = [x for x in allYLocations]
    x = 0
    y = 0
    click(cords[0], cords[1])
    if (pyautogui.pixel(60, 155)[2] == 255):
        print("Left Upgrade Menu Open")
        x = xLocations[0]
    elif (pyautogui.pixel(1280, 155)[2] == 255):
        print("Right Upgrade Menu Open")
        x = xLocations[1]
    else:
        print("NO UPGRADE MENU OPENED")
        time.sleep(5)
        return
    
    # Removes certain y location due to upgrade path closing
    towerUpgrades = tower.upgrades
    print(towerUpgrades)
    maxUpgrade = max(towerUpgrades)
    if (maxUpgrade >= 3 and 2 in towerUpgrades):
        yLocations = [yLocations[towerUpgrades.index(maxUpgrade)]]
    elif (towerUpgrades.count(0) == 1):
        yLocations.pop(towerUpgrades.index(0))

    y = random.choice(yLocations)
    upgrade = allYLocations.index(y)
    print(f"Upgrading path {upgrade + 1}")
    roundActive = True  
    upgraded = False
    while roundActive and not upgraded:
        upgraded = tryUpgrade(x, y, tower, upgrade)
        if (roundReadyToStart()):
            roundActive = False
            upgraded = tryUpgrade(x, y, tower, upgrade)
    keyboard.press('esc')
    time.sleep(0.1)
    keyboard.release('esc')
    time.sleep(0.1)

def tryUpgrade(x, y, tower: Tower, upgrade):
    if (pyautogui.pixel(x, y)[1] >= 220):
            click(x, y, 1)
            tower.upgraded(upgrade)
            print("Upgraded")
            return True
    return False

minX = 338
maxX = 1296
minY = 350
maxY = 826

wave = 0
placeTowerChance = 1 # Between 0 and 1

towers = []

# Main function loop
while True:
    print("Deciding What to Do")
    if (random.random() <= placeTowerChance):
        selectTower()
    else:
        upgradeTower()
    
    if (roundReadyToStart()):
        startRound()
        if (wave == 0):
            click(1824, 994)
        wave += 1
        if (wave % 2 == 0):
            placeTowerChance *= 0.9
            print(f"Place Tower Chance: {round(placeTowerChance, 2)}")