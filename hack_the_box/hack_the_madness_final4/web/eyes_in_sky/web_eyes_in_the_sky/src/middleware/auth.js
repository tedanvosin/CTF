const { verifyToken } = require('../utils/jwt');

const authMiddleware = async (req, res, next) => {
    const token = req.cookies.jwt;
    
    if (!token) {
        return res.redirect('/next?url=/unauthorized');
    }

    const decoded = await verifyToken(token);

    if (!decoded) {
        return res.redirect('/next?url=/unauthorized');
    }

    req.user = decoded;
    next();
};

module.exports = authMiddleware; 