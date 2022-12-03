const express = require('express');
const fileUpload = require('express-fileupload');
const multer = require('multer');
const bodyParser= require('body-parser')

const storage = multer.diskStorage({
	destination: function(req, file, cb) {
		cb(null, '/tmp/upload/');
	},
	filename: function(req, file, cb){
		cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
	}
});



const upload = multer({storage: storage});

const app = express();
app.use(fileUpload());

function verifyFileExtension(fileName){
	var validExtensions = ["txt","ini", "sql", "c", "php", "cpp", "js", "r", "ru", "py"];
	for(var i = 0; i < validExtensions.length; i++){
		fileExtension = fileName.split('.').pop();
		if(fileExtension == validExtensions[i]){
			return true;
		}
	}
	return false;
}

function verifyPath(fileName){
	if(fileName.includes("..")){
		return false;
	}
	return true;
}

async function verifyFile(fileName){
	if(!verifyFileExtension(fileName)){
		return false;
	}
	// Do some other verification based on different things. E.g. calling external validation services
	// ...
	// ...
	// ...
}

function verifyName(fileName){
	//
	// ...
	//
	return true;
}


app.get('/upload', function(req, res){
	res.send('<form action="/upload-file" method="POST" enctype="multipart/form-data">File: <input type="file" name="fileZ" /><br /><input type="submit" value="submit"/><br /></form>');
	res.end();
});


app.post('/upload-file', upload.single('fileZ'), (req, res) => {
	try {
		const fileZ = req.files;
		console.log(req.files);
		if(!fileZ){
			res.status(400).send({
				status: false,
				data: 'No file uploaded.'
			});
			res.end();
		} else {
			// Do some data manipulation 
			// ...
			// ...
		}

		var file = fileZ[Object.keys(req.files)[0]];
		var verified = verifyPath(file.name);
		if(!verified){
			throw new Error('[PATH] ERROR, FILE CANNOT BE VERIFIED!');
		}

		verified = verifyName(file.name);
		if(!verified){
			throw new Error('[NAME] ERROR, FILE CANNOT BE VERIFIED!');
		}

		verified = verifyFile(file.name);
		if(!verified){
			throw new Error('[FILE] ERROR, FILE CANNOT BE VERIFIED!');
		}else{
			// Do another calculations
			// ...
			// ...
			// ...
		}
		res.send('File upload - success!');
		res.end();
	} catch (err){
		res.status(500).send(err);
		console.log(err);
	}
});


function log(msg) {
	console.log(msg);
}

const PORT = process.env.PORT || 9876;
let server = app.listen(PORT, () => log('Server running on: ' + PORT));
