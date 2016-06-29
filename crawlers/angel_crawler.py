import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import json
with open('../config.json') as config_file:    
    config = json.load(config_file)
#PhantomJs Files have different extensions for different operating system
PHANTOMJS_PATH = config['phantomJSPath']
browser = webdriver.PhantomJS(PHANTOMJS_PATH)
response = raw_input("Please enter the name of the Company: ")
url = "https://angel.co/search?q="+response+"&type=companies"
browser.get(url);
soup = BeautifulSoup(browser.page_source,"html.parser")

companies = soup.find_all("div",{"class":"title"},limit=config['limit']['angel'])
for company in companies:
	profile = company.find_all('a',href=True)
	if(len(profile)>0):
		url = str(profile[0]['href'])
		#TODO Open this URL in browser instance, create a soup out of it and extract company name and website 
browser.quit()