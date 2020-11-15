#!/usr/bin/python3
import random as randint
import pyscreenshot as ImageGrab
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
        return Perception(image=ImageGrab.grab())


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
            exec(action._finally)

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
            exec(action)


class ActionScrollMove(Action):
    def __init__(self, scrollMove, _finally=None):
        super().__init__(_finally=_finally)
        self.scrollMove = scrollMove

    def _execMainAction(self):
        pyautogui.scroll(self.scrollMove)


class ActionMouseMove(Action):
    def __init__(self, aim: PixelPosition, durationMoveMilliseconds=100, _finally=None):
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


bot = Bot(
    triggersAndActions=[
        TriggerAndAction(
            trigger=TriggerPrintPoint(
                position=PixelPosition(x=0, y=0),
                color=Color(r=0, g=0, b=0),
            ),
            action=ActionMouseMove(aim=PixelPosition(x=100, y=100)),
        ),
    ],
    stepIntervalMilliseconds=2000,
    builderPerception=BuilderPerception()
)

bot.run()

"""
def printPexel(x, y):
    time.sleep(5)
    print("color:", ImageGrab.grab().getpixel((x, y)))


def printMousePositionPixel():
    coodenadas = pyautogui.position()
    print("position:", coodenadas)
    time.sleep(5)
    print("color:", ImageGrab.grab().getpixel(coodenadas))

# printMousePositionPixel()


def getPixel(image, coodenadas):
    return image.getpixel(coodenadas)


def clickIn(coodenadas):
    print("click", coodenadas)
    pyautogui.moveTo(coodenadas)
    pyautogui.click()


def delay(secunds):
    time.sleep(secunds)


def printScreen():
    return ImageGrab.grab()


def closePopupMoreSpin(image):
    color1 = r, g, b = 240, 188, 3
    colorBtnClose = r, g, b = 255, 255, 255

    coodenada1 = x, y = 383, 244
    coodenadaBtnClose = x, y = 625, 439
    ehUmAnuncio = color1 == getPixel(
        image, coodenada1) and colorBtnClose == getPixel(image, coodenadaBtnClose)
    if ehUmAnuncio:
        print("Fechando Popup de Spin Esgotados")
        clickIn(coodenadaBtnClose)
        delay(1)
        return True
    return False


def closePopupReivindicacao(image):
    color1 = r, g, b = 165, 220, 134
    colorBtnClose = r, g, b = 124, 209, 249

    coodenada1 = x, y = 402, 269
    coodenadaBtnClose = x, y = 432, 427
    ehUmAnuncio = color1 == getPixel(
        image, coodenada1) and colorBtnClose == getPixel(image, coodenadaBtnClose)
    if ehUmAnuncio:
        print("Fechando Popup de Reivendicao")
        clickIn(coodenadaBtnClose)
        delay(1)
        return True
    return False


def closeAd(image):
    color1 = r, g, b = 255, 255, 255
    colorBtnClose = r, g, b = 0, 0, 0

    coodenada1 = x, y = 106, 175
    coodenadaBtnClose = x, y = 100, 177
    ehUmAnuncio = (color1 == getPixel(image, coodenada1)
                   and colorBtnClose == getPixel(image, coodenadaBtnClose))
    if ehUmAnuncio:
        print("Fechando Anuncio")
        clickIn(coodenadaBtnClose)
        delay(1)
        return True
    return False


def closeTab(image):
    colorBtnClose = r, g, b = 146, 149, 152

    coodenadaBtnClose = x, y = 434, 46
    outraAbaAberta = colorBtnClose == getPixel(image, coodenadaBtnClose)
    if outraAbaAberta:
        print("Fechando Aba de Anuncio")
        clickIn(coodenadaBtnClose)
        delay(1)
        return True
    return False


def closeWindow(image):
    color1 = r, g, b = 57, 103, 181
    color2 = r, g, b = 245, 246, 247
    colorBtnClose = r, g, b = 211, 218, 227

    coodenada1 = x, y = 14, 14
    coodenada2 = x, y = 14, 39
    coodenadaBtnClose = x, y = 786, 17

    outraJanelaAberta = color1 == getPixel(image, coodenada1) and color2 == getPixel(
        image, coodenada2) and colorBtnClose == getPixel(image, coodenadaBtnClose)
    if outraJanelaAberta:
        print("Fechando Janela de Anuncio")
        clickIn(coodenadaBtnClose)
        delay(1)
        return True
    return False


def reivendicarSpins(image):
    color1 = r, g, b = 1, 92, 195
    colorBotao = r, g, b = 92, 184, 92

    coodenada1 = x, y = 395, 455
    coodenadaBotao = x, y = 394, 483

    naoEhUmaPopup = color1 == getPixel(image, coodenada1)

    botaoParaReclamarApareceu = naoEhUmaPopup and colorBotao == getPixel(
        image, coodenadaBotao)
    if botaoParaReclamarApareceu:
        print("Clicando em Reivendicar Spins")
        clickIn(coodenadaBotao)
        return True
    return False


def abrirBau(image):
    color1 = r, g, b = 255, 197, 20
    colorBotao = r, g, b = 213, 129, 0

    coodenada1 = x, y = 434, 440
    coodenadaBotao = x, y = 286, 452

    bauApareceu = color1 == getPixel(
        image, coodenada1) and colorBotao == getPixel(image, coodenadaBotao)
    if bauApareceu:
        print("Clicando para Abrir Bau")
        clickIn(coodenadaBotao)
        return True
    return False


def escolherVermelhoOuPreto(image):
    colorVermelho = r, g, b = 226, 0, 0
    colorPreto = r, g, b = 0, 0, 0

    coodenada1 = x, y = 366, 461
    coodenadaBotaoVermelho = x, y = 341, 520
    coodenadaBotaoPreto = x, y = 523, 523

    vermelhoOuPretoApareceu = (colorVermelho == getPixel(image, coodenada1) or colorPreto == getPixel(
        image, coodenada1)) and colorVermelho == getPixel(image, coodenadaBotaoVermelho) and colorPreto == getPixel(image, coodenadaBotaoPreto)
    if vermelhoOuPretoApareceu:
        print("Clicando para Escolher Vermelho ou Preto")
        random.seed()
        if random.randint(0, 10) < 5:
            clickIn(coodenadaBotaoVermelho)
        else:
            clickIn(coodenadaBotaoPreto)

        return True
    return False


def playFancy(image):
    color = r, g, b = 255, 0, 129

    coodenada = x, y = 434, 481
    btnEstaAtivo = color == getPixel(image, coodenada)
    if btnEstaAtivo:
        print("Clicando em PlayFancy")
        clickIn(coodenada)
        return True
    return False


def refresh(image):
    coodenada = x, y = 86, 82
    clickIn(coodenada)
    delay(3)
    clickIn(coodenada)


def main():
    print("\riniciara em 5s...")
    delay(1)
    print("\riniciara em 4s...")
    delay(1)
    print("\riniciara em 3s...")
    delay(1)
    print("\riniciara em 2s...")
    delay(1)
    print("\riniciara em 1s...")
    delay(1)
    print("\riniciado.")
    reivindicadoPorUltimo = time.time()-900
    playFancyPorUltimo = time.time()-900
    while True:
        image = printScreen()
        closedWindow = closeWindow(image)
        closedTab = closeTab(image)
        closedAd = closeAd(image)
        closedPopupReivindicacao = closePopupReivindicacao(image)
        closedPopupMoreSpin = closePopupMoreSpin(image)
        if not (closedPopupReivindicacao or closedPopupMoreSpin or closedAd or closedTab or closedWindow):
            tempoAtual = time.time()
            if tempoAtual - reivindicadoPorUltimo >= 60:
                reivindicadoPorUltimo = time.time()
                print("conferindo reivindicacao, decorrido:",
                      int(tempoAtual - reivindicadoPorUltimo))

                pyautogui.moveTo(786, 500)
                pyautogui.scroll(-3)
                delay(.9)
                image = printScreen()
                reivendicarSpins(image)
                pyautogui.scroll(3)
                delay(.5)
                image = printScreen()

            abrirBau(image)
            escolherVermelhoOuPreto(image)
            tempoAtual = time.time()
            if playFancy(image):
                playFancyPorUltimo = tempoAtual
            elif tempoAtual - playFancyPorUltimo >= 60 and tempoAtual - reivindicadoPorUltimo >= 30:
                refresh(image)
                playFancyPorUltimo = playFancyPorUltimo + 1800

        delay(1)


main()
"""
