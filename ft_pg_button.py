import pygame as pg
import time

pg.font.init()
FT_AUTO_FONT = pg.font.Font(pg.font.get_default_font(), 30)
FT_TXT_COLOR = (3, 3, 3)

class FtPgButton(object):
	def __init__(
				self,
				screen,
				id_=False,
				pos=(0, 0),
				size=(200, 200),
				text=False,
				text_color=FT_TXT_COLOR,
				text_antialias=True,
				font=FT_AUTO_FONT,
				theme=False,
				display_on=True
				):

		self.screen = screen
		self.id_ = id_
		self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
		self.text = text
		self.text_color = text_color
		self.text_antialias = text_antialias
		self.font = font
		self.theme = theme
		self.display_on = display_on

		self.hold = False
		self.active = False
			

		self.unactive_surface = pg.Surface((self.rect.w, self.rect.h))
		self.unactive_surface.fill((100,149,237))

		self.active_surface = pg.Surface((self.rect.w, self.rect.h))
		self.active_surface.fill((240,128,128))

		if self.text:
			text_surface = self.font.render(self.text, self.text_antialias, self.text_color)
			self.unactive_surface.blit(text_surface,
				(self.rect.w / 2 - text_surface.get_size()[0] / 2, self.rect.h / 2 - text_surface.get_size()[1] / 2))
			self.active_surface.blit(text_surface,
				(self.rect.w / 2 - text_surface.get_size()[0] / 2, self.rect.h / 2 - text_surface.get_size()[1] / 2))


	def event(self, event):
		if self.display_on:
			if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				mx, my = pg.mouse.get_pos()
				if self.rect.collidepoint((mx, my)):
					self.hold = True
					self.active = True

			elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
				self.active = False
				if self.hold:
					self.hold = False
					return True
				self.hold = False

			elif event.type == pg.MOUSEMOTION:
				if self.hold:
					mx, my = pg.mouse.get_pos()
					if not self.rect.collidepoint((mx, my)):
						self.hold = False


	def display(self):
		if self.display_on:
			if self.active:
				self.screen.blit(self.active_surface, (self.rect.x, self.rect.y))
			else:
				self.screen.blit(self.unactive_surface, (self.rect.x, self.rect.y))

