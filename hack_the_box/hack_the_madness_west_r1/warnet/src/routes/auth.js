import { Router } from "express"
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import db from "../helpers/db.js";
import { secretKey } from "../helpers/auth.js";

const router = Router();

router.get("/login", (req, res) => {
    res.render("login")
});

router.get("/register", (req, res) => {
    res.render("register");
});

router.post("/login", async (req, res) => {
    if (typeof req.body === "undefined") return res.render("error", { message: "please provide valid data." });

    const { callsign, password } = req.body;

    const user = await db.users.findOne({
        where: { callsign }
    });

    if (!user) return res.render("error", { message: "there is no organization member by that callsign." });

    if(!bcrypt.compareSync(password, user.password)) return res.render("error", { message: "provide a valid personnel provided."});

    const token = jwt.sign({ id: user.id, callsign: user.callsign, god_mode: user.godMode }, secretKey, {
        expiresIn: "1h",
    });

    res.cookie("session", token);

    res.render("message", { message: "logged in." });
})

router.post("/register", async (req, res) => {
    if (typeof req.body === "undefined") return res.render("error", { message: "please provide valid data." });

    const { callsign, password, confirm_pass: confirmPass } = req.body;

    if (password !== confirmPass) return res.render("error", { message: "passwords must be identical." });

    const possibleUser = await db.users.findOne({
        where: { callsign }
    });

    if (possibleUser) return res.render("error", { message: "callsign already used by personnel" });

    await db.users.create({
        callsign,
        password,
        godMode: false,
    });
    return res.render("message", { message: "registered successfully." });
});

export default router;