import pyautogui


def screenshot_tool():
    screenshot = pyautogui.screenshot()
    screenshot.save("capture.png")
    print("Screenshot salva como captura_tela.png")