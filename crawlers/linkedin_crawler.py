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
url = "https://www.google.co.in/search?q="+response+"+:www.linkedin.com/company"
browser.get(url);
soup = BeautifulSoup(browser.page_source,"html.parser")
results = soup.find_all('div',{'class':'g'},limit=config['limit']['linkedin'])
for result in results:
	link = result.find('cite').text
	title = result.find('h3',{'class':'r'}).find('a').text
	browser.get(str(link))
	newSoup = BeautifulSoup(browser.page_source,"html.parser")
	company_name = newSoup.find("h1",{"class":"name"}).text
	company_website = newSoup.find("li",{"class":"website"}).find("a").text
	print company_name
	print company_website
browser.quit()