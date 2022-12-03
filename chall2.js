const express = require('express')

const PID = process.pid;

const crypto = require('crypto');


// This specific function is only used in this file and nowhere else
function log(msg) {
	console.log(`[${PID}]` ,new Date(), msg);
}

const app = express();

app.get('/apphealth', function apphealth(req, res){
	log("Initiated health checking");
	res.send("Server is working\n");
});

function generateRandomString(){
	return crypto.randomBytes(200).toString('hex');
}


app.get('/computehash', function computehash(req, res){
	if(typeof req.query.iter === 'undefinied'){
		var iter = 10;
	}else{
		var iter = req.query.iter;
	}
	const hash = crypto.createHash('sha512');
	for(let i = 1; i < iter; i++){
		hash.update(generateRandomString());
	}
	res.send(hash.digest('hex') + "\n");
});

app.get('/helloworld', function helloworld(req, res){
	param = req.query.val;
	if(param){
		safePram = encodeURIComponent(param)
			.replace(/&#126;/g, '+')
            .replace(/%20/g, '+')
            .replace(/%3C/g, '&lt;')
            .replace(/%3E/g, '&gt;')
            .replace(/%3D/g,'=');
		res.send("Hello World. Here is a link to helloworld page : <a href='/" + safePram +  "'/>Click!</a>");
	}else{
		res.send('Provide a param');
	}
});


const PORT = process.env.PORT || 9876;
let server = app.listen(PORT, () => log('Server running on: ' + PORT));