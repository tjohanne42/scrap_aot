import pygame as pg

# my modules
from ft_pg_input_textbar import *
from ft_pg_button import *

class FtPgGui(object):

	def __init__(self, screen):
		pg.key.set_repeat(400, 35)
		self.screen = screen
		self.buttons = []
		self.input_textbar = []

	def add_button(self, **kwargs):
		self.buttons.append(FtPgButton(self.screen, **kwargs))
		return self.buttons[-1]

	def add_input_textbar(self, **kwargs):
		self.input_textbar.append(FtPgInputTextbar(self.screen, **kwargs))
		return self.input_textbar[-1]


	def event(self, event):
		my_ret = {"textbar": {}, "button": {}}

		for textbar in self.input_textbar:
			ret = textbar.event(event)
			my_ret["textbar"][textbar.id_] = ret

		for button in self.buttons:
			ret = button.event(event)
			my_ret["button"][button.id_] = ret

		return my_ret


	def display(self):
		for textbar in self.input_textbar:
			textbar.display()

		for button in self.buttons:
			button.display()
