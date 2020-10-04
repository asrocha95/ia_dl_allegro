from game_api import *
import pyautogui as ag
from random import randint
import sys
import os
import platform
import time

# from allegro_env import al_env

AGENT_FPS = 10

class al_env:
	def __init__(self,game='frogger',path='..'+ bar + '..'+ bar + 'frogger',start=True):
		
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
		self.control = None
		self.capture = None

		self.position=0
		self.reward=0

		# Se desloca para a pasta do programa
		# os.chdir(path+bar)

		if start:
			self.start()
			# while self.control.window.isActive:
			#     time.sleep(1/AGENT_FPS)
			#     if self.data.keyboard:
			#         a = self.data.keys[randint(0,len(self.data.keys)-1)]
			#         self.step(a)
			#         # if a != 'escape':
			#         #     print("Pressed:", a) 
			#         #     ag.press(a)
			#         # else:
			#         #     print('pause') 
			#         # self.capture.print()

	def start(self):
		self.control = ctrl(self.fexe, self.title)
		time.sleep(1/AGENT_FPS)
		self.capture = state(self.control.window,self.path,self.game)
		
	def stop(self):
		self.control.stop()

	def step(self,action):
		# Tracks the position of the agent
		if action=='w':
			self.position+=1
		elif action=='s' and self.position>0:
			self.position-=1

		# Takes action and get observation
		if action != 'escape':
			ag.press(action)
		self.capture.print()

		# Gets game state
		self.done = not self.control.window.isActive

		# Calculates Reward
		if self.done:
			if self.position>=10:
				self.reward=float('inf')
			else:
				self.reward -= 100000
		else:
			self.reward+=1

		return self.reward, self.done

		