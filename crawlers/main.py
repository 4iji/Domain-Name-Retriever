#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
# gives
'http://stackoverflow.com/'
import json

with open('../config.json') as config_file:    
    config = json.load(config_file)
# Siftery Crawler
def crawlSiftery(browser,queryParam):
	url = "https://siftery.com/search?q="+queryParam
	browser.get(url);
	soup = BeautifulSoup(browser.page_source,"html.parser")
	companies = soup.find_all("div",{"class":"list-group-item__info"},limit=config['limit']['siftery'])
	output = []
	for company in companies:
		link = company.find('h5').text
		title = company.find('span').text
		pair = (title,link)
		output.append(pair)
	return output


		
#Google Crawler
def crawlGoogle(browser,queryParam):
	url = "https://www.google.co.in/search?q="+response+"&tbs=li:1" #The end part is to enable verbatim search
	browser.get(url);
	soup = BeautifulSoup(browser.page_source,"html.parser")
	companies = soup.find_all('div',{'class':'g'})
	output = []
	for company in companies:
		link = company.find('cite').text
		link =  link.split("/")[0] #To ignore the specific path post the website name
		title = company.find('h3',{'class':'r'}).find('a').text
		pair = (title,link)
		output.append(pair)
	return output

#Main code goes here
PHANTOMJS_PATH = config['phantomJSPath']
browser = webdriver.PhantomJS(PHANTOMJS_PATH)
response = raw_input("Please enter the name of the Company: ")
print "This is the response by Siftery \n"
crawlSiftery(browser,response)
print "This is the response by Google \n"
crawlGoogle(browser,response)

browser.quit()