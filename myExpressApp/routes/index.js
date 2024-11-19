var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Home' });
});

router.get('/home', (req, res) => {
  res.render('home', {title: 'LandingPage'})
});

router.get('/news', (req, res) => {
  res.render('news', { title: 'News' });
});

router.get('/matchups', (req, res) => {
  res.render('matchups', { title: 'Matchups' });
});

router.get('/AFCTeams', (req, res) => {
  res.render('AFCTeams', { title: 'AFCTeams' });
});

router.get('/NFCTeams', (req, res) => {
  res.render('NFCTeams', { title: 'NFCTeams' });
});

router.get('/PowerRankings', (req, res) => {
  res.render('PowerRankings', { title: 'PowerRankings' });
});

module.exports = router;
