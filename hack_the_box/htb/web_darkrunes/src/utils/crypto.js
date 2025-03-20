const crypto = require("crypto");

const generateRandomString = (length = 16) =>
  crypto.randomBytes(length).toString("hex");

const SECRET = generateRandomString(32);

const createHash = (s) => crypto.createHash("sha256").update(s).digest("hex");

const signString = (s) =>
  crypto
    .createHash("sha256")
    .update(s + SECRET)
    .digest("hex");

const generateCookie = (username, id) => {
  const stringifiedUser = btoa(JSON.stringify({ username, id }));
  const sig = signString(stringifiedUser);
  return `${stringifiedUser}-${sig}`;
};

const validate = (s) => {
  const parts = s.split("-");
  if (parts.length !== 2) return false;
  return signString(parts[0]) === parts[1];
};

const generateAccessCode = () => {
  const randomBytes = crypto.randomBytes(2);
  const secureCode = (randomBytes.readUInt16BE() % 10000)
    .toString()
    .padStart(4, "0");

  return secureCode;
};

module.exports = {
  generateCookie,
  createHash,
  signString,
  validate,
  generateRandomString,
  generateAccessCode,
};
