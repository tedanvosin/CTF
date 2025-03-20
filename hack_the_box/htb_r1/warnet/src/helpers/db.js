import { Sequelize } from "sequelize";
import bcrypt from "bcryptjs";

const sequelize = new Sequelize({
    dialect: "sqlite",
    storage: "./db.sqlite"
});

const db = {};

db.sequalize = sequelize;

db.users = sequelize.define("user", {
    id: {
        type: Sequelize.INTEGER,
        autoIncrement: true,
        primaryKey: true,
        allowNull: false,
        unique: true,
    },
    callsign: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true,
    },
    password: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    godMode: {
        type: Sequelize.BOOLEAN,
        allowNull: false,
        default: false,
    },
}, {
    hooks: {
        beforeCreate: (record, options) => {
            record.dataValues.password = bcrypt.hashSync(record.dataValues.password, 10);
        }
    }
})

export default db;