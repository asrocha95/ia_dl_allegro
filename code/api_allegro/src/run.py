from game_api import *
import pyautogui as ag
from random import randint
import sys
import os
import platform
import time

AGENT_FPS = 10

if platform.system() == "Windows":
    bar = '\\'
    fexe = ''
else:
    bar = '/'
    fexe = '.'+bar

if len(sys.argv) > 1:
    folder = game = sys.argv[1]
else:
    print('\nE necessario o nome do jogo.\n')
    quit()

if len(sys.argv) > 2:
    path = sys.argv[2]
else:
    path = "."+bar


game_file = path+bar+game+".c"

if not os.path.isfile(game_file):
    print("Arquivo '"+game_file+"' não existe!")
    quit()

data = finder(game_file)
print(data.keys)

fexe = fexe+game+".exe"
control = ctrl(path+bar, fexe, game+".exe")
time.sleep(1/AGENT_FPS)
capture = state(control.window,game)

# capture.print_clock(f_name, 300)

l = len(data.keys)-1
while control.window.isActive:
    time.sleep(1/AGENT_FPS)
    if data.keyboard:
        a = data.keys[randint(0,l)]
        if a != 'escape':
            print("Pressed:", a) 
            ag.press(a)
        else:
            print('pause') 
        capture.print()
    if data.mouse:
        x1, x2, y1, y2 = control.edges()
        x = randint(x1,x2)
        y = randint(y1,y2)
        print("Clicked:", x, y)
        ag.click(x=x,y=y)
        capture.print()

