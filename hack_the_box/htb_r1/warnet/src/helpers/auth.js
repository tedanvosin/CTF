import crypto from "crypto";
import jwt from "jsonwebtoken";

const secretKey = crypto.randomBytes(64 / 2).toString("hex").slice(0, 128);

const getUserId = (sessionCookie) => {
    try {
        const session = jwt.verify(sessionCookie, secretKey);
        return session.id;
    } catch (err) {
        return null;
    }
};

export { secretKey, getUserId };