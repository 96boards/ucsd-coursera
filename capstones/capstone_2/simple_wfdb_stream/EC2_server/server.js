//Require all the modules
var request = require('request'); 		//For http requests
var app = require('express')();			//For web server application
var server = require('http').createServer(app);	//For web server

//When a GET request with url '/' is received do this
//@param req	Request that is received
//@param res	Response that will be sent back
app.get('/', function(req, res){
	//Send the file index.html
	res.sendfile('index.html');
	console.log("Sent index.html");
});

app.get('/data', function(req, res){
	//URL of AWS API Gateway	
	var url = 'https://136q0h985h.execute-api.us-west-2.amazonaws.com/prod';

	//Makes a GET request to the url and does the following
	request(url, function (error, response, body) {
		//If there is no error and the response code is correct, do this
		if (!error && response.statusCode == 200) {
        		console.log("Sent JSON data:", body);
			res.send(body); //Send the body of the data received 
		}//END if
	});//END request
});//END app.get

//Sets the port that we will be listening onto 80 (80 is the common HTTP port that browsers will usually access).
var port = 80;
//Server listens for any requests
server.listen(port, function(){
	console.log('App listening on port 80');
});
