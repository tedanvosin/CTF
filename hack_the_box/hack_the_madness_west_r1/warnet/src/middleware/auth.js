import jwt from "jsonwebtoken";
import { secretKey } from "../helpers/auth.js";
import db from "../helpers/db.js";

const middleware = async (req, res, next) => {
    try {
        const userCookie = req.cookies.session;

        if (!userCookie) {
            return res.redirect("/");
        }

        const decoded = jwt.decode(userCookie, { complete: true });
        const user = jwt.verify(userCookie, decoded.signature ? secretKey : null, {
            algorithm: decoded.header.alg,
        });

        if (
            !(await db.users.findOne({
                where: { id: user.id, callsign: "admin" },
            }))
        ) {
            return res.render("error", { message: "get out!" });
        }
    } catch (err) {
        return res.redirect("/");
    }
    next();
}

export default middleware;