const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const axios = require('axios');

// Generate RSA key pair
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
    publicKeyEncoding: {
        type: 'spki',
        format: 'pem'
    },
    privateKeyEncoding: {
        type: 'pkcs8',
        format: 'pem'
    }
});

// Create JWKS
const jwks = {
    keys: [
        {
            kty: 'RSA',
            kid: 'evil-core-key-1',
            n: Buffer.from(publicKey).toString('base64url'),
            e: 'AQAB'
        }
    ]
};

// JWT signing function with default JKU header
const signToken = (payload) => {
    return jwt.sign(payload, privateKey, {
        algorithm: 'RS256',
        keyid: 'evil-core-key-1',
        header: {
            jku: 'http://localhost:3000/.well-known/jwks.json'
        }
    });
};

// JWT verification function with JKU support
const verifyToken = async (token) => {
    try {
        const header = JSON.parse(Buffer.from(token.split('.')[0], 'base64url').toString());
        
        // Check if token has JKU header
        if (header.jku) {
            // Verify JKU URL is from localhost:3000
            const jkuUrl = new URL(header.jku);
            if (jkuUrl.host !== 'localhost:3000') {
                throw new Error('Invalid JKU host');
            }

            try {
                // Fetch JWKS from JKU URL
                const jwksResponse = await axios.get(header.jku);
                const jwks = jwksResponse.data;

                // Find matching key
                const key = jwks.keys.find(k => k.kid === header.kid);
                if (!key) {
                    throw new Error('No matching key found');
                }

                // Convert JWK to PEM
                const jwkToPem = require('jwk-to-pem');
                const publicKey = jwkToPem(key);

                // Verify token with fetched key
                return jwt.verify(token, publicKey, {
                    algorithms: ['RS256']
                });
            } catch (error) {
                console.error('Error fetching JWKS:', error);
                // Fallback to default verification if JWKS fetch fails
                return jwt.verify(token, publicKey, {
                    algorithms: ['RS256']
                });
            }
        }

        // If no JKU, use default verification
        return jwt.verify(token, publicKey, {
            algorithms: ['RS256']
        });
    } catch (error) {
        console.error('JWT verification error:', error);
        return null;
    }
};

module.exports = {
    jwks,
    signToken,
    verifyToken
}; 