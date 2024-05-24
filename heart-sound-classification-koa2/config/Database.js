const mysql = require("mysql");


let config = mysql.createConnection({
    host: "localhost",   // 数据库的地址
    user: "root",        // 数据库用户名
    password: "123456789",    // 数据库密码
    port: "3306",        // mysql数据库的端口号
    database: "heartsound"      // 使用那个数据库
})

config.connect();
console.log("数据库连接成功");

module.exports = config;
