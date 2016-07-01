#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from difflib import SequenceMatcher

import json
with open('../config.json') as config_file:    
    config = json.load(config_file)
# Similarity Score
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
# Construct Feature Vector
def constructFeatureMatrix(companyName,sifteryResults,googleResults):
	return 1
# Siftery Crawler
def crawlSiftery(browser,queryParam):
	url = "https://siftery.com/search?q="+queryParam
	browser.get(url);
	soup = BeautifulSoup(browser.page_source,"html.parser")
	companies = soup.find_all("div",{"class":"list-group-item__info"},limit=config['limit']['siftery'])
	output = {}
	for company in companies:
		title = company.find('h5',{'class':'list-group-item__title'}).text
		link = company.find('div',{'class':'list-group-item__text'}).text
		link = link.split("//")[-1].split("/")[0]
		output[link]=-1
		output[link]=max(output[link],similar(title,queryParam))
	return output


		
#Google Crawler
def crawlGoogle(browser,queryParam):
	url = "https://www.google.co.in/search?q="+queryParam+"&tbs=li:1" #The end part is to enable verbatim search
	browser.get(url);
	soup = BeautifulSoup(browser.page_source,"html.parser")
	companies = soup.find_all('div',{'class':'g'})
	output = {}
	for company in companies:
		link = company.find('cite').text
		link =  link.split("//")[-1].split("/")[0]
		title = company.find('h3',{'class':'r'}).find('a').text
		output[link]=-1
		output[link]=max(output[link],similar(title,queryParam))
	return output
#LinkedIn Crawler
def crawlLinkedin(browser,queryParam):
	url = "https://www.google.co.in/search?q="+queryParam+"+:www.linkedin.com/company"
	browser.get(url);
	soup = BeautifulSoup(browser.page_source,"html.parser")
	companies = soup.find_all('div',{'class':'g'},limit=config['limit']['linkedin'])
	output ={}
	for company in companies:
		linkedInURL = company.find('cite').text
		linkedInURL_copy = linkedInURL
		if linkedInURL_copy.split("//")[1].split("/")[0]=="www.linkedin.com" and linkedInURL_copy.split("//")[1].split("/")[1]=="company" :
			browser.get(str(linkedInURL))
			newSoup = BeautifulSoup(browser.page_source,"html.parser")
			try:
				title = newSoup.find("h1",{"class":"name"}).find('span').text
				link = newSoup.find("li",{"class":"website"}).find("a").text
				link =  link.split("//")[-1].split("/")[0]
				output[link]=-1
				output[link]=max(output[link],similar(title,queryParam))
			except AttributeError:
				continue #skip to the next loop.
	return output
			
#Main code goes here
PHANTOMJS_PATH = config['phantomJSPath']
browser = webdriver.PhantomJS(PHANTOMJS_PATH)
companyName = raw_input("Please enter the name of the Company: ")
sifteryVector = crawlSiftery(browser,companyName)
googleVector = crawlGoogle(browser,companyName)
linkedInVector = crawlLinkedin(browser,companyName)
browser.quit()