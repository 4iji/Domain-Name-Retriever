#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import json

with open('../config.json') as config_file:    
    config = json.load(config_file)
# LevenShtein Distance 
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]
# Siftery Crawler
def crawlSiftery(browser,queryParam):
	url = "https://siftery.com/search?q="+queryParam
	browser.get(url);
	soup = BeautifulSoup(browser.page_source,"html.parser")
	companies = soup.find_all("div",{"class":"list-group-item__info"},limit=config['limit']['siftery'])
	print companies
	output = []
	for company in companies:
		link = company.find('h5',{'class':'list-group-item__title'}).text
		title = company.find('div',{'class':'list-group-item__text'}).text
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
		link =  link.split("/")[0]
		title = company.find('h3',{'class':'r'}).find('a').text
		pair = (title,link)
		output.append(pair)
	return output

#Main code goes here
PHANTOMJS_PATH = config['phantomJSPath']
browser = webdriver.PhantomJS(PHANTOMJS_PATH)
response = raw_input("Please enter the name of the Company: ")
print crawlSiftery(browser,response)
print crawlGoogle(browser,response)


browser.quit()