import { randomBytes } from "crypto";

export const users = [
    {
        id: 1,
        callsign: "admin",
        password: randomBytes(16).toString("hex"),
        godMode: true
    }
];