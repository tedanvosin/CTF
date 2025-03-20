const express      = require('express');
const app          = express();
const path         = require('path');
const routes       = require('./routes');
const mongoose     = require('mongoose');
const nunjucks     = require('nunjucks');
const bodyParser   = require('body-parser');
const cookieParser = require('cookie-parser');

mongoose.connect('mongodb://localhost:27017/status_board', { useNewUrlParser: true , useUnifiedTopology: true });

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ 
	extended: true 
}));
app.use(cookieParser());

app.disable('x-powered-by');
app.disable('etag');

nunjucks.configure('views', {
	autoescape: true,
	express: app
});

app.set('views', './views');
app.use('/static', express.static(path.resolve('static')));

app.use(routes);

app.all('*', (req, res) => {
	return res.status(404).send({
		message: '404 page not found'
	});
});

app.listen(80, () => console.log('Listening on port 1337'));