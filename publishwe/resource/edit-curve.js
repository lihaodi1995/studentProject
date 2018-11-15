(function ($) {
    var lastTime = 0;
    var vendors = ['webkit', 'moz'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame'] ||    // name has changed in Webkit
            window[vendors[x] + 'CancelRequestAnimationFrame'];
    }
    if (!window.requestAnimationFrame) {
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16.7 - (currTime - lastTime));
            var id = window.setTimeout(function() {
                callback(currTime + timeToCall);
            }, timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
    }
    if (!window.cancelAnimationFrame) {
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
    }
    var funParabola = function(element, target, options) {
        var i=0;
        var defaults = {
            speed: 500, // 每帧移动的像素大小，每帧（对于大部分显示屏）大约16~17毫秒
            curvature: 0.0010,  // 实际指焦点到准线的距离，你可以抽象成曲率，这里模拟扔物体的抛物线，因此是开口向下的
            progress: function() {},
            complete: function() {}
        };

        var params = {}; options = options || {};

        for (var key in defaults) {
            params[key] = options[key] || defaults[key];
        }
        var exports = {
            mark: function() { return this; },
            position: function() { return this; },
            move: function() { return this; },
            init: function() { return this; }
        };
        /* 确定移动的方式
         * IE6-IE8 是margin位移
         * IE9+使用transform
         */
        var moveStyle = "margin", testDiv = document.createElement("div");
        if ("oninput" in testDiv) {
            ["", "ms", "webkit"].forEach(function(prefix) {
                var transform = prefix + (prefix? "T": "t") + "ransform";
                if (transform in testDiv.style) {
                    moveStyle = transform;
                }
            });
        }
        // 根据两点坐标以及曲率确定运动曲线函数（也就是确定a, b的值）
        /* 公式： y = a*x*x + b*x + c;
         */
        var a = params.curvature, b = 0, c = 0;

        // 是否执行运动的标志量
        var flagMove = true;

        if (element && target && element.nodeType == 1 && target.nodeType == 1) {
            var rectElement = {}, rectTarget = {};

            // 移动元素的中心点位置，目标元素的中心点位置
            var centerElement = {}, centerTarget = {};

            // 目标元素的坐标位置
            var coordElement = {}, coordTarget = {};

            // 标注当前元素的坐标
            exports.mark = function() {
                if (flagMove == false) return this;
                if (typeof coordElement.x == "undefined") this.position();
                element.setAttribute("data-center", [coordElement.x, coordElement.y].join());
                target.setAttribute("data-center", [coordTarget.x, coordTarget.y].join());
                return this;
            }

            exports.position = function() {
                if (flagMove == false) return this;

                var scrollLeft = document.documentElement.scrollLeft || document.body.scrollLeft,
                    scrollTop = document.documentElement.scrollTop || document.body.scrollTop;

                // 初始位置
                if (moveStyle == "margin") {
                    element.style.marginLeft = element.style.marginTop = "0px";
                } else {
                    element.style[moveStyle] = "translate(0, 0)";
                }

                // 四边缘的坐标
                rectElement = element.getBoundingClientRect();
                rectTarget = target.getBoundingClientRect();

                // 移动元素的中心点坐标
                centerElement = {
                    x: rectElement.left + (rectElement.right - rectElement.left) / 2 + scrollLeft,
                    y: rectElement.top + (rectElement.bottom - rectElement.top) / 2	+ scrollTop
                };

                // 目标元素的中心点位置
                centerTarget = {
                    x: rectTarget.left + (rectTarget.right - rectTarget.left) / 2 + scrollLeft,
                    y: rectTarget.top + (rectTarget.bottom - rectTarget.top) / 2 + scrollTop
                };

                // 转换成相对坐标位置
                coordElement = {
                    x: 0,
                    y: 0
                };
                coordTarget = {
                    x: -1 * (centerElement.x - centerTarget.x),
                    y:  -1 * (centerElement.y - centerTarget.y)
                };
                b = (coordTarget.y - a * coordTarget.x * coordTarget.x) / coordTarget.x;

                return this;
            };

            // 按照这个曲线运动
            exports.move = function() {
                // 如果曲线运动还没有结束，不再执行新的运动
                if (flagMove == false) return this;
                var self = this;
                var startx = 0, rate = coordTarget.x > 0? 1: -1;

                var step = function() {
                    if(!document.getElementById("mini")) return;
                    // 切线 y'=2ax+b
                    var tangent = 2 * a * startx + b; // = y / x
                    // y*y + x*x = speed
                    // (tangent * x)^2 + x*x = speed
                    // x = Math.sqr(speed / (tangent * tangent + 1));
                    startx = startx + rate * Math.sqrt(params.speed / (tangent * tangent + 1));
                    // 防止过界
                    if ((rate == 1 && startx > coordTarget.x) || (rate == -1 && startx < coordTarget.x)) {
                        startx = coordTarget.x;
                    }
                    var x = startx, y = a * x * x + b * x;

                    // 标记当前位置，这里有测试使用的嫌疑，实际使用可以将这一行注释
                    mini.setAttribute("data-center", [Math.round(x), Math.round(y)].join());

                    // x, y目前是坐标，需要转换成定位的像素值
                    if (moveStyle == "margin") {
                        mini.style.marginLeft = x + "px";
                        mini.style.marginTop = y + "px";
                    } else {
                        mini.style[moveStyle] = "translate("+ [x + "px", y + "px"].join() +")";
                    }
                    if (startx !== coordTarget.x) {
                        params.progress(x, y);
                        window.requestAnimationFrame(step);
                    } else {
                        // 运动结束，回调执行
                        params.complete();
                        flagMove = true;
                        self.addEnd(mini);
                        //回调函数添加位置
                    }
                };
                window.requestAnimationFrame(step);
                return this;
            };

            // 初始化方法
            exports.init = function(mini) {
                this.position().mark().move();
            };
            exports.addEnd = function(mini) {
                $(mini).remove();
                var $strong=$(".goods-pay").find(".personal-car strong");
               if($strong.hasClass("none")){
                   $strong.removeClass("none");
                   $(".goods-pay .radio-all").addClass("active");
               }
                //判断是不是新数据
                if(parabola.flag){
                    var $strong=$(".personal-car strong");
                    var val=parseFloat($strong.text())||0;
                    $strong.text(val+1);
                    parabola.flag=false;
                }
            };
        }

        return exports;
    };

    /* 元素 */
    var target = document.getElementsByClassName("personal-car")[0];
    //var target = document.getElementsByClassName("basket-car")[0];

    // 抛物线元素的的位置标记
    var $shoppingCartBtn=$(".shoppingCartBtn");
    var parabola = funParabola($shoppingCartBtn[0], target).mark();
    parabola.flag=false;
    // 抛物线运动的触发 配合剑剑触发
    $(document).on("addShoppingCart", function (e,data) {
        if($("#mini").length||!$(".goods-pay").length) return;
        var obj=$.parseJSON(data.cartItem);
        data.count=obj.count;
        var srcPath=obj.picPath;
        $("<div class='mini' id='mini'> </div>").appendTo($("body"));
        $.ajax({
            url: "/shoppingcart/updateCart",
            type: "post",
            data: data,
            dataType: "json",
            success: function (json) {
                if(json.status==200){
                    $(".mini").css({
                        "left":($shoppingCartBtn.offset().left - $(window).scrollLeft())+60+"px",
                        "top":($shoppingCartBtn.offset().top - $(window).scrollTop())+"px",
                        "background-image": "url(" + srcPath + ")",
                        "background-size": "100% 100%"
                    });
                    setTimeout(function () {
                        $("#mini").show();
                        parabola.init(document.getElementById("mini"));
                    },400);
                    //对比数据开始
                    var arr=obj.specificationId.split("");
                    var str=obj.id;
                    for(var i=0;i<arr.length;i++){ str+=arr[i] };
                    var $liList=$(".wqd-buyCar .detail-list li");
                    $liList.length?parabola.exist(obj,$liList,str):parabola.joinData(obj);
                }else {
                    $("#mini").remove();
                }
            },
            error:function(){
                $("#mini").remove();
            }
        })


    });
    parabola.exist = function (obj, $liList, str) {
        var flag = true;
        $liList.each(function (i, _) {
            var _str = $(this).attr("id");
            _str+=$(this).find(".detail-describe").attr("sizeid");
            if (str == _str) {
                var $same = $(this).find(".number");
                $same.text(parseFloat($same.text()) + parseFloat(obj.count));
                flag = false;
                return false;
            }
        });
        flag && parabola.joinData(obj);
    };
    parabola.joinData = function (data) {
        var $li = $("<li id=" + data.id + "><span class='edit-radio active'></span> <dl class='clearfix'> <dt><a href="+data.itemLink+"><img src=" + data.picPath + " alt=''/></a></dt> <dd class='detail-title' title=" + data.name + "><a href="+data.itemLink+">" + data.name + "</a></dd> <dd class='detail-describe' sizeid="+data.specificationId+"> </dd> <dd class='detail-model'> <i class='num-reduse'></i> <span class='number'>" + data.count + "</span> <i class='num-add'></i> <span class='price'>￥<b class='unit-price'>" + data.price + "</b></span> <em class='delete'></em> </dd> </dl> </li>");
        $li.appendTo($(".detail-list"));
        var $lastLi = $(".detail-list li:last");
        if ($(".detail-list li").length == 1){$lastLi.addClass("list-first");}
        var arr = data.specificationValue.split("_"), $span;
        for (var i = 0; i < arr.length; i++) {
            $span = i == 0 ? $("<span class='describe-first'>" + arr[i] + "</span>") : $("<span>" + arr[i] + "</span>");
            $span.appendTo($lastLi.find(".detail-describe"));
        }
        //判断是不是新数据
        parabola.flag=true;
    };

})($);
