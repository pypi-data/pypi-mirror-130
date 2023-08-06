import pyautogui
import time

pyautogui.FAILSAFE = False


class Mouse(object):
    def __init__(self):
        super()

    def mouseClick(self,
                   count, Time=1, isdoubleclick=True, x=None, y=None, button='left', istripleClick=False):
        c = 0
        while c < count:
            if isdoubleclick:
                pyautogui.doubleClick(x=x, y=y, button=button)
            elif isdoubleclick == False:
                pyautogui.click(x=x, y=y, button=button)
            else:
                pyautogui.tripleClick(x, y, button=button)
            c += 1
            print(c)
            time.sleep(Time)

    def getMouseXY(self):
        try:
            return pyautogui.position()
        except Exception as e:
            print(repr(e))

    def MoveTo(self, x, y, duration=0.25):
        pyautogui.moveTo(x=x, y=y, duration=duration)

    def dragTo(self, x, y, button='left', duration=1):
        pyautogui.dragTo(x, y, duration=duration, button=button)


def prees(key, count, Time=1, ishotkey=False, isprees=True, iskeyUp=False, iskeyDown=False, istypewrite=False):
    c = 0
    while c < count:
        if isprees:
            pyautogui.press(key)
        elif ishotkey:
            pyautogui.hotkey(key)
        elif iskeyUp:
            pyautogui.keyUp(key)
        elif iskeyDown:
            pyautogui.keyDown(key)
        elif istypewrite:
            pyautogui.typewrite(key)
        time.sleep(Time)
        c += 1
