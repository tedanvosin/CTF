const { validate } = require("./utils/crypto");

const isAuthenticated = (req, res, next) => {
  const token = req.cookies.user;

  if (!token) {
    return res.status(401).send("Unauthorized");
  }

  if (!validate(token)) {
    return res.status(401).send("Unauthorized");
  }

  const user = JSON.parse(atob(token.split("-")[0]));
  req.user = user;

  return next();
};

const isAdmin = (req, res, next) => {
  if (req.user.username === "admin") {
    return next();
  }

  return res.status(403).send("Forbidden");
};

module.exports = { isAuthenticated, isAdmin };
