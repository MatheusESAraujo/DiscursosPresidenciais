import numpy as np 
import pandas as pd 
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os, glob, io

download_dir = "C:\\Users\\mathe\\Desktop\\Projetos"
options = Options()
options.headless = True
options.add_argument(f"download.default_directory={download_dir}")


browser = "chromedriver"
driver =  webdriver.Chrome(browser,options=options)



def navigate (driver,url,df):
	
	
	# time.sleep(2)
	for i in range(30):
		try:
			driver.get(url)
			title = driver.find_element_by_xpath(f'//*[@id="content-core"]/article[{i+1}]/div/h2/a').get_attribute('textContent')
			print(title)
			href = driver.find_element_by_xpath(f'//*[@id="content-core"]/article[{i+1}]/div/h2/a').get_attribute('href')
			print(href)
			# textContent = driver.find_elements_by_xpath('//*[@class="Description"]')[i].get_attribute('textContent').splitlines()
			# print(textContent)
			speech = speech_extract(driver,href)
			date = title[:10].replace("-","/")

			try:		
				df = register(title,href,date,speech,df)
			except:
				print("---")
				df = df
		except:
			print("---------")
			df = df
	
	return df	

def speech_extract(driver,href):
	
	
	driver.get(href)
	# time.sleep(2)
	try:
		
		speech = driver.find_element_by_id("parent-fieldname-text").get_attribute('textContent')
	
	except:
		print("-----------------")
		
		speech = ""
	
	return speech 

		
def register(title,href,date,speech,df):
	df2 = pd.DataFrame([[title,href,date,speech]],columns=["title","href","date","speech"])
	df = pd.concat([df,df2], ignore_index=True)
	return df	

		
base = pd.DataFrame()
#infos_temer
for i in range(14):
	print(f"#######################################  |||| Temer Pag-{i} ||||  #######################################")
	df = pd.DataFrame()
	aux = i*30
	url = f"http://www.biblioteca.presidencia.gov.br/presidencia/ex-presidentes/michel-temer/discursos-do-presidente-da-republica/discursos?b_start:int={aux}"
	df = navigate(driver,url,df)
	base = pd.concat([base,df])

print(base)
base.to_csv("discursos_temer.csv",sep="|",index=False)

driver.close()