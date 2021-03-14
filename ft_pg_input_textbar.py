import pygame as pg
import pyperclip
import time

pg.font.init()

FT_WTHEME_TXT = (3, 3, 3)
FT_WTHEME_BG_COLOR = (249, 249, 249)
FT_WTHEME_BORDER_COLOR = (0, 0, 0)
FT_WTHEME_CURSOR_COLOR = (3, 3, 3)
FT_WTHEME_PLACECHOLDER_COLOR = (96, 96, 96)

# todo: 
#		- create some THEMES (black, white, blue, etc...)
#	//	- limiter la taille du texte pour pas qu'il depasse
#		- clignotement du curseur
#		- changer la position du curseur en clique gauche
#		- 2 clic gauche : selection du mot, 3 clic gauche : selection de la ligne
#		- selection du texte (pour copier coller, supprimer, couper)
#		- selectionner une font auto avec une taille adaptée
#		- historique pour ctrl + z et ctrl + shift + z
#		- menu clique droit
#		- gestion des caracs chelous genre TAB qui affichent des carrés en mode caractère pas pris en compte
#		- ajout d'une FONCTION qui permet de changer les parametres (couleur, texte, etc...) depuis le main
#		- ajout argument fonction pour lancer une fonction lorsque l'utilisateur tape entree
#		- ajout argument bg / text / threshold transparent
#		- ajout argument croix sur le coté droit pour supprimer toute la recherche
#		- ajout argument bouton search
#		- ajout argument bouton reconnaissance vocale
#		- ajout argument historique des recherches qui s'affichent quand on clique sur la barre
#		- ajout argument changement de la couleur de la bordure quand active = True
#		- ajout argument autocompletion recherche

FT_AUTO_FONT = pg.font.Font(pg.font.get_default_font(), 30)

class FtPgInputTextbar(object):
	def __init__(
				self,
				screen,
				id_=False,
				pos=(0, 0),
				size=(200, 50),
				bg_color=FT_WTHEME_BG_COLOR,
				rounded=6,
				border=True,
				border_width=2,
				border_color=FT_WTHEME_BORDER_COLOR,
				placeholder=False,
				placeholder_font=False,
				placeholder_color=FT_WTHEME_PLACECHOLDER_COLOR,
				font=FT_AUTO_FONT,
				text_color=FT_WTHEME_TXT,
				text_antialias=True,
				distance_left_text=False, # distance entre les bordures de la barre et du texte
				cursor_color=FT_WTHEME_CURSOR_COLOR,
				display_on=True
				):

		self.screen = screen
		self.id_ = id_
		self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
		self.bg_color = bg_color
		self.rounded = rounded
		self.border = border
		self.border_width = border_width
		self.border_color = border_color
		self.font = font
		self.text_color = text_color
		self.text_antialias = text_antialias
		self.cursor_color = cursor_color
		self.display_on = display_on

		self.font_max_height = self.font.size("|")[1]
		self.distance_top_text = self.rect.h / 2 - self.font_max_height / 2
		if distance_left_text:
			self.distance_left_text = distance_left_text
		else:
			self.distance_left_text = 10
		self.text_max_width = int(self.rect.w - self.distance_left_text * 2)
		
		if placeholder:
			if placeholder_font:
				self.placeholder = placeholder_font.render(placeholder, text_antialias, placeholder_color)
			else:
				self.placeholder = font.render(placeholder, text_antialias, placeholder_color)
		else:
			self.placeholder = False

		self.active = False
		self.ctrl_pressed = False
		self.cursor_ibeam = False
		self.text = ""

		self.cursor_pos = len(self.text)
		self.cursor_pix_pos = 0

		self.init_surface_bg_and_cursor()
		self.get_actual_surface()

	def init_surface_bg_and_cursor(self):
		# save bg_surface
		self.bg_surface = pg.Surface((self.rect.w, self.rect.h))
		self.bg_surface.fill(self.bg_color)
		rounded_surface = pg.Surface((self.rect.w, self.rect.h), pg.SRCALPHA)
		pg.draw.rect(rounded_surface, (255, 255, 255), (0, 0, self.rect.w, self.rect.h), border_radius=self.rounded)
		self.bg_surface = self.bg_surface.convert_alpha()
		self.bg_surface.blit(rounded_surface, (0, 0), None, pg.BLEND_RGBA_MIN)

		if self.border:
			# draw border if param border == True
			pg.draw.rect(self.bg_surface, self.border_color, pg.Rect(0, 0, self.rect.w, self.rect.h),
				width=self.border_width, border_radius=self.rounded)

		# save cursor_surface
		self.cursor_surface = pg.Surface((1, self.font_max_height))
		self.cursor_surface.fill(self.cursor_color)


	def get_actual_surface(self):
		self.display_text_x = 0
		self.actual_surface = self.bg_surface.copy()

		if self.active:
			left_text_surface = self.font.render(self.text[:self.cursor_pos], self.text_antialias, self.text_color)
			left_text_size = left_text_surface.get_size()[0]
			#right_text_surface = self.font.render(self.text[self.cursor_pos:], self.text_antialias, self.text_color)

			full_text_surface = self.font.render(self.text, self.text_antialias, self.text_color)

			if self.cursor_pix_pos > self.text_max_width:
				self.cursor_pix_pos = self.text_max_width
			elif self.cursor_pix_pos < 0:
				self.cursor_pix_pos = 0
			# s'il y a des carac cachés a gauche alors qu'il y a la place
			# // A FAIRE
			#elif self.cursor_pos == len(self.text)

			text_surface = pg.Surface((self.text_max_width, self.font_max_height))
			text_surface.fill(self.bg_color)
			
			if left_text_size > self.cursor_pix_pos:
				text_surface.blit(full_text_surface, (0 - (left_text_size - self.cursor_pix_pos), 0))
			else:
				text_surface.blit(full_text_surface, (0, 0))

			self.actual_surface.blit(text_surface, (self.distance_left_text, self.distance_top_text))

		elif self.text != "":
				text_surface = self.font.render(self.text, self.text_antialias, self.text_color)

				self.actual_surface.blit(text_surface, (self.distance_left_text, self.distance_left_text))

		elif self.placeholder:
			self.actual_surface.blit(self.placeholder, (self.distance_left_text, self.distance_left_text))



	def event(self, event):
		if self.display_on:
			if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				mx, my = pg.mouse.get_pos()
				if self.rect.collidepoint((mx, my)):
					if not self.active:
						self.active = True
						self.cursor_pos = len(self.text)
						self.cursor_pix_pos = self.font.size(self.text)[0]
						self.ctrl_pressed = False
				else:
					self.active = False

			elif self.active and event.type == pg.KEYDOWN:
				if event.key == 1073742048:
					self.ctrl_pressed = True

				elif event.key == pg.K_BACKSPACE:
					if self.cursor_pos > 0:
						previous_size = self.font.size(self.text)[0]
						self.text = (self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:])
						self.cursor_pix_pos -= (previous_size - self.font.size(self.text)[0])
						self.cursor_pos -= 1

				elif event.key == pg.K_DELETE:
					self.text = (self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:])
				
				elif event.key == pg.K_RETURN:
					self.active = False
					self.get_actual_surface()
					return self.text

				elif event.key == pg.K_RIGHT:
					if self.cursor_pos < len(self.text):
						self.cursor_pix_pos += (self.font.size(self.text[:self.cursor_pos + 1])[0] - self.font.size(self.text[:self.cursor_pos])[0])
						self.cursor_pos += 1

				elif event.key == pg.K_LEFT:
					if self.cursor_pos > 0:
						self.cursor_pix_pos -= (self.font.size(self.text[:self.cursor_pos])[0] - self.font.size(self.text[:self.cursor_pos - 1])[0])
						self.cursor_pos -= 1

				elif event.key == pg.K_END:
					self.cursor_pix_pos += (self.font.size(self.text)[0] - self.font.size(self.text[:self.cursor_pos])[0])
					self.cursor_pos = len(self.text)

				elif event.key == pg.K_HOME:
					self.cursor_pix_pos = 0
					self.cursor_pos = 0

				elif self.ctrl_pressed:
					if event.key == ord("v"):
						string = pyperclip.paste()
						previous_size = self.font.size(self.text)[0]
						self.text = (self.text[:self.cursor_pos] + string + self.text[self.cursor_pos:])
						self.cursor_pix_pos += (self.font.size(self.text)[0] - previous_size)
						self.cursor_pos += len(string)

					elif event.key == ord("c"):
						pyperclip.copy(self.text)
					elif event.key == ord("x"):
						pyperclip.copy(self.text)
						self.text = ""
						self.cursor_pix_pos = 0
						self.cursor_pos = 0
				else:
					previous_size = self.font.size(self.text)[0]
					self.text = (self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:])
					self.cursor_pix_pos += (self.font.size(self.text)[0] - previous_size)
					self.cursor_pos += len(event.unicode)

			elif event.type == pg.KEYUP and event.key == 1073742048:
				self.ctrl_pressed = False

			# if active is False or True
			if event.type == pg.MOUSEMOTION:
				mx, my = pg.mouse.get_pos()
				if self.rect.collidepoint((mx, my)):
					if not self.cursor_ibeam:
						pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_IBEAM)
						self.cursor_ibeam = True
				elif self.cursor_ibeam:
					pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
					self.cursor_ibeam = False

			self.get_actual_surface()
		return False

	def display(self):
		if self.display_on:
			self.screen.blit(self.actual_surface, (self.rect.x, self.rect.y))
			if self.active:
				self.screen.blit(self.cursor_surface, (self.rect.x + self.distance_left_text + self.cursor_pix_pos, self.rect.y + self.distance_top_text))
