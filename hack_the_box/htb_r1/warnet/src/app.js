import express from "express";
import expressEjsLayouts from "express-ejs-layouts";
import cookieParser from "cookie-parser";
import { randomBytes } from "crypto"

import viewsRouter from "./routes/views.js";
import authRouter from "./routes/auth.js";
import adminRouter from "./routes/admin.js";

const app = express();

app.use(express.json());
app.use(express.urlencoded({extended: true}));

app.set("view engine", "ejs");
app.use(expressEjsLayouts);
app.set("layout", "./layouts/layout");

app.use(cookieParser(randomBytes(128).toString("hex")));

app.use(viewsRouter);
app.use(authRouter);
app.use(adminRouter);

export default app;