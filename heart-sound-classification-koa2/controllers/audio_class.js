const DB = require("../dbhelper/db_high");
const md5 = require("md5");
const Token = require("../token");
const {exec} = require("child_process");

//1登录
exports.login = async (ctx, next) => {
        let req = ctx.request.body;
        let id = req.id;
        let password = md5(req.password);
        let result = await DB.find(`id="${id}"`);
        if (result.length != 0) {
                if (password == result[0].password) {
                        let token = await Token.encrypt({ id: id }, 60 * 60 * 24 * 7);
                        // console.log(token);
                        if (token) {
                                ctx.body = {
                                        code: 0,
                                        result: "登录成功",
                                        token: token
                                }
                        } else {
                                ctx.body = {
                                        code: 1,
                                        result: "登录失败，获取token失败"
                                }
                        }
                } else {
                        ctx.body = {
                                code: 2,
                                result: "登录失败，密码错误"
                        }
                }
        } else {
                ctx.body = {
                        code: 3,
                        result: "失败，该账户未注册"
                }
        }
}

//2注册
exports.register = async (ctx, next) => {
        let req = ctx.request.body;
        let id = req.id;
        let password = md5(req.password);
        let name = req.name;
        let age = req.age;
        let gender = req.gender;
        let  history = req.history

        if (req.password.length >= 6) {
                let result = await DB.find(`id="${id}"`);
                if (result.length == 0) {
                        try {
                                await DB.addinfo(`"${id}","${password}","${name}",${age},${gender},${history}`);
                        } catch{
                                ctx.body = {
                                        code: 1,
                                        result: "注册失败"
                                }
                                return;
                        }
                        ctx.body = {
                                code: 0,
                                result: "注册成功，请前去登录 "
                        }
                } else {
                        ctx.body = {
                                code: 2,
                                result: "该用户id已注册，请直接登录或更换用户id"
                        }
                }
        } else {
                ctx.body = {
                        code: 3,
                        result: "密码长度少于6位，注册失败"
                }
        }

}


exports.UploadForm = async (ctx,next) => {
        let req = ctx.request.body;
        let id = ctx.request.id;
        let wav_address = req.wav_address;
        try {
                const classresult = exec(`python ./model_predict/predict.py  ${wav_address}`, (error, stdout, stderr) => {
                        if (error) {
                          console.error(`执行 Python 脚本时发生错误: ${error.message}`);
                          return;
                        }
                        if (stderr) {
                          console.error(`Python 脚本执行过程中出现错误: ${stderr}`);
                          return;
                        }
                        // 输出 Python 脚本的返回值
                        console.log(`Python 函数返回值: ${stdout}`);

                        addnpy_result = DB.addrecord(`"${id}", "${wav_address}", "${formatDate()}", ${stdout}`)
                        
                        ctx.body = {
                                code:0,
                                stdout:stdout,
                                result:"存入wav和结果成功"
                        }
                      });
        }catch{
                ctx.body = {
                        code:1,
                        result:"存入wav和结果失败"
                }
        }
        
}


exports.HistorySearch = async (ctx,next) => {
        let req = ctx.request.body;
        let id = req.id;
        try {
                history_result = await DB.find_history(id)
        }catch{
                ctx.body = {
                        code:1,
                        result:"搜索历史记录失败"
                }
        }
        ctx.body = {
                code:0,
                history_result:history_result,
                result:"搜索历史记录成功"
        }

}


// 使用函数将日期格式化为 "YYYY/MM/DD HH:mm" 格式
function formatDate() {
        // 获取当前日期时间
        date = new Date()
        // 获取年
        let year = date.getFullYear();
        
        // 获取月，月份从 0 开始计数，所以需要加 1
        let month = date.getMonth() + 1;
        // 如果月小于 10，补零
        if (month < 10) {
        month = '0' + month;
        }
        
        // 获取日
        let day = date.getDate();
        // 如果日小于 10，补零
        if (day < 10) {
        day = '0' + day;
        }
        
        // 获取小时
        let hours = date.getHours();
        // 如果小时小于 10，补零
        if (hours < 10) {
        hours = '0' + hours;
        }
        
        // 获取分钟
        let minutes = date.getMinutes();
        // 如果分钟小于 10，补零
        if (minutes < 10) {
        minutes = '0' + minutes;
        }
        
        // 格式化日期时间为 "YYYY/MM/DD HH:mm"
        return `${year}/${month}/${day} ${hours}:${minutes}`;
}