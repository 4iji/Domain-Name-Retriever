#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from difflib import SequenceMatcher
from collections import defaultdict
import neural_network as nn
import numpy as np
import operator

import json
with open('../config.json') as config_file:    
    config = json.load(config_file)
# Similarity Score
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
# Construct Feature Vector
def constructInputMatrix(sifteryResults,googleResults,linkedinResults):
	output = defaultdict(list)
	for result in sifteryResults:
		output[result].append(sifteryResults[result])
	for result in googleResults:
		if(not result in output):
			output[result].append(0)
		output[result].append(googleResults[result])
	for result in linkedinResults:
		if(not result in output):
			output[result].append(0)
		if(len(output[result])==1):
			output[result].append(0)
		output[result].append(linkedinResults[result])
	for result in output:
		if(len(output[result])==1):
			output[result].append(0)
		if(len(output[result])==2):
			output[result].append(0)
	return output
# Siftery Crawler
def crawlSiftery(browser,queryParam):
	url = "https://siftery.com/search?q="+queryParam
	browser.get(url);
	soup = BeautifulSoup(browser.page_source,"html.parser")
	companies = soup.find_all("div",{"class":"list-group-item__info"},limit=config['limit']['siftery'])
	output = {}
	for company in companies:
		try:
			title = company.find('h5',{'class':'list-group-item__title'}).text
			link = company.find('span',{'class':'primary-text ng-binding'}).text #skips product pages, only consider company pages
			link = link.split("//")[-1].split("/")[0]
			output[link]=-1
			output[link]=max(output[link],round(similar(title,queryParam),2))
		except AttributeError:
			continue
	return output
#Google Crawler
def crawlGoogle(browser,queryParam):
	#Ignoring facebook,linkedin and twitter results
	url = "https://www.google.co.in/search?q="+queryParam+"+-facebook+-twitter+-linkedin+-wikipedia&tbs=li:1" #The end part is to enable verbatim search
	browser.get(url);
	soup = BeautifulSoup(browser.page_source,"html.parser")
	companies = soup.find_all('div',{'class':'g'})
	output = {}
	for company in companies:
		link = company.find('cite').text
		link =  link.split("//")[-1].split("/")[0]
		title = company.find('h3',{'class':'r'}).find('a').text
		output[link]=-1
		output[link]=max(output[link],round(similar(title,queryParam),2))
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
				output[link]=max(output[link],round(similar(title,queryParam),2))
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
candidates = constructInputMatrix(sifteryVector,googleVector,linkedInVector)
#Intialise a single neuron neural network.
neural_network = nn.NeuralNetwork()
training_set_inputs = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 1], [0, 0, 0]])
training_set_outputs = np.array([[0, 1, 1, 0]]).T

# Train the neural network using a training set.
# Do it 10,000 times and make small adjustments each time.
neural_network.train(training_set_inputs, training_set_outputs, 10000)
# Test the neural network with a new situation.
output = {}
for result in candidates:
	output[result] = neural_network.think(np.array(candidates[result]))
sorted_output = sorted(output.items(), key=operator.itemgetter(1))
print sorted_output
browser.quit()