// const p="/Users/luo/WebstormProjects/node-server-git/user-server/"
// const p="/home/ubuntu/NodeServer/user-server/"

const crypto = require('crypto');
/**
 * 加密方法
 * @param key 加密key
 * @param iv       向量
 * @param data     需要加密的数据
 * @returns string
 */
const encrypt = function (key, iv, data) {
    let cipher = crypto.createCipheriv('aes-128-cbc', key, iv);
    let crypted = cipher.update(data, 'utf8', 'binary');
    crypted += cipher.final('binary');
    crypted = new Buffer(crypted, 'binary').toString('base64');
    return crypted;
};

/**
 * 解密方法
 * @param key      解密的key
 * @param iv       向量
 * @param crypted  密文
 * @returns string
 */
const decrypt = function (key, iv, crypted) {
    crypted = new Buffer(crypted, 'base64').toString('binary');
    let decipher = crypto.createDecipheriv('aes-128-cbc', key, iv);
    let decoded = decipher.update(crypted, 'binary', 'utf8');
    decoded += decipher.final('utf8');
    return decoded;
};
const key = '751f621ea5c8f930';
const iv = '2624750004598718';

// console.log('加密的key:', key.toString('hex'));

//console.log('加密的iv:', iv);
// let data = "Hello, nodejs. 演示aes-128-cbc加密和解密";
// console.log("需要加密的数据:", data);
// let crypted = encrypt(key, iv, data);
// console.log("数据加密后:", crypted);
// let dec = decrypt(key, iv, crypted);
// console.log("数据解密后:", dec);

//需要输出的加密函数
let myEnc=function (data) {
    return encrypt(key,iv,data);
}
//解密函数
let myDec=function (cryptedData) {
    return decrypt(key,iv,cryptedData);
}

// let data={
//     "name":"小王",
//     "id":"5",
//     "type":"user"
// }
//
// console.log(myEnc(JSON.stringify(data)))

module.exports = {"enc":myEnc,"dec":myDec};