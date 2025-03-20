const express = require("express");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const authRouter = require("./routes/auth");
const documentsRouter = require("./routes/documents");
const generateRouter = require("./routes/generate.js");
const path = require("path");
const { rotatePass } = require("./utils/pass.js");

const app = express();

const PORT = process.env.PORT || 3000;

app.set("view engine", "ejs");
app.set("views", path.join(process.cwd(), "views"));

app.use(express.static(path.join(process.cwd(), "static")));

app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());

app.use(authRouter);
app.use(documentsRouter);
app.use(generateRouter);

app.listen(PORT, () => {
  rotatePass();
  console.log(`Server started on port ${PORT}`);
});
