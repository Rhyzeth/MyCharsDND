var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Home' });
});

router.get('/home', (req, res) => {
  res.render('home', {title: 'Home'})
});

router.get('/news', (req, res) => {
  res.render('news', { title: 'News' });
});

router.get('/matchups', (req, res) => {
  res.render('matchups', { title: 'Matchups' });
});

module.exports = router;
