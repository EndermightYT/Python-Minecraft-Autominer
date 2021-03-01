import pyautogui, sys
import keyboard
from pynput.keyboard import Key, Controller
import time as t
import random
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput
pyautogui.FAILSAFE = False

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def InvSwitch(hexKeyCode):
    PressKey(hexKeyCode)
    ReleaseKey(hexKeyCode)

def Jump():
    PressKey(0x39)
    t.sleep(0.2)
    ReleaseKey(0x39)
    
def walk():
    PressKey(0x11)
    Jump()
    t.sleep(1)
    ReleaseKey(0x11)

def CursorPos():
    x, y = pyautogui.position()
    positionStr = "X: " + str(x).rjust(4) + " Y: " + str(y).rjust(4)
    print(positionStr, end="")
    print("\b" * len(positionStr), end="", flush=True)   

def Stackdrop():
    t.sleep(0.2)
    PressKey(0x1D)
    PressKey(0x10)
    t.sleep(0.2)
    ReleaseKey(0x10)
    ReleaseKey(0x1D)

def DropLast3():
    pyautogui.mouseDown()
    t.sleep(1)
    pyautogui.mouseUp()
    InvSwitch(0x08)
    Stackdrop()
    InvSwitch(0x09)
    Stackdrop()
    InvSwitch(0x0A)
    Stackdrop()
    pyautogui.move(0, 60,  0.3)
    

def doubleRight():
    pyautogui.click(button="right")
    t.sleep(0.3)
    pyautogui.click(button="right")

def Bucket():
    pyautogui.mouseUp()
    InvSwitch(0x04)
    t.sleep(0.1)
    pyautogui.click(button="right")
    t.sleep(0.3)
    pyautogui.click(button="right")
    InvSwitch(0x03)
    pyautogui.mouseDown()

def Torch():
    pyautogui.move(0, -295,  0.3)
    pyautogui.mouseDown()
    t.sleep(1)
    pyautogui.mouseUp()
    InvSwitch(0x06)
    t.sleep(0.3)
    pyautogui.click(button="right")
    t.sleep(0.5)
    InvSwitch(0x03)
    pyautogui.move(0, 270,  0.3)

def BuildUp(length):
    for i in range(length):
        InvSwitch(0x03)
        pyautogui.move(0, -600,  0.4,pyautogui.easeInQuad)
        pyautogui.mouseDown()
        t.sleep(1)
        pyautogui.mouseUp()
        pyautogui.move(0, 600,  0.4,pyautogui.easeInQuad)
        InvSwitch(0x07)
        Jump()
        doubleRight()
        Jump()
        doubleRight()
        t.sleep(0.3)
        InvSwitch(0x03)
        t.sleep(0.5)
    pyautogui.move(0, -400,  0.3)
    pyautogui.move(0, 270,  0.3)

def Positioning():
    pyautogui.move(0, -300,  0.3)
    pyautogui.move(0, 270,  0.3)

def Turn(drop,build):
    pyautogui.move(600, 0,  0.3, pyautogui.easeInQuad)
    if drop == 1:
        DropLast3()
    if build == 1:
        InvSwitch(0x07)
        doubleRight()
        InvSwitch(0x03)
    t.sleep(0.3)
    pyautogui.move(295*random.choice(minusplus), 0,  0.3, pyautogui.easeInQuad)
    
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def Mining(length):
    pyautogui.mouseDown()
    for i in range(random.randint(1, length)):
        if keyboard.is_pressed("p"):
            exit(0)
        t.sleep(0.3)
        pyautogui.move(0, -10,  0.3, pyautogui.easeInQuad)
        pyautogui.move(60*random.choice(minusplus), 0,  0.3, pyautogui.easeInQuad)
        walk()
    pyautogui.mouseUp()

def Eat():
    InvSwitch(0x05)
    pyautogui.mouseDown(button="right")
    t.sleep(2)
    pyautogui.mouseUp(button="right")
    t.sleep(0.4)
    InvSwitch(0x03)

t.sleep(4)
minusplus = [-1,1]
k = Controller()
try:
    while True:
        t.sleep(1)
        BuildUp(6)
        Eat()
        Positioning()
        for i in range(20):
            Mining(30)
            Turn(1,1)
            Torch()     
except KeyboardInterrupt:
    print("Code stopped")
