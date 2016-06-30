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
url = "https://siftery.com/search?q="+response
browser.get(url);
soup = BeautifulSoup(browser.page_source,"html.parser")
companies = soup.find_all("div",{"class":"list-group-item__info"},limit=config['limit']['siftery'])
for company in companies:
	link = company.find('h5').text
	title = company.find('span').text
	print link
	print title
	print "\n"
browser.quit()