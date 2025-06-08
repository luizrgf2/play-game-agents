import pyautogui
from langchain.tools import tool


def screenshot_tool():
    '''
        Essa ferrementa serve para tirar screenshot da janela do game
    '''

    screenshot = pyautogui.screenshot()
    screenshot.save("capture.png")
    print("Screenshot salva como captura_tela.png")