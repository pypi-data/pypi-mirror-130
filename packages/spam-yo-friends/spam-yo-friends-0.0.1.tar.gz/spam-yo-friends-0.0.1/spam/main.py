import keyboard  # using module keyboard
import pyautogui
import questionary
import os
from time import *


def Spam():
    clear = lambda: os.system('cls')
    method = questionary.select("What spamming method do you want to use?", choices=["WhatsApp", "Discord"]).ask()
    message = questionary.text("What message do you want to spam with?").ask()

    allright = questionary.confirm(f"\nSpamming Method: {method}\nMessage: {message}\nIs this all right?").ask()

    if allright == False:
        clear()
        exit()

    if method == "WhatsApp":
        print(f'Spamming will start in 8 seconds! Press F3 at any time to stop spamming!')
        sleep(8)
        while True:  # making a loop
            try:  # used try so that if user pressed other than the given key error will not be shown

                    pyautogui.typewrite(message)
                    pyautogui.press('enter')
                    if keyboard.is_pressed('f3'):  # if key 'q' is pressed 
                        print('Stopped spamming...')
                        clear()
                        break  # finishing the loop                    
            except:
                break  # if user pressed a key other than the given key the loop will break
    elif method == "Discord":
        print(f'Spamming will start in 8 seconds! Press F3 at any time to stop spamming! (You may need to hold it for a bit!)')
        sleep(8)
        while True:  # making a loop
            try:  # used try so that if user pressed other than the given key error will not be shown
                    if keyboard.is_pressed('f3'):  # if key 'q' is pressed 
                        print('Stopped spamming...')
                        clear()
                        exit()  # finishing the loop                    
                    sleep(.5)
                    pyautogui.typewrite(message)
                    pyautogui.press('enter')
            except:
                break  # if user pressed a key other than the given key the loop will break

def SpamDontSend():
    clear = lambda: os.system('cls')
    method = questionary.select("What spamming method do you want to use?", choices=["WhatsApp", "Discord"]).ask()
    message = questionary.text("What message do you want to spam with?").ask()

    allright = questionary.confirm(f"\nSpamming Method: {method}\nMessage: {message}\nIs this all right?").ask()

    if allright == False:
        clear()
        exit()

    if method == "WhatsApp":
        print(f'Spamming will start in 8 seconds! Press F3 at any time to stop spamming!')
        sleep(8)
        while True:  # making a loop
            try:  # used try so that if user pressed other than the given key error will not be shown

                    pyautogui.typewrite(message)
                    if keyboard.is_pressed('f3'):  # if key 'q' is pressed 
                        print('Stopped spamming...')
                        clear()
                        break  # finishing the loop                    
            except:
                break  # if user pressed a key other than the given key the loop will break
    elif method == "Discord":
        print(f'Spamming will start in 8 seconds! Press F3 at any time to stop spamming! (You may need to hold it for a bit!)')
        sleep(8)
        while True:  # making a loop
            try:  # used try so that if user pressed other than the given key error will not be shown
                    if keyboard.is_pressed('f3'):  # if key 'q' is pressed 
                        print('Stopped spamming...')
                        clear()
                        exit()  # finishing the loop                    
                    sleep(.5)
                    pyautogui.typewrite(message)
            except:
                break  # if user pressed a key other than the given key the loop will break