#Domain Name Retrival using Neural Network
The Aim of this project is to predict the domain (website) name, given the name of the company.

*Input*: Company Name<br>
*Output*: Domain of the company.

examples:


1) Microsoft
    microsoft.com

2) Split an Atom
    splitanatom.com

3) Guru Technologies
    getguru.com

4) Outwork
    outwork.com

5) Total Pest
    totalpest.co

##Approach
###Parsers / Crawlers
To solve the following problem, Three crawler functions have been written in main.py file
```python
crawlGoogle(browser,queryParam)
crawlLinkedin(browser,queryParam)
crawlSiftery(browser,queryParam)
```
These functions make use of a parsing library in Python, Beautiful Soup and PhantomJs to parse (Title of the Company, Link to the Company Home Page). The output of these functions is a website link and asimliarty score between the title parsed and the name of the company given as input. 

###Neural Network
A neural network (actually a single neuron) was used for training and testing. It has 3 input connections and a single output connection. It follows a backpropogation mecahnism to obtain the weights of the synapse. The input to this network is a custom dictionary which has list of candidate websites as the "key" and a list of similarity scores obtained by that website in Siftery,Google and Linkedin Respectively. The nonlinear function used 

[Reference](http://iamtrask.github.io/2015/07/12/basic-python-network/)<br>
*Currently the data is being trained through a logical matrix, which gives more weight to Linkedin Results > Siftery Results > Google Results
##TODO
- To modify google results to be more rich
- Add Angel.co and Glassdoor parsers
- Train the NN using actual data