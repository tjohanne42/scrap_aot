import pygame as pg
import os
import atexit
import constants

def ft_pg_init	(
				title=False,
				icon_path=False,
				window_size=False,
				load_pg_mixer=True,
				load_font=True,
				font_path=False,
				font_size=(1, 30),
				centered=True,
				return_dict=False
				):


	# center window display
	if centered:
		try:
			os.environ["SDL_VIDEO_CENTERED"] = "1"
		except:
			print("ft_pg_init : os.environ['SDL_VIDEO_CENTERED'] = '1' FAILED")


	# init pygame
	pg.init()


	# atexit quit pygame
	atexit.register(pg.quit)


	# title of window
	if title:
		pg.display.set_caption(title)


	# icon of window
	if icon_path:
		icon_surface = pg.image.load('assets/icon.ico')
		pg.display.set_icon(icon_surface)


	# window size
	if window_size:
		window_width, window_height = window_size
	else:
		info = pg.display.Info()
		window_width, window_height = int(info.current_w * 9 / 10), int(info.current_h * 9 / 10)



	# create the screen
	screen = pg.display.set_mode((window_width, window_height), pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)


	# get clock time
	clock = pg.time.Clock()


	# init pygame mixer
	if load_pg_mixer:
		pg.mixer.init(44100, -16, 2, 2048, allowedchanges=pg.AUDIO_ALLOW_ANY_CHANGE)


	# load font as a dict
	# fonts[x] means "FONT WITH SIZE x"
	# fontsize is tuple with minsize and maxsize of fonts we want to load
	# fontsize=(x,y) means "FONTS WITH SIZE x TO y included"
	if load_font:
		if not font_path or os.path.isfile(font_path):
			font_path = pg.font.get_default_font()
		fonts = {}
		i = font_size[0]
		while i <= font_size[1]:
			fonts[i] = pg.font.Font(font_path, i)
			i += 1


	# if return_dict is True then return all values in dict
	if return_dict:
		ft_dict = 	{
					"window_width" : window_width,
					"window_height" : window_height,
					"screen" : screen,
					"clock" : clock,
					}
		if load_font:
			ft_dict["fonts"] = fonts
		return ft_dict


	# else return all values
	if load_font:
		return screen, window_width, window_height, clock, fonts
	else:
		return screen, window_width, window_height, clock
