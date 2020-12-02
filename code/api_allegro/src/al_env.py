from game_api import *
import pyautogui as ag
from random import randint
import sys
import os
import platform
import time
import numpy as np

# from al_env import al_env; env =al_env(start=True)

OS_is_MAC = False

if platform.system() == "Windows":
    bar = '\\'

elif platform.system() == "Darwin":
	OS_is_MAC = True
	bar = '/'
else:
    bar = '/'

SCREEN_W = 640;    # largura tela
SCREEN_H = 480;    # altura tela
LOCATE_WIN_WITH_IMG = "frog_locate_window.png" # Arquivo usado para localizar a janela na tela usando PILLOW
AGENT_FPS = 10

class al_env:
	def __init__(self,game='frogger',path='..'+ bar + '..'+ bar + 'frogger',
		locate_on_screen=None,box_height=None,box_width=None,adjust_top=0,adjust_left=0):
		
		if platform.system() == "Windows":
		    self.bar = '\\'
		    self.fexe = ''
		else:
		    self.bar = '/'
		    self.fexe = '.' + self.bar

		self.game = game
		self.path = path
		self.title = game + '.exe'
		self.fexe = self.path+bar+self.fexe + self.title
		self.data = finder(self.path+bar+game+'.c')
		self.actions = self.data.keys

		# Remove escape key from action space
		try:
			self.actions.remove('escape')
		except:
			pass

		self.num_actions = len(self.actions)
		self.control = None
		self.capture = None
		self.done = True

		self.position=0
		self.reward=0

		self.locate_on_screen=locate_on_screen
		self.box_height=box_height
		self.box_width=box_width
		self.adjust_top=adjust_top
		self.adjust_left=adjust_left

		if OS_is_MAC:
			self.locate_on_screen=LOCATE_WIN_WITH_IMG
			self.box_height=SCREEN_H
			self.box_width=SCREEN_W

		# Se desloca para a pasta do programa
		# os.chdir(path+bar)

	def start(self):
		self.reward=0
		self.position=0
		self.control = ctrl(self.fexe, self.title,self.locate_on_screen,self.box_height,self.box_width,self.adjust_top,self.adjust_left)
		self.done = not self.control.window.isActive

		time.sleep(0.1)
		self.capture = state(self.control.window,self.path,self.game)

		obs = np.array(self.capture.print())
		obs = obs[:,:,:3]

		return obs
		
	def stop(self):
		if self.control is not None:
			self.control.stop()

	def reset(self):
		self.stop()
		return self.start()

	def step(self,a):
		action = self.actions[a]
		
		# Takes action and get observation
		if action != 'escape':
			ag.press(action)
		obs = np.array(self.capture.print())
		obs = obs[:,:,:3]

		# Gets game state
		if OS_is_MAC:
			self.control.window.isActive = ag.locateOnScreen(self.locate_on_screen) is not None

		self.done = not self.control.window.isActive
		
		# Calculates Reward
		# Tracks the position of the agent
		if action=='w':
			self.position+=1
			self.reward = 1
		elif action=='s' and self.position>0:
			self.position-=1
			self.reward = -1
		else:
			self.reward = -0.05


		if self.done:
			output = self.control.process.stdout.readline()
			if len(output) > 0: # Frogger
				self.reward = -1
				# pass
			else:
				self.reward=10
		

		return obs, self.reward, self.done