const path = require('path');

const getHomePage = (req, res) => {
    res.sendFile(path.join(__dirname, '../templates', 'index.html'));
};

const getDashboardPage = (req, res) => {
    res.sendFile(path.join(__dirname, '../templates', 'dashboard.html'));
};

const getUnauthorizedPage = (req, res) => {
    res.sendFile(path.join(__dirname, '../templates', 'unauthorized.html'));
};

const handleNext = (req, res) => {
    const url = req.query.url;
    res.redirect(url);
};

module.exports = {
    getHomePage,
    getDashboardPage,
    getUnauthorizedPage,
    handleNext
}; 