var fs = require('fs');
var child_process = require('child_process');

var express = require('express');
var morgan = require('morgan');
var multer = require('multer');
var bodyParser = require('body-parser');
var pg = require('pg');
var mkdirp = require('mkdirp');
var app = express();

var upload = multer({
    dest: './uploads/',
    limits: {
        fieldSize: '10MB'
    }
}).single('file');

app.set('port', (process.env.PORT || 5000));

app.use(express.static(__dirname + '/public'));
app.use(morgan('dev', {immediate: true}));
app.use(bodyParser.urlencoded({extended: false}));

// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.get('/', function(request, response) {
    response.render('pages/index');
});

app.get('/upload-debug', function(req, res) {
    res.render('pages/upload-debug');
});

app.post('/upload', upload, function(req, res, next) {
    var username = req.body.username;
    console.log(req.file);
    var tmpPath = req.file.path;
    var targetPath = './uploads/' + username + '/' + (new Date()).getTime() + '-' + req.file.originalname;
    mkdirp('./uploads/' + username, function(err, result) {
        if (err) {
            throw err;
        }
        fs.rename(tmpPath, targetPath, function(err) {
            if (err) {
                throw err;
            }
            res.send("File uploaded to " + targetPath);

            /**
            child = child_process.execFile('python', ['./converter/saveload.py', targetPath, targetPath + '.converted'], function(err, stdout, stderr) {
                if (err) {
                    throw err;
                }
                console.log(stdout);
            });
             */
        });
    });

    /**
    pg.connect(process.env.DATABASE_URL, function(err, client, done) {
        client.query('INSERT INTO converted VALUES ("' + username + '","' + targetPath + '"', function(err, result) {
            fs.rename(tmpPath, targetPath, function(err) {
                if (err) {
                    throw err;
                }
                res.send("File uploaded to " + targetPath);
            });
        });
    });
     */
});

app.get('/converted/:username/:filename', function(req, res, next) {
    var filename = req.params.filename;
    var username = req.params.username;
    console.log("Download " + filename);
    res.download('./uploads/' + username + '/' + filename);
});

app.get('/list', function(req, res, next) {
    fs.readdir('./uploads', function(err, users) {
        var ret = [];
        for (var i = 0; i < users.length; i++) {
            var userDir = fs.statSync('./uploads/' + users[i]);
            if (userDir.isDirectory()) {
                var username = users[i];
                var filenames = fs.readdirSync('./uploads/' + users[i]);
                for (var j = 0; j < filenames.length; j++) {
                    ret.push({user: username, filename: filenames[j]});
                }
            }
        }
        res.json({users: ret});
    });
});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});


