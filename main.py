import time
import pygame as pg
import sys
import concurrent.futures
from datetime import datetime

from scrap_episode_aot import *
from ft_pg_init import *
from ft_pg_gui import *

BG = (40, 40, 40)
WHITE_TXT = (200, 200, 200)

class MyApp(object):

	def __init__(self):

		self.screen, self.window_width, self.window_height, self.clock, self.fonts = ft_pg_init()
		self.fps = 30
		self.running = True

		self.ft_gui = FtPgGui(self.screen)
		
		self.init_variables()


	def quit(self):
		if self.loaded:
			now = datetime.now()
			str_now = now.strftime("%d/%m/%Y %H:%M:%S")
			self.logs_a.write(f"\n{str_now} episode {self.episode} saison {self.saison}")
		while self.playing:
			time.sleep(1)
		while self.loading:
			time.sleep(1)

	def init_variables(self):
		self.nb_episode = [25, 12, 22, 13]
		self.logs_r = open('logs.txt', "r")
		self.logs_a = open('logs.txt', "a")
		#text = self.logs.readlines()[-1]
		self.last_session = self.logs_r.readlines()[-1]
		self.last_session_surface = self.fonts[20].render("last session: " + self.last_session, True, WHITE_TXT)

		self.start_session = time.time()
		self.end_session = self.start_session + 2 * 60 * 60

		self.text_bar_end_session = self.ft_gui.add_input_textbar(id_="end session", pos=(800, 10), size=(300, 50), font=self.fonts[30],
									placeholder="end session in")
		self.text_bar_saison = self.ft_gui.add_input_textbar(id_="saison", pos=(100, 10), size=(300, 50), font=self.fonts[30],
								placeholder="saison")
		self.text_bar_episode = self.ft_gui.add_input_textbar(id_="episode", pos=(100, 70), size=(300, 50), font=self.fonts[30],
								placeholder="épisode")
		self.button_episode = self.ft_gui.add_button(id_="episode", pos=(420, 10), size=(300, 110), text="rechercher", font=self.fonts[30])

		self.loading = False
		self.loading_surface = self.fonts[30].render("loading ...", True, WHITE_TXT)

		self.playing = False
		self.playing_surface = self.fonts[30].render("playing ...", True, WHITE_TXT)

		self.loaded = False

		

	def play_episode(self, file_name):
		self.playing = True
		os.system(f"vlc {file_name} --fullscreen vlc://quit")
		self.playing = False
		self.end_playing = time.time()

	def load_episode(self, saison, episode):
		self.loading = True
		file_name = f"video/saison{saison}/episode{episode}.mp4"
		print("loading", file_name)
		link = download_aot(saison, episode, file_name, download=True)
		f1 = concurrent.futures.ThreadPoolExecutor().submit(self.play_episode, file_name)
		episode += 1
		if episode > self.nb_episode[saison-1]:
			episode = 1
			saison += 1
		if not saison > 4:
			file_name = f"video/saison{saison}/episode{episode}.mp4"
			print("loading", file_name)
			link = download_aot(saison, episode, file_name, download=True)
		self.loaded = True
		self.loading = False


	def event(self, event):
		ret = self.ft_gui.event(event)
		if not self.playing and not self.loading and not self.loaded and ret["button"][self.button_episode.id_]:
			try:
				self.saison = int(self.text_bar_saison.text)
				self.episode = int(self.text_bar_episode.text)
			except:
				print("bad inputs")
			if self.saison < 1 or self.saison > 4 or self.episode < 1 or self.episode > self.nb_episode[self.saison-1]:
				print("episode not exist")
			else:
				f1 = concurrent.futures.ThreadPoolExecutor().submit(self.load_episode, self.saison, self.episode)
		if ret["textbar"][self.text_bar_end_session.id_]:
			try:
				value = int(self.text_bar_end_session.text)
				self.end_session = time.time() + value * 60
			except:
				print("bad input")

	def display(self, fps=False):
		# finit la session apres un certain temps
		if time.time() >= self.end_session:
			print("end session by time")
			self.running = False
			return

		# si l'episode est finis, lance le prochain
		if self.loaded and not self.playing and not self.loading:
			if time.time() > self.end_playing + 15:
				self.episode += 1
				if self.episode > self.nb_episode[self.saison-1]:
					self.episode = 1
					self.saison += 1
				if self.saison > len(self.nb_episode) + 1:
					print("reached the end of the serie")
					self.running = False
					return
				else:
					f1 = concurrent.futures.ThreadPoolExecutor().submit(self.load_episode, self.saison, self.episode)

		self.screen.fill(BG)
		
		if self.loading:
			self.screen.blit(self.loading_surface, (400, 400))

		if self.playing:
			self.screen.blit(self.playing_surface, (400, 600))

		# display fps
		if not fps:
			fps_real_time_surface = self.fonts[15].render("FPS : -", True, WHITE_TXT)
		else:
			fps_real_time_surface = self.fonts[15].render("FPS : " + str(fps), True, WHITE_TXT)
		self.screen.blit(fps_real_time_surface, (20, 20))

		end_session_in_surface = self.fonts[30].render("session end in : " + str(round((self.end_session - time.time()) / 60, 1)) + " min",
			True, WHITE_TXT)
		self.screen.blit(end_session_in_surface, (800, 70))
		self.screen.blit(self.last_session_surface, (800, 110))

		self.ft_gui.display()
		pg.display.flip()


if __name__ == "__main__":

	app = MyApp()
	
	timer = time.time()
	count_fps = 0
	last_count_fps = False
	
	while app.running:
	
		for event in pg.event.get():
			if event.type == pg.QUIT:
				app.running = False
			else:
				app.event(event)
	
		app.display(last_count_fps)
	
		app.clock.tick(app.fps)
	
		count_fps += 1
		if time.time() - timer >= 1:
			last_count_fps = count_fps
			count_fps = 0
			timer = time.time()
	
	app.quit()

"""
nb_episode = 



saison = int(input("quelle saison?\n"))
episode = int(input("quel episode?\n"))

if saison > 4 or saison < 1:
	print("wrong input")
	exit()

if episode > nb_episode[saison - 1] or episode < 1:
	print("wrong input")
	exit()

print("start watching ...")


start = time.time()

launched = True
while launched:
	os.system(f"python scrap_episode.py {saison} {episode}")
	print("done")
 
	file_name = f"video/saison{saison}/episode{episode}.mp4"
	os.system(f"vlc {file_name} --fullscreen vlc://quit")
	logs.truncate()
	logs.write(f"{saison} {episode}")
	logs.close()

	if time.time() - start >= 120 * 60:
		print("last episode:", saison, episode)
		exit()
	episode += 1
	if episode > nb_episode[saison-1]:
		saison += 1
		episode = 1
	if saison > 4:
		print("end of serie")
		exit()
"""
