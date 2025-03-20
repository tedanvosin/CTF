import app from "./app.js";
import db from "./helpers/db.js";
import { users as usersSeed } from "./db_seed.js";

const PORT = 1337;

const start = async () => {
    try {
        await db.users.sync({ force: true });
        usersSeed.forEach(async (u) => {
            await db.users.create(u);
        });
        db.sequalize.authenticate();
        app.listen(1337, () => {
            console.log("app is running at port", PORT);
        })
    } catch (error) {
        console.error("oops", error);
    }
}

start();