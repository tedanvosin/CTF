import { Router } from "express";
import fs from "node:fs";
import authMiddleware from "../middleware/auth.js";

const router = Router();

let flag;

try {
    flag = fs.readFileSync("./flag.txt", "utf8");
} catch (err) {
    console.error(err, "no admin route will be loaded");
}

router.get("/admin", authMiddleware, async (req, res) => {
    res.render("admin", { flag });
});

export default router;