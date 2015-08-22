var fs = require('fs');

var express = require('express');
var multer = require('multer');
var app = express();

var upload = multer({dest: './uploads/'});

app.set('port', (process.env.PORT || 5000));

app.use(express.static(__dirname + '/public'));

// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.get('/', function(request, response) {
    response.render('pages/index');
});

app.get('/upload-debug', function(req, res) {
    res.render('pages/upload-debug');
});

app.post('/upload', upload.single('file'), function(req, res, next) {
    var tmpPath = req.file.path;
    var targetPath = './uploads/' + req.file.originalname;
    console.log(tmpPath);
    fs.rename(tmpPath, targetPath, function(err) {
        if (err) {
            throw err;
        }
        res.send("File uploaded to " + targetPath);
    });
});

app.get('/converted/:filename', function(req, res, next) {
    var filename = req.params.filename;
    console.log("Download " + filename);
    res.download('./uploads/' + filename);
});

app.get('/list', function(req, res, next) {
    fs.readdir('./uploads', function(err, list) {
        console.log(list);
        var ret = {};
        ret['list'] = list;
        res.json(ret);
    });
});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});


