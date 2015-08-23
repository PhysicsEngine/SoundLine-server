var fs = require('fs');
var child_process = require('child_process');

var express = require('express');
var morgan = require('morgan');
var multer = require('multer');
var bodyParser = require('body-parser');
var pg = require('pg');
var mkdirp = require('mkdirp');
var app = express();

/**
 *  File upload configuration of multer.
 *  Targt dir is './uploads' and file limit size 10MB.
 */
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
    var filter = req.body.filter;
    var now = new Date();
    var tmpPath = req.file.path;
    var targetPath = './uploads/' + username + '/' + now.getTime() +
            '-' + req.file.originalname;
    var convertedPath = './uploads/' + username + '/' + 'converted-' +
            now.getTime() + '-' + req.file.originalname + '.mp3';
    mkdirp('./uploads/' + username, function(err, result) {
        if (err) {
            throw err;
        }
        fs.rename(tmpPath, targetPath, function(err) {
            if (err) {
                throw err;
            }
            res.send("File uploaded to " + targetPath);

            child = child_process.execFile('python',
                ['./convert.py', targetPath, convertedPath, filter],
                function(err, stdout, stderr) {
                if (err) {
                    throw err;
                }
                console.log(stdout);
                fs.unlink(targetPath, function(err) {
                    if (err) {
                        throw err;
                    }
                });
            });
        });
    });
});

app.get('/converted/:username/:filename', function(req, res, next) {
    var filename = req.params.filename;
    var username = req.params.username;
    console.log("Download " + filename);
    res.download('./uploads/' + username + '/' + filename);
});

function compareUserTime(u1, u2) {
    var pattern = /converted-([0-9]+)-.+\.mp3/;
    var time1 = pattern.exec(u1.filename);
    var time2 = pattern.exec(u2.filename);
    if (time1 != null && time2 != null) {
        if (time1[1] > time2[1]) {
            return -1;
        } else {
            return 1;
        }
    }
    return 0;
}

String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

String.prototype.startsWith = function(prefix) {
    return this.indexOf(prefix) === 0;
}

app.get('/list', function(req, res, next) {
    fs.readdir('./uploads', function(err, users) {
        var ret = [];
        for (var i = 0; i < users.length; i++) {
            var userDir = fs.statSync('./uploads/' + users[i]);
            if (userDir.isDirectory()) {
                var username = users[i];
                var filenames = fs.readdirSync('./uploads/' + users[i]);
                for (var j = 0; j < filenames.length; j++) {
                    if (!filenames[j].endsWith("xml") && filenames[j].startsWith("converted")) {
                        ret.push({user: username, filename: filenames[j]});
                    }
                }
            }
        }
        ret.sort(compareUserTime);
        res.json({users: ret});
    });
});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});


