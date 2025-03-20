import { Router } from "express"

const router = Router();

router.get("/", (req, res) => {
    res.render("home");
});

router.get("/exploitation", (req, res) => {
    res.render("exploitation-guide");
});

export default router;