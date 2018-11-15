/*
    creat       :   daimingru
    date        :   2016-10-14
    function    :   wechatlogin
    loginClass  :   member-login
*/
(function ($) {
    var time,loginopendata={};
    var storage=window.localStorage;
    var dfd=$.Deferred(),iscanWx;
    //根据数据返回
    $.ajax({
        url:"/customer/loginWay",
        type:"post",
        success:function(data){
            if(data.status==200){
                loginopendata.openEmailLogin=data.data.isOpenEmailLogin;
                loginopendata.openPhoneLogin=data.data.isOpenPhoneLogin;
                loginopendata.isOpenWechatLogin=data.data.isOpenWechatLogin;
                if(!loginopendata.openEmailLogin&&!loginopendata.openPhoneLogin&&!loginopendata.isOpenWechatLogin){
                    return
                }
                if(data.data.isOpenEmailLogin||data.data.isOpenPhoneLogin){
                    if($(".member-login").length){
                        $(".member-login").attr({"href":"/customer/login.html"})
                    } 
                     if ($(".member-regist").length){
                        $(".member-regist").attr({"href":"/customer/register.html"}); 
                    }
                } else{
                    $("body").on("click",".member-regist,.member-login",function(){
                        wxAuthorization();
                       $.when(dfd).done(function(data){
                           if(iscanWx){
                              createQcode();
                           }
                       })
                    })
                }
                $(document).on("login.commodityDetail",function(e) {
                    storage.setItem("wxhref",location.href);
                    if (loginopendata.openEmailLogin || loginopendata.openPhoneLogin) {

                        location.href="/customer/login.html";

                    } else if (loginopendata.isOpenWechatLogin && !loginopendata.openEmailLogin && !loginopendata.openPhoneLogin) {

                        createQcode();

                    }
                })
            }
        }
    });
    $("body").on("click",".member-regist,.member-loginWX,.member-login,[data-elementtype=memberLoginWX]",function(){
        storage.setItem("wxhref",location.href);
        if(loginopendata.isOpenWechatLogin){
            if(/member-loginWX$/.test($(this).attr("class"))||$(this).attr("data-elementtype")=="memberLoginWX"){
               wxAuthorization();
               $.when(dfd).done(function(data){
                   if(iscanWx){
                      createQcode();
                   }
               })
            }
        }
    })
    //创建二维码
    function createQcode() {
        var body = document.body;
        var div = '<div class="canvascode"><div class="canvascodeb"><p>微信登录<i></i></p><div class="canvascodea"></div><span>请使用微信扫描二维码登录</span><div class="succ"><img src="/images/wechat/login_success.png" width="40px"><b>登录成功！</b></div></div></div>';
        $('body').append(div);
        $('body').on('click', '.canvascodeb i',function() {
            clearInterval(timer);
            $('.canvascode').remove();
        });
        getwechatUrlcode();
    }
    //获取链接生成URL
    function getwechatUrlcode(){
        $.ajax({
            url:'/customer/wxlogin/getLoginQrcodeUrl',
            type:'get',
            data:{},
            datatype:"json",
            success:function(data){
                if(data.status == 200){
                    $('.canvascodea').qrcode({
                        width: 200,
                        height: 200,
                        text: data.data
                    });
                    selectAJAX();
                }

            },
            err:function(err){
            }
        })
    }
    //微信是否授权
    function wxAuthorization(){
        $.ajax({
            url:"/customer/is/authorized",
            type:"get",
            success:function(data){
                if(data.status==200){
                    iscanWx=data.data;
                    dfd.resolve();
                }
            }
        })
    }
    //开启轮询ajax
    function selectAJAX(){
        timer = setInterval(function(){
            $.ajax({
                url:'/customer/wxlogin/isWechatLogin',
                type:'get',
                data:{},
                datatype:"json",
                success:function(data){
                    if(data.status == 200){
                        $('.canvascode span').hide();
                        $('.succ').show();
                        clearInterval(timer);
                        setTimeout(function(){
                            /*window.location.reload();*/
                            window.location.href=storage.getItem("wxhref");
                        },2000);
                    }
                },
                err:function(err){
                }
            })
        },4000);
    }
    
})(jQuery);
