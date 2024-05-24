/**
 * 前端路由表
 */
const router = require('koa-router')();
const audio_class = require("./controllers/audio_class");

// 注册 填写基本信息
router.post("/login",audio_class.login);
// 登录
router.post("/register",audio_class.register);
// 上传文件和结果
router.post("/UploadForm",audio_class.UploadForm);
// 搜索历史记录
router.post("/HistorySearch",audio_class.HistorySearch);


module.exports = router.routes();



