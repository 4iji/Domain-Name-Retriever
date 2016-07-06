var array =[];
var websites = $(".website a")

for(var i = 0; i < websites.length; i++) {
	var name = $(".photo img")[i].getAttribute("alt")
	var website = websites[i];
	var object={};
	object["name"]=name;
	object["website"]=website.text
	array.push(object)
} 
