#!/usr/bin/python3
import random as randint
import pyscreenshot as image_grab
import pyautogui
import time


class PixelPosition(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Color(object):
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

    def isEqualsTo(self, color) -> bool:
        return color.r == self.r and color.g == self.g and color.b == self.b


class Perception(object):
    def __init__(self, image):
        self.image = image

    def colorPointPrint(self, position: PixelPosition) -> Color:
        color = self.image.getpixel((position.x, position.y))
        return Color(color[0], color[1], color[2])


class BuilderPerception(object):
    def buildNewPerception(self) -> Perception:
        return Perception(image=image_grab.grab())


class Trigger(object):
    def isFiring(self, perception: Perception) -> bool:
        pass


class Action(object):
    def __init__(self, _finally=None):
        self._finally = _finally

    @staticmethod
    def exec(action):
        action._execMainAction()
        if action._finally:
            Action.exec(action._finally)

    def _execMainAction(self):
        pass


class TriggerAndAction(object):
    def __init__(self, trigger: Trigger, action: Action):
        self.trigger = trigger
        self.action = action


class Bot(object):
    def __init__(self,
                 triggersAndActions: list,
                 stepIntervalMilliseconds: int,
                 builderPerception: BuilderPerception):
        self.triggersAndActions = triggersAndActions
        self.stepIntervalMilliseconds = stepIntervalMilliseconds
        self.builderPerception = builderPerception

        self.running = False

    def run(self):
        self.running = True
        while(self.running):
            print("stap")
            perception = self.builderPerception.buildNewPerception()
            for triggerAndAction in self.triggersAndActions:
                if triggerAndAction.trigger.isFiring(perception):
                    Action.exec(triggerAndAction.action)
                    break
            time.sleep(self.stepIntervalMilliseconds/1000)

    def stop(self):
        self.running = False


class TriggerPrintPoint(Trigger):
    def __init__(self, position: PixelPosition, color: Color):
        self.position = position
        self.color = color

    def isFiring(self, perception: Perception) -> bool:
        c = perception.colorPointPrint(self.position)
        print(c.isEqualsTo(self.color))
        return c.isEqualsTo(self.color)


class TriggerPrintArea(Trigger):
    def __init__(self, topLeft: PixelPosition, bottomRight: PixelPosition, coloringArea: list):
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        self.coloringArea = coloringArea

    def isFiring(self, perception: Perception) -> bool:
        for i in range(self.topLeft.x, self.bottomRight.x):
            for j in range(self.topLeft.y, self.bottomRight.y):
                c = perception.colorPointPrint(PixelPosition(x=i, y=j))
                if not c.isEqualsTo(self.coloringArea[i][j]):
                    return False
        return True


class TriggerCompound(Trigger):
    def __init__(self, triggersSet: list):
        self.triggersSet = triggersSet

    def isFiring(self, perception: Perception) -> bool:
        for trigger in self.triggersSet:
            if not trigger.isFiring(perception=perception):
                return False
        return True


class ActionClick(Action):
    def __init__(self, _finally=None):
        super().__init__(_finally=_finally)

    def _execMainAction(self):
        pyautogui.click()


class ActionWaitDuration(Action):
    def __init__(self, durationMilliseconds, _finally=None):
        super().__init__(_finally=_finally)
        self.durationMilliseconds = durationMilliseconds

    def _execMainAction(self):
        time.sleep(self.durationMilliseconds/1000)


class ActionCompound(Action):
    def __init__(self, actionSequence: list, _finally=None):
        super().__init__(_finally=_finally)
        self.actionSequence = actionSequence

    def _execMainAction(self):
        for action in self.actionSequence:
            Action.exec(action)


class ActionScrollMove(Action):
    def __init__(self, scrollMove, _finally=None):
        super().__init__(_finally=_finally)
        self.scrollMove = scrollMove

    def _execMainAction(self):
        pyautogui.scroll(self.scrollMove)


class ActionMouseMove(Action):
    def __init__(self, aim: PixelPosition, durationMoveMilliseconds=300, _finally=None):
        super().__init__(_finally=_finally)
        self.aim = aim
        self.durationMoveMilliseconds = durationMoveMilliseconds

    def _execMainAction(self):
        pyautogui.moveTo(
            self.aim.x,
            self.aim.y,
            duration=self.durationMoveMilliseconds / 1000,
            tween=pyautogui.easeInOutQuad,
        )


class ActionMouseDragTo(Action):
    def __init__(self, aim: PixelPosition, durationMoveMilliseconds=300, _finally=None):
        super().__init__(_finally=_finally)
        self.aim = aim
        self.durationMoveMilliseconds = durationMoveMilliseconds

    def _execMainAction(self):
        pyautogui.dragTo(
            self.aim.x,
            self.aim.y,
            duration=self.durationMoveMilliseconds / 1000,
            tween=pyautogui.easeInOutQuad,
            button='left'
        )


class ActionCode(Action):
    def __init__(self, code=lambda: 0, _finally=None):
        super().__init__(_finally=_finally)
        self.code = code

    def _execMainAction(self):
        self.code()
