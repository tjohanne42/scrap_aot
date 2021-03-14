import random
import urllib.request

from bs4 import BeautifulSoup

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time

def user_agent():
	tab = ["Mozilla/5.0", "Linux", "Android 8.0.0", "Pixel 2 XL", "Build/OPD1.170816.004",
	"AppleWebKit/537.36", "(KHTML, like Gecko)", "Chrome/67.0.3396.87", "Mobile Safari/537.36"]
	return tab[random.randint(0, len(tab) - 1)]


def init_selenium():
	useragent = user_agent()
	firefoxOptions = Options()

	firefoxOptions.add_argument("-headless")
	profile = webdriver.FirefoxProfile()
	profile.set_preference("general.useragent.override", useragent)
	try:
		driver = webdriver.Firefox(firefox_profile=profile, executable_path="geckodriver", options=firefoxOptions)
	except:
		print("selenium is not configure with geckodriver")
		exit()
	return driver

def get_link_aot(saison, episode):
	if saison == 3:
		main_url = f"https://attaque-des-titans-streaming.net/shingeki-no-kyojin-season-{saison}-episode-{episode}-vostfr/"
	elif saison == 4:
		if episode >= 8:
			main_url = f"https://attaque-des-titans-streaming.net/lattaque-des-titans-saison-{saison}-episode-{episode}-vostfr/"
		else:
			main_url = f"https://attaque-des-titans-streaming.net/shingeki-no-kyojin-saison-{saison}-episode-{episode}-vostfr/"

	driver = init_selenium()
	driver.get(main_url)
	driver.execute_script("window.scrollTo(0, 500);")
	time.sleep(1)
	iframes = driver.find_elements_by_tag_name("iframe")
	driver.switch_to.frame(iframes[2])
	buttons = driver.find_elements(By.XPATH, '//button')
	main_handle = driver.window_handles
	title = driver.title
	i = 0
	while i < 20:
		try:
			action = ActionChains(driver)
			action.move_to_element(buttons[0])
			action.click()
			action.perform()
		except:
			break
		time.sleep(1)
		handles = driver.window_handles
		if len(handles) > 1:
			driver.switch_to.window(handles[1])
			driver.close()
			driver.switch_to.window(main_handle[0])
			driver.switch_to.frame(iframes[2])
		i += 1
	video = driver.find_element(By.CLASS_NAME, "vjs-tech")
	link = video.get_attribute("src")
	driver.close()
	driver.quit()
	return link

def download_link(link, file_name):
	rsp = urllib.request.urlopen(link)
	with open(file_name,'wb') as f:
	    f.write(rsp.read())
	print(file_name, "downloaded")

def file_exist(file_name):
	try:
		open(file_name)
		return True
	except:
		return False

def download_aot(saison, episode, file_name, download=True):
	#import sys
	
	#saison = int(sys.argv[1])
	#episode = int(sys.argv[2])
	if file_exist(file_name):
		return True
	
	link = get_link_aot(saison, episode)

	if download:
		download_link(link, file_name)

	return link

if __name__ == "__main__":

	#test
	saison = 3
	episode = 17
	download = False
	link = download_aot(saison, episode, f"video/saison{saison}/episode{episode}.mp4", download=download)
	print(link)