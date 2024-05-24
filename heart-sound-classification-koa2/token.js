const jwt = require('jsonwebtoken');

//加密
exports.encrypt = function(data,time){
    return jwt.sign(data,'token',{expiresIn:time});
}

//解密
exports.decrypt = function(token){
    try{
        let data = jwt.verify(token,'token');
        return{
            token:true,
            id:data.id
        }
    }catch(error){
        return{
            token:false,
            data:error
        }
    }
}