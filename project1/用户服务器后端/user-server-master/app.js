// const p="/Users/luo/WebstormProjects/node-server-git/user-server/"
// const p="/home/ubuntu/NodeServer/user-server/"


const express = require('express')
//引入加密
const  aes= require("./encrypt.js");
//创建
const app = express()
//扩展body解析
let bodyParser = require('body-parser');
let multer = require('multer'); // v1.0.5
//mysql
const mysql = require('mysql');

//改用连接池
const pool=mysql.createPool({
    connectionLimit : 200, // default = 10
    host: '192.144.174.97',
    user: 'acmp',
    password: 'acmp666',
    database: 'ACMP'
})
let sqlStr=function(s){
    return s.replace(/["']/g, " ")

}
// const connection = mysql.createConnection({
//     host: '192.144.174.97',
//     user: 'acmp',
//     password: 'acmp666',
//     database: 'ACMP'
// });
// let connectDB=function(){
//     try {
//         connection.connect()
//     } catch (e) {
//     }
// }
// connectDB()
//支持跨域
app.all('*', function(req, res, next) {

    res.header("Access-Control-Allow-Origin", ""+req.header("Origin"));
    res.header("Access-Control-Allow-Headers", " Origin, X-Requested-With, Content-Type, Accept");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    res.header("Access-Control-Allow-Credentials", "true")
    next();
});

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded
//工具函数

function log(msg){
    console.log(msg)
}
let preOperation=function (req,res,next){
    log("receive body"+JSON.stringify(req.body))
    next()
}
//设置进程标题
process.title = process.argv[2];
//挂载前置处理
app.use(preOperation)
//管理员
let adminLogin = function (req,res,next) {
    let bodyAdmin=req.body
    let admin={
        "email":"",
        "password":""
    }
    admin.email=bodyAdmin.email
    admin.password=bodyAdmin.password;
    //
    log("body内部的email和password为"+admin.email+"\t"+admin.password)

    //start

    let result={
        "code":"200",//200-成功,400-失败
        "msg":"",//成功或失败附带的消息
        "data":{
            "token":"no404"
        }//内容负载
    };
    pool.getConnection(function (err, connection) {
        connection.query('SELECT * FROM manager WHERE email = \'' + admin.email + '\';', function (error, results, fields) {
            if (error) throw error;
            if (results.length !== 1) {
                //账号不存在
                if (!result) {
                    log("无法引用result!")
                } else {
                    log("可以引用result,result的code为" + result.code)
                }

                result.code = "400";
                result.msg = "账号不存在"
                result.data = {}
                log("用户不存在")
                res.send(result)
                connection.release()
                next()

            } else {
                //用户名存在
                if (results[0].password === admin.password) {

                    //成功
                    result.code = "200"
                    result.msg = "认证成功!"
                    let user = {"type": "", "id": "", "name": ""}
                    user.id = results[0].id
                    user.name = results[0].name
                    user.type = "manager"

                    let tokenBef = JSON.stringify(user)
                    let tokenAft = aes.enc(tokenBef)
                    //log
                    log("加密输出:" + tokenAft)
                    result.data.token = tokenAft
                    res.send(result)
                    connection.release()
                    next()

                } else {
                    //密码错误
                    result.code = "400"
                    result.msg = "密码错误"
                    result.data = {}
                    res.send(result)
                    connection.release()
                    next()

                }
            }
        });
    })
    //stop
};
app.post('/manager/login',adminLogin);
//普通用户
//注册
let userRegister= function (req,res,next){
    pool.getConnection(function (err, connection) {
        let user = req.body;
        let result = {
            "code": "200",//200-成功,400-失败
            "msg": "",//成功或失败附带的消息
            "data": {
                "token": "no404"
            }//内容负载
        };
        if (user.name.length>0 && user.email.length>0 && user.password.length>0) {
            //可用
            connection.query('SELECT * FROM user WHERE email=\'' + user.email + '\' or name=\'' + user.name + '\';', function (error, results, fields) {
                if (results.length > 0) {
                    //email或者名字冲突
                    result.code = "400"
                    result.msg = "邮箱或名字已经被他人注册"
                    result.data = {}
                    //todo
                    res.send(result)
                    connection.release()

                    next()
                } else {
                    //邮箱和名字不冲突
                    connection.query('INSERT INTO user(email, password, name) VALUES (\'' + user.email + '\',\'' + user.password + '\',\'' + user.name + '\');\n', function (error, results, fields) {
                        if (error) {
                            //插入失败
                            result.code = "400"
                            result.msg = "邮箱,名字,密码过长!"
                            result.data = {}

                        } else {
                            //插入成功
                            result.code = "200"
                            result.msg = "注册成功!"
                            let userData = {
                                "id": "" + results.insertId,
                                "name": user.name,
                                "type": "user"
                            }
                            let dataString = JSON.stringify(userData)
                            result.data.token = aes.enc(dataString)

                        }
                        res.send(result)
                        connection.release()

                        next()
                    })
                }
            })
        } else {
            result.code = "400"
            result.msg = "字段不全,或格式错误!"
            result.data = {}
            res.send(result)
            connection.release()

            next()
        }
    })
};
app.post('/user/register',userRegister)
//用户登录
let userLogin=function (req,res,next) {
    pool.getConnection(function (err, connection) {
        if(err){
            log(err)
            res.send({"code":"400","msg":"数据库问题:"+err.toString(),"data":{}})
            connection.release()
            next()
        }else {
            let user = req.body
            //start
            let result = {
                "code": "200",//200-成功,400-失败
                "msg": "",//成功或失败附带的消息
                "data": {
                    "token": "no404"
                }//内容负载
            };
            if (user && user.email && user.password) {
                //格式可能正确
                connection.query('SELECT * FROM user WHERE email = \'' + user.email + '\';', function (error, results, fields) {
                    connection.release()

                    if (error) {
                        result.code = "400"
                        result.msg = "检查出错,格式错误"
                        result.data = {}
                    } else {
                        if (results.length !== 1) {
                            //账号不存在
                            result.code = "400";
                            result.msg = "账号不存在"
                            result.data = {}

                        } else {
                            //用户名存在
                            if (results[0].password === user.password) {
                                //成功
                                result.code = "200"
                                result.msg = "认证成功!"
                                let userData = {"type": "", "id": "", "name": ""}
                                userData.id = "" + results[0].id
                                userData.name = results[0].name
                                userData.type = "user"
                                result.data.token = aes.enc(JSON.stringify(userData))
                            } else {
                                //密码错误
                                result.code = "400"
                                result.msg = "密码错误"
                                result.data = {}

                            }
                        }
                    }
                    res.send(result)
                    next()
                });
            } else {
                //格式错误
                result.code = "400"
                result.msg = "报文格式错误"
                result.data = {}
                res.send(result)
                connection.release()
                next()
            }
            //
            //stop
        }
    })

};
app.post('/user/login',userLogin)
//机构与负责人
let insRegister=function (req,res,next) {
    pool.getConnection(function (err, connection) {
        let ins = req.body;
        let result = {
            "code": "200",//200-成功,400-失败
            "msg": "",//成功或失败附带的消息
            "data": {
                "token": "no404"
            }//内容负载
        };
        if (ins && ins.name && ins.location && ins.phone && ins.backimg && ins.introduction && ins.evidence) {
            //可用
            connection.query('SELECT * FROM institution WHERE name=\'' + ins.name + '\' ;', function (error, results, fields) {
                if (results.length > 0) {
                    //email或者名字冲突
                    result.code = "400"
                    result.msg = "机构重名"
                    result.data = {}
                    //todo
                    res.send(result)
                    connection.release()

                    next()
                } else {
                    //判断用户是否存在
                    if (ins.principal && ins.principal.name && ins.principal.password && ins.principal.email && ins.principal.phone) {
                        //用户字段存在

                        connection.query('SELECT * FROM principal WHERE email=\'' + ins.principal.email + '\' ;', function (newError, newResults, newField) {
                            if (newError || newResults.length > 0) {
                                //邮箱格式出错或已重复
                                result.code = "400"
                                result.msg = "邮箱重复 or "+newError
                                result.data = {}
                                //todo
                                res.send(result)
                                connection.release()

                                next()
                            } else {
                                //可以注册插入机构 并 插入第一个负责人
                                //邮箱和名字不冲突
                                connection.query('INSERT into institution(name,location,phone, backimg, introduction, evidence ) VALUES (\'' + sqlStr(ins.name) + '\',\'' + sqlStr(ins.location) + '\',\'' + sqlStr(ins.phone) + '\',\'' + sqlStr(ins.backimg) + '\',\'' + sqlStr(ins.introduction) + '\',\'' + sqlStr(ins.evidence) + '\');', function (nnerror, nnresults, nnfields) {

                                    if (nnerror) {
                                        //插入失败
                                        result.code = "400"
                                        result.msg = "输入的字段过长或非法!"+nnerror
                                        result.data = {}
                                        res.send(result)
                                        connection.release()

                                        next()
                                    } else {
                                        if(!nnresults){
                                            result.code="400"
                                            result.msg="nnresult not defined"
                                            connection.release()
                                            res.send(result)
                                            next()
                                        }else{
                                            //插入机构成功了,现在需要尝试插入第一个负责人
                                            let insId = nnresults.insertId
                                            let pp = ins.principal
                                            connection.query('INSERT INTO principal(belongIns, email, password, name, phone, power,location) VALUES (' + insId + ',\'' + pp.email + '\',\'' + pp.password + '\',\'' + pp.name + '\',\'' + pp.phone + '\',\'ALL\',\''+ins.location+'\');', function (n3error, n3results, n3fields) {
                                                //插入负责人结束
                                                if (n3error) {
                                                    //插入失败
                                                    result.code = "400"
                                                    result.msg = "特殊错误,联系管理"+n3error
                                                    result.data = {}
                                                } else {
                                                    //插入成功
                                                    let ppId = n3results.insertId
                                                    let ppUser = {"name": pp.name, "id": "" + ppId, "type": "principal"}
                                                    result.code = "200"
                                                    result.msg = "添加机构成功"
                                                    result.data.token = aes.enc(JSON.stringify(ppUser))
                                                }
                                                res.send(result)
                                                connection.release()

                                                next()
                                            })
                                        }

                                    }
                                })

                            }
                        })
                    } else {
                        //负责人信息非法
                        result.code = "400"
                        result.msg = "负责人数据格式非法"
                        result.data = {}
                        //todo
                        res.send(result)
                        connection.release()

                        next()
                    }

                }
            })
        } else {
            result.code = "400"
            result.msg = "字段不全,或格式错误!"
            result.data = {}
            res.send(result)
            connection.release()

            next()
        }
    })
};
app.post('/ins/register',insRegister)
//负责人登录
let ppLogin=function (req,res,next) {
    pool.getConnection(function (err, connection) {
        let pp = req.body
        let result = {
            "code": "",
            "msg": "",
            "data": {
                "token": ""
            }
        }
        if (pp && pp.email && pp.password) {
            //字段存在
            connection.query('SELECT * FROM principal WHERE email=\'' + pp.email + '\';', function (error, results, fields) {
                if (error || results.length === 0) {
                    //错误
                    result.code = "400"
                    result.msg = "邮箱错误或账号不存在"
                } else {
                    //检查
                    if (results[0].password === pp.password) {
                        //正确!
                        result.code = "200"
                        result.msg = "登录成功"
                        let userData = {
                            "type": "principal",
                            "id": "" + results[0].id,
                            "name": results[0].name
                        }
                        result.data.token = aes.enc(JSON.stringify(userData))
                    } else {
                        result.code = "400"
                        result.msg = "密码错误"
                    }
                }
                //
                res.send(result)
                connection.release()

                next()
            })
        } else {
            //字段缺失
            result.code = "400"
            result.msg = "字段缺失"
            res.send(result)
            connection.release()

            next()
        }
    })
}
app.post('/pp/login',ppLogin)
// app.get('/',(req,res) => res.send('hello world'))
//添加负责人
let ppAdd=function (req,res,next){
    pool.getConnection(function (err, connection) {
        if (!(req.body && req.body.token)) {
            //没有token
        }
        //有token
        let token = req.body.token
        let user = JSON.parse(aes.dec(token))
        if (!(user && user.belongIns && user.email && user.password && user.name && user.location && user.phone)) {

        }
        let result = {
            "code": "200",//200-成功,400-失败
            "msg": "",//成功或失败附带的消息
            "data": {
                "token": "no404"
            }//内容负载
        };
        if (user.name && user.email && user.password) {
            //可用
            connection.query('SELECT * FROM user WHERE email=\'' + user.email + '\' or name=\'' + user.name + '\';', function (error, results, fields) {
                if (results.length > 0) {
                    //email或者名字冲突
                    result.code = "400"
                    result.msg = "邮箱或名字已经被他人注册"
                    result.data = {}
                    //todo
                    res.send(result)
                    connection.release()

                    next()
                } else {
                    //邮箱和名字不冲突
                    connection.query('INSERT INTO user(email, password, name) VALUES (\'' + user.email + '\',\'' + user.password + '\',\'' + user.name + '\');\n', function (error, results, fields) {
                        if (error) {
                            //插入失败
                            result.code = "400"
                            result.msg = "邮箱,名字,密码过长!"
                            result.data = {}

                        } else {
                            //插入成功
                            result.code = "200"
                            result.msg = "注册成功!"
                            let userData = {
                                "id": "" + results.insertId,
                                "name": user.name,
                                "type": "user"
                            }
                            let dataString = JSON.stringify(userData)
                            result.data.token = aes.enc(dataString)

                        }
                        res.send(result)
                        connection.release()

                        next()
                    })
                }
            })
        } else {
            result.code = "400"
            result.msg = "字段不全,或格式错误!"
            result.data = {}
            res.send(result)
            connection.release()

            next()
        }
    })
}
app.post('pp/add',ppAdd)
//运行
//定时任务
// setInterval(connectDB,6000000)
let server = app.listen(3000, () => { console.log('it is running!')})

