function getPublicKey(){
    var jsonData = {};
    var publicKey = "";
    $.ajax({
        url: "{:url('index/index/getPublicKey')}",
        type: "post",
        datatype: "json",
        data: jsonData,
        async: false,
        success: function(data){
            publicKey = data['key'];
        },
        error: function(data){}
    })
    return publicKey;
}

function publicDecrypt(data, publicKey){
    var jsencrypt = new JSEncrypt();
    jsencrypt.setPublicKey(publicKey);
    var decryptData = jsencrypt.encrypt(data);
    return decryptData;
}

function strToHex(str){
    alert('begin');
    var jsonData = {str: str};
    var hex = "";
    $.ajax({
        url: "{:url('index/index/strToHex')}",
        type: "post",
        datatype: "json",
        data: jsonData,
        async: false,
        success: function(data){
            hex = data['hex'];
        },
        error: function(data){
        }
    })
    return hex;
}

function hexToStr(hex){
    var jsonData = {hex: hex};
    var str = "";
    $.ajax({
        url: "{:url('index/index/hexToStr')}",
        type: "post",
        datatype: "json",
        data: jsonData,
        async: false,
        success: function(data){
            str = data['str'];
        },
        error: function(data){}
    })
    return str;
}