const Koa = require('koa')
const app = new Koa()
const json = require('koa-json')
const onerror = require('koa-onerror')
const bodyparser = require('koa-bodyparser')
const logger = require('koa-logger')
const Token = require("./token");


// error handler
onerror(app)

// middlewares
app.use(bodyparser({
  enableTypes: ['json', 'form', 'text']
}))
app.use(json())
app.use(logger())


//不拦截页面
let excludeURL = [
  "/login",
  "/register"
]
function inArray(search,Array){
  for(let i in Array){
    if(search.startsWith( Array[i] )){
      return true;
    }
    return false;
  }
}
app.use(async(ctx,next) => {
  let url = ctx.request.url;
  if(inArray(url,excludeURL)){
    await next();
    return;
  }
  let token;
  //接收token
  if(ctx.request.query.token == undefined){
    token = ctx.request.header.token;
    console.log(token);
  }else{
    token = ctx.request.query.token;
    console.log(token);
  }
  let data = Token.decrypt(token);
  console.log(data);

  if (data.token) {
     //有效token
     ctx.id = data.id;
     console.log(ctx.id)
     await next();
   } else {
     //无效token
     ctx.response.body = {
       msg: "无效token"
     }
     return;
   }

})

// routes
let route = require('./router')
app.use(route);
// error-handling
app.on('error', (err, ctx) => {
  console.error('server error', err, ctx)
});

app.listen(3000, () => {
  console.log("服务器连接成功")
})
