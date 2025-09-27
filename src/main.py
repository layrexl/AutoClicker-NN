import sys
import threading
from time import sleep
from pyautogui import leftClick, rightClick
from keyboard import wait as keyWait
from pynput.keyboard import Controller
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_nn import Ui_Form

keyboard = Controller()
keysDict = {'Space': keyboard._Key.space, 'Tab': keyboard._Key.tab, 'Caps Lock': keyboard._Key.caps_lock, 'Esc': keyboard._Key.esc, 'F1': keyboard._Key.f1, 'F2': keyboard._Key.f2, 'F3': keyboard._Key.f3, 'F4': keyboard._Key.f4, 'F5': keyboard._Key.f5, 'F6': keyboard._Key.f6, 'F7': keyboard._Key.f7, 'F8': keyboard._Key.f8, 'F9': keyboard._Key.f9, 'F10': keyboard._Key.f10, 'F11': keyboard._Key.f11, 'F12': keyboard._Key.f12}

infinityMain = True
infinity = True
delay = None
delayKeyPressRelease = None

mouseBtn = None
repeats = None
startChoiceBtn = None

keyChoiced = None

def mouseAutoLeftClick():
    if repeats == None:
        while infinity:
            leftClick()
            sleep(delay)
    else:
        for _ in range(0, repeats):
            if infinity == True:
                leftClick()
                sleep(delay)
            else:
                break

def mouseAutoRightClick():
    if repeats == None:
        while infinity:
            rightClick()
            sleep(delay)
    else:
        for _ in range(0, repeats):
            if infinity == True:
                rightClick()
                sleep(delay)
            else:
                break

def mouseAutoClick():
    global infinity

    while infinityMain:
        infinity = True
        keyWait(startChoiceBtn)

        if mouseBtn == 'Left':
            thread = threading.Thread(target=mouseAutoLeftClick)
            thread.start()
        else:
            thread = threading.Thread(target=mouseAutoRightClick)
            thread.start()

        keyWait(startChoiceBtn)
        infinity = False

        sleep(1.5)

def keyboardAutoPress():
    while infinity:
        sleep(delay)

        keyboard.press(keyChoiced)
        sleep(delayKeyPressRelease)
        keyboard.release(keyChoiced)

def keyboardAutoPressMain():
    global infinity

    while infinityMain:
        infinity = True
        keyWait(startChoiceBtn)

        threadMain = threading.Thread(target=keyboardAutoPress)
        threadMain.start()

        keyWait(startChoiceBtn)
        infinity = False

        sleep(2)

class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.startButton.clicked.connect(self.startBtn)
    
    def closeEvent(self, event):
        event.accept()
        raise Exception

    def startBtn(self):
        global delay
        global startChoiceBtn

        global repeats
        global mouseBtn

        global delayKeyPressRelease
        global keyChoiced

        # change status
        self.startButton.setEnabled(False)
        self.statusLabel.setText('Status: Started')
        # ---

        if self.tabWidget.currentWidget().objectName() == 'Mouse':
            # check self.seconds.text()
            try:
                # ',' -> '.'
                scnds = self.seconds.text()
                if list(scnds).count != 0:
                    if ',' in list(scnds):
                        listSeconds = list(scnds)
                        newListSeconds = []
                        for i in listSeconds:
                            if i == ',':
                                newListSeconds.append('.')
                            else:
                                newListSeconds.append(i)
                        scnds = ''.join(newListSeconds)
                # ---        

                delay = float(scnds)
            except Exception:
                sys.exit()
            # ---

            mouseBtn = self.mouseButton.currentText()

            startChoiceBtn = self.startChoiceButton.currentText()

            if self.radioButtonRepeat.isChecked():
                repeats = self.spinBoxRepeat.value()

            threadMain = threading.Thread(target=mouseAutoClick)
            threadMain.start()
        else:
            # check self.betweenKeystrokes.text()
            try:
                # ',' -> '.'
                timeBetweenKeystrokes = self.betweenKeystrokes.text()
                if list(timeBetweenKeystrokes).count != 0:
                    if ',' in list(timeBetweenKeystrokes):
                        listTimeBetweenKeystrokes = list(timeBetweenKeystrokes)
                        newListTimeBetweenKeystrokes = []
                        for i in listTimeBetweenKeystrokes:
                            if i == ',':
                                newListTimeBetweenKeystrokes.append('.')
                            else:
                                newListTimeBetweenKeystrokes.append(i)
                        timeBetweenKeystrokes = ''.join(newListTimeBetweenKeystrokes)
                # ---        

                delay = float(timeBetweenKeystrokes)
            except Exception:
                sys.exit()
            # ---

            # check self.betweenPressRelease.text()
            try:
                # ',' -> '.'
                timeBetweenPressRelease = self.betweenPressRelease.text()
                if list(timeBetweenPressRelease).count != 0:
                    if ',' in list(timeBetweenPressRelease):
                        listTimeBetweenPressRelease = list(timeBetweenPressRelease)
                        newListTimeBetweenPressRelease = []
                        for i in listTimeBetweenPressRelease:
                            if i == ',':
                                newListTimeBetweenPressRelease.append('.')
                            else:
                                newListTimeBetweenPressRelease.append(i)
                        timeBetweenPressRelease = ''.join(newListTimeBetweenPressRelease)
                # ---        

                delayKeyPressRelease = float(timeBetweenPressRelease)
            except Exception:
                sys.exit()
            # ---

            if self.comboBoxKey.currentText() in keysDict:
                keyChoiced = keysDict[self.comboBoxKey.currentText()]
            else:
                keyChoiced = self.comboBoxKey.currentText()

            startChoiceBtn = self.startChoiceButton.currentText()

            threadMain = threading.Thread(target=keyboardAutoPressMain)
            threadMain.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())