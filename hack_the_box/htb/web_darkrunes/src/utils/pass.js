const { generateRandomString, generateAccessCode } = require("./crypto");
const fs = require("fs");

let ACCESS_PASS = generateRandomString(32);

/**
 * @dev for now this software is run on the admin laptop ( which should be never turned off ). So we can avoid using email and use simple files :D which is moooooore secure and headache free.
 */
const rotatePass = () => {
    try {
        if (fs.existsSync(String(ACCESS_PASS)))
            fs.unlinkSync(String(ACCESS_PASS));
        ACCESS_PASS = generateAccessCode();
        fs.writeFileSync(
            String(ACCESS_PASS),
            `You Access Code is "${generateRandomString(4)}". Please use it to access the debug features`,
        );
    } catch (e) {
        console.error("Error generating pass", e);
    }
};

const verifyPass = (pass) => {
    try {
        if (!fs.existsSync(ACCESS_PASS)) return false;

        const currName = fs.readFileSync(ACCESS_PASS, { encoding: "utf-8" });

        if (currName.length === 0) return false;

        return ACCESS_PASS === pass;
    } catch (e) {
        return false;
    }
};

module.exports = { verifyPass, rotatePass };
