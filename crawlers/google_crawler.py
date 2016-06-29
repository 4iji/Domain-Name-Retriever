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
url = "https://www.google.co.in/search?q="+response+"&tbs=li:1"
browser.get(url);
soup = BeautifulSoup(browser.page_source,"html.parser")
results = soup.find_all('div',{'class':'g'})
for result in results:
	link = result.find('cite').text
	title = result.find('h3',{'class':'r'}).find('a').text
	print link
	print title
	print "\n"
browser.quit()