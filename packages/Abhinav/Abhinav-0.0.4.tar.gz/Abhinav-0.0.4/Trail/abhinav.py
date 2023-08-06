import pyautogui as py
import pyttsx3 as sx3

def alert():
    py.alert('This is an alert box.')
    'OK'

def confirm():
    py.confirm('Shall I proceed?')
    'Cancel'

def screenshot():
    im1 = py.screenshot()
    im1.save('Screenshot.png')
    im2 = py.screenshot('Screenshot.png')
    sx3.speak('Screenshot file has been saved. In your abhinav folder.')

def write():
    print(input('Enter your words: '))

def speak():
    engine = sx3.init()
    engine.say(input('Enter the words that are to speaken: '))
    engine.runAndWait()

def sum(a1,a2):
    n = a1 + a2
    print('The result is:', n)

def sub(a1,a2):
    n = a1 - a2
    print('The result is:', n)

def mul(a1,a2):
    n = a1 * a2
    print('The result is:', n)

def div(a1,a2):
    n = a1 / a2
    print('The result is:', n)

