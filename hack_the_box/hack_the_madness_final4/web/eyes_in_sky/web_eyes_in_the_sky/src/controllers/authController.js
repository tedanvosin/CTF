const { signToken } = require('../utils/jwt');

const login = async (req, res) => {
    const { username, password } = req.body;
    
    if (username === 'admin' && password === process.env.ADMIN_PASSWORD) {
        // Generate JWT token
        const token = signToken({
            username,
            role: 'admin',
            iat: Math.floor(Date.now() / 1000),
            exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 hours
        });

        // Set JWT as HTTP-only cookie
        res.cookie('jwt', token, {
            httpOnly: true,
            sameSite: 'strict',
            maxAge: 24 * 60 * 60 * 1000 // 24 hours
        });

        res.json({ 
            success: true, 
            message: 'Login successful'
        });
    } else {
        res.status(401).json({ success: false, message: 'Invalid credentials' });
    }
};

const logout = (req, res) => {
    // Clear the JWT cookie
    res.clearCookie('jwt', {
        httpOnly: true,
        sameSite: 'strict'
    });
    res.json({ success: true, message: 'Logged out successfully' });
};

module.exports = {
    login,
    logout
}; 