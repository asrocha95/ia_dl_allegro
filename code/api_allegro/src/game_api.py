import pyautogui as ag
import pygetwindow as gw
import os
import subprocess
import signal
from time import time
import platform
import shutil
from PIL import Image

OS_is_MAC = False

if platform.system() == "Windows":
    bar = '\\'

elif platform.system() == "Darwin":
	OS_is_MAC = True
	bar = '/'
else:
    bar = '/'

# Perceptor
class state():
	n = 0
	nt = 0
	ct = 0.0
	def __init__(self, window,path, name):
		self.win = window
		self.name = name
		self.path = path
		if not os.path.exists(self.path+bar+'img'):
			os.makedirs(self.path+bar+'img')
		else: 
			shutil.rmtree(self.path+bar+'img')
			os.makedirs(self.path+bar+'img')
		
	def print(self):
		if self.win.isActive:
			self.n = self.n+1
			print_name = self.path+bar+'img'+bar+self.name+str(self.n)+'.png'

			# if OS_is_MAC:
			# 	screen_capt_command = 'screencapture -R ' + str(self.win.left) + ',' + str(self.win.top) + ',' + str(self.win.width) + ',' + str(self.win.height)  + ' ' + print_name
			# 	subprocess.call(screen_capt_command,shell=True)
			# 	return Image.open(print_name)

			return ag.screenshot(print_name, region=(self.win.left, self.win.top, self.win.width, self.win.height))
		

	def print_clock(self, name, t):
		while self.win.isActive:
			if time() - self.ct > t:
				self.ct = time()
				self.nt = self.nt+1
				ag.screenshot('img\\'+name+'_t_'+str(self.nt)+'.png', region=(self.win.left, self.win.top, self.win.width, self.win.height))

# Atuador
class ctrl:
	def __init__(self,fexe,title,locate_on_screen=None,box_height=None,box_width=None,adjust_top=0,adjust_left=0):
		self.locate_on_screen = locate_on_screen
		# Inicia o programa em um novo proocesso
		self.process = subprocess.Popen(fexe, stdout=subprocess.PIPE, shell=True)
		self.window = self.getWindowMac(title,locate_on_screen,box_height,box_width,adjust_top,adjust_left) if OS_is_MAC else self.getWindowWindows(title)

	def getWindowWindows(self,title):
		# Espera a janela abrir e a ativa 
		while True:	
			try: 
				window = gw.getWindowsWithTitle(title)[0]
				window.activate()
				break
			except:
				pass 

		return window;

	def getWindowMac(self,title,locate_on_screen,box_height,box_width=None,adjust_top=0,adjust_left=0): # !!!! Workaround - NOT RECOMENDED !!!!
		#Obtem janela
		return window_for_mac(title,locate_on_screen,box_height,box_width,adjust_top,adjust_left)

	def edges(self):
		return self.window.left, self.window.left+self.window.width, self.window.top, self.window.top+self.window.height

	def stop(self):
		self.process.terminate()
		if OS_is_MAC:
			self.window.isActive = ag.locateOnScreen(self.locate_on_screen) is not None
		else:
			while self.window.isActive:
				pass
# Classe de janela para Mac !!!! Workaround - NOT RECOMENDED !!!!
class window_for_mac:
	def __init__(self,title,locate_on_screen,box_height,box_width=None,adjust_top=0,adjust_left=0):
		self.title = title
		self.isActive = False
		self.box_region = None
		while not self.isActive:
			try:
				self.box_region=ag.locateOnScreen(locate_on_screen)
				self.isActive = self.box_region is not None
			except:
				pass

		self.top = self.box_region.top + self.box_region.height + adjust_top
		self.left = self.box_region.left + adjust_left
		self.width = box_width if box_width is not None else self.box_region.width
		self.height = box_height

	
		
		

# Identificador
class finder:
	keyboard = False
	mouse = False

	def __init__(self, file_name):
		# Abre o arquivo *.c
		try:
			self.file = open(file_name, 'r').read()
		except:
			print("File {} not found.".format(file_name))
			return
		
		# Guarda todas as palavras do arquivo 
		self.words = self.to_list(self.file)

		if self.search('mouse'):
			self.mouse = True

		# Recupera todas as teclas pressionaveis
		self.keys = self.get_keys('ALLEGRO_KEY_')

		if len(self.keys)>0:
			self.keyboard = True

		
	# Transforma um arquivo.c em uma lista de palavras
	def to_list(self, txt):
		# Aprende todos osimbolos utilizados
		simbols = []
		valids = [' ','_']
		for a in txt:
			if not a.isalnum() and a not in valids:
				if a not in simbols:
					simbols.append(a)
		
		new_txt = txt
		
		# Retira os simbolos do texto para facilitar a separacao
		for s in simbols:
			new_txt = new_txt.replace(s, ' ')

		# Separa todas as palavras e cria uma lista das validas
		return [w for w in new_txt.split(' ') if len(w) > 0 ]

	# Retorna todas as palavras que contem um termo
	def search(self, name):
		word_list = []

		for word in self.words:
			if len(word) < len(name):
				continue

			for i in range(len(word)):
				if len(word)-i < len(name):
					break

				if name[0] == word[i]:
					found = False

					for j in range(len(name)):
						if name[j] == word[i+j]:
							found = True
						else:
							found = False
							break

					if found and word not in word_list:
						word_list.append(word)
						break

		return word_list

	# Retorna todas as teclas validas
	def get_keys(self, prefix):
		# Lista as palavras com comandos de tecla
		w_list = self.search(prefix)
		k_list = []
		
		# Retira o prefixo de comando
		for w in w_list:
			k_list.append(w.replace(prefix, ''))
		
		# Lista as teclas 
		return [k.lower() for k in k_list if len(k) > 0 ]
