const config = require('../config/Database');


// 增加个人信息
exports.addinfo = function (addSqlParams) {
  let sql = "INSERT INTO info (id, password, name, age, gender) VALUES (?,?,?,?,?);";
  return new Promise(function (resolve, reject) {
    config.query(sql, addSqlParams, function (err, result) {
      if (err) {
        reject(err);
      }
      resolve(result);
      console.log(result);
    })
  })
}


// 增加个人心音特征文件
exports.addrecord = function (addSqlParams) {
  let sql = "INSERT INTO feature_result (id, npy_address, data, result) VALUES (?,?,?,?);";
  return new Promise(function (resolve, reject) {
    config.query(sql, addSqlParams, function (err, result) {
      if (err) {
        reject(err);
      }
      resolve(result);
      console.log(result);
    })
  })
}

// 登录
exports.find = function (condition) {
  let sql = "SELECT * FROM info WHERE " + condition;
  return new Promise(function (resolve, reject) {
    config.query(sql, function (err, result) {
      if (err) {
        reject(err);
      }
      resolve(result);
      console.log(result);
    })
  })
}

// 条件查历史记录
exports.find_history = function (id) {
  let sql = "SELECT * FROM feature_result WHERE id=" + id;
  return new Promise(function (resolve, reject) {
    config.query(sql, function (err, result) {
      if (err) {
        reject(err);
      }
      resolve(result);
      console.log(result);
    })
  })
}




