
//------------------------------------------------------
$(function() {
    var pictureEvent = {};
    pictureEvent.eleInit = function() {
        //去除点击效果
        $(".mShadeBg").removeClass("mShadeBg");
        $(".mTitleColor").removeClass("mTitleColor");
        $(".pohotoshow").each(function() {
            var showHeight = $(this).parents("div[data-elementtype=picture]").height() - 84;
            $(this).css("height", showHeight);
        }).css("opacity", 0);
    }();
    pictureEvent.bindEvent = function() {
        var pc = $(window).width() > 768 ? true : false;
        var screenWid = $(window).width();
        var screenHei = $(window).height();
        var $AclickSource;
        $(".atlasWrap,.atlasWrap3,.atlasWrap5,.atlasWrap4").each(function() {
            var self = $(this);
            //手机端点击出现遮罩事件
            if ($("body").find(".wqdIphoneView").length) {
                self.find(".wqd-atlas li .wrap ").on("click", function() {
                    $(this).find("a>span").toggleClass("mShadeBg").end().parent().siblings().find("a>span").removeClass("mShadeBg");
                    $(this).find("h5").toggleClass("mTitleColor").end().parent().siblings().find("h5").removeClass("mTitleColor");
                });
            };
        });
        //发布后的图册三动画效果
        $(".atlasWrap3").each(function(i) {
            var self = $(this);
            self.find("#scroller").width(self.find(".wqd-atlas").width());
            if ($(window).width() >= 768) {
                var speed = 10;
                var tab = self[0];
                var tab1 = self.find(".wqd-atlas.autoscroll")[0];
                //为了平滑过渡
                if (self.find(".autoscroll.copy").length == 0) {
                    $("<div class='autoscroll copy'><div>").appendTo(self.find(".scrollBox"));
                };
                var MyMar;
                tab.scrollLeft = 0;
                var tab2 = self.find(".autoscroll.copy")[0];
                tab2.innerHTML = tab1.innerHTML;
                self.parent().find(".leftBar,.rightBar").hover(function() {
                        clearInterval(MyMar);
                        if ($(this).hasClass("rightBar")) {
                            function Marquee1() {
                                if (tab2.offsetWidth - tab.scrollLeft <= 0) {
                                    tab.scrollLeft = 0;
                                } else {
                                    tab.scrollLeft += 1;;
                                }
                            };
                            MyMar = setInterval(Marquee1, speed);
                        } else if ($(this).hasClass("leftBar")) {
                            function Marquee2() {
                                if (tab.scrollLeft <= 0)
                                    tab.scrollLeft += tab2.offsetWidth
                                else {
                                    tab.scrollLeft--
                                }
                            }
                            MyMar = setInterval(Marquee2, speed);
                        };
                    },
                    function() {
                        clearInterval(MyMar);
                    });
            } else {
                self.find(".copy").remove();
                self.siblings(".leftBar,.rightBar").css("display", "none");
            };
        });
        
        //发布后的图册四动画效果
        $(".atlasWrap4").each(function(i) {
            //获取比例
            function getInitRatio(url) {
                var image = new Image();    
                image.src = url;
                var realWidth = image.width;
                var realHeight = image.height;
                return realWidth / realHeight;
            };
            var self = $(this).find(".wqd-atlas");
            self.find("a").each(function() {
                $(this).height($(this).parents("[data-elementtype='picture']").height());
            });
            self.on("mouseenter click", "li", function() {
                var $li = $(this);
                var viewHeight = $li.parents("[data-elementtype='picture']").height();
                var viewWidth = $li.parent().width();
                var imgSrc = $li.find("a").css("background-image").replace(/\"|\(|\)|url/g, '');;
                var activeWidth = viewHeight * getInitRatio(imgSrc) >= viewWidth * 0.8 ? viewWidth * 0.8 : viewHeight * getInitRatio(imgSrc);
                var allChildren = $li.parent().children();
                var liLen = allChildren.length;
                var otherWidth = (viewWidth - activeWidth) / (liLen - 1);
                var activeIndex = $li.index();
                $li.addClass("active").siblings().removeClass("active");
                $li.find(".wrap,.wrap a").css({
                    "width": "100%"
                });
                allChildren.each(function(i) {
                    var self = $(this);
                    if (i < activeIndex) {
                        self.stop().animate({
                            "left": i * otherWidth,
                            "width": otherWidth
                        });
                    } else if (i == activeIndex) {
                        self.stop().animate({
                            "left": i * otherWidth,
                            "width": activeWidth
                        }, function() {
                            self.find(".txt_box").css("width", activeWidth).stop().show(200)
                        });
                    } else if (i > activeIndex) {
                        self.stop().animate({
                            "width": otherWidth,
                            "left": (i - 1) * otherWidth + activeWidth
                        });
                    };
                });
            });
            self.on("mouseleave", function() {
                var viewWidth = $(this).width();
                var liLen = self.find("li").length;
                self.find("li").each(function(m) {
                    self.find(".txt_box").hide();
                    $(this).stop().animate({
                        "width": viewWidth / liLen,
                        "left": viewWidth * m / liLen
                    }, function() {
                        self.find(".wrap,.wrap a").css({
                            "width": viewWidth / liLen + "px"
                        });
                    });
                });

            });

        });
        //发布后的图册五动画效果
        $(".atlasWrap5").each(function() {
            var self = $(this);
            var scrollBox = self.find(".wqd-atlas");
            var $li=self.find(".wqd-atlas li");
            var scrollerWidth=$li.length * $li.find("a").innerWidth() + parseInt(($li.length-1)*10);
            self.find("#scroller,.wqd-atlas").css("width",scrollerWidth);
            self.find(".wqd-atlas a").each(function() {
                $(this).attr("onclick", "return false");
            });
        });
        //手机端添加弹框         
        $("[data-elementtype]").length != 0 && $("body").append("<div class='mtucebg' style='display:none;background-color:#000;position:fixed;top:0;width:100%;z-index:999'><div id='mWrapper' style='height:" + screenHei + "px'><div id='mScrollerShow'><ul style='white-space:nowrap' ></ul></div></div></div>");
        $(".autoscroll").addClass("wqd-atlas");
        //pc前进后退按键
        $(document).on("click", "i", function() {
            var $cboxLoadedContent = $("#cboxLoadedContent"),
                mengban;
            if ($(this).hasClass("pictureShowL") || $(this).hasClass("pictureShowR")) {
                $(this).hasClass("pictureShowL") && $("#cboxPrevious").trigger("click");
                $(this).hasClass("pictureShowR") && $("#cboxNext").trigger("click");
                setTimeout(function() {
                    var $cboxLoadedContentImg = $("#cboxLoadedContent").find("img")
                    $AclickSource.closest("ul").find("a").each(function() {
                        if (($(".atlasWrap3,.atlasWrap4,.atlasWrap5").length && $(this).css("background-image").indexOf($cboxLoadedContentImg.attr("src")) != -1) || (!$(".atlasWrap3,.atlasWrap4,.atlasWrap5").length && $(this).find("img").attr("src").indexOf($cboxLoadedContentImg.attr("src")) != -1)) {
                            mengban = $(this).find("div").css("background-color") ? $(this).find("div").css("background-color") : "rgba(0,0,0,0)";
                        };
                    });
                    $("#cboxLoadedContent").css({
                        position: "relative"
                    }).find("div").remove().end().append("<div style='background-color:" + mengban + ";position:absolute;top:0;left:0;width:100%;height:100%;'></div>")
                }, 100);
            };
            $(this).hasClass("pictureShowClose") && $("#cboxOverlay").trigger("click");
        });
        //关闭pc图册弹窗
        $(document).on("click", "#cboxOverlay", function() {
            $(".btnControl,.pictureShowClose").hide();
            $(".btnControl").remove();
        });
        //手机图册弹出框
        var time1, time2; //解决双击事件bug
        $(document).on("click", ".wqd-atlas:not(.pohotoindex .wqd-atlas) a,.pohotoshow a", function(e) {
            if($(this).attr("href").indexOf("javascript:void(0)")==-1) return;
            var screenWid = $(window).width();
            var screenHei = $(window).height();
            var bgHei = $(document).height() > $(window).height() ? $(document).height() : $(window).height();
            var $thisA=$(this);
            e.stopPropagation();
            $AclickSource = $(e.target);
            if (pc) {
                return;
            };
            $(".mtucebg").height(bgHei);
            $(".btnControl,.pictureShowClose").hide();
            if ($(this).parents(".atlasWrap4").length != 0) {
                return;
            };
            //加载手机弹窗
            var html = "";
            var liLen = $(this).parents("li").parent().children().length;
            $ele = $(this).parents('.pohotoshow').length ? $(this).parents('.pohotoshow').find("a") : $(this).parents('[data-elementtype]').find("a");
            $ele.each(function() {
                if($(this).attr("href").indexOf("javascript:void(0)")==-1) return;
                var imgSrc = $(this).parents(".atlasWrap3,.atlasWrap4,.atlasWrap5").length == 0 ? $(this).find("img").attr("src") : $(this).css("background-image").replace(/\"|\(|\)|url/g, '');
                var mengban = $(this).find("div").css("background-color");
                html += "<li style='display:inline-block;position:relative'><div style='display:table;vertical-align:middle;width:100%;height:100%'><p style='display:table-cell;vertical-align:middle'><span style='position:relative;display:inline-block'><img style='vertical-align: middle;' src='" + imgSrc + "'><span style='position:absolute;top:0;left:0;width:100%;height:100%;display:inline-block;background-color:" + mengban + "'></span></span></p></li>";
            });
            $(".mtucebg ul").html(html);
            //设置显示文字
            var $mtucebgLiIndex;
            $(".mtucebg ul li").each(function(){
                var $index=$(this).index()+1;
                var liLen=$(".mtucebg ul li").length;
                var liImg=$(this).find("img");
                var aInitImg=$thisA.parents(".atlasWrap3,.atlasWrap4,.atlasWrap5").length == 0 ? $thisA.find("img").attr("src") : $thisA.css("background-image").replace(/\"|\(|\)|url/g, '')
                $(this).append("<span style='position:absolute;top:10px;left:10px;color:#fff'>" + $index + "/" + liLen + "</span>")
                if(liImg.attr("src").indexOf(aInitImg)!=-1){
                   $mtucebgLiIndex=$(this).index()+1; 
                };
            });
            var sonLen = $(".mtucebg ul li").length;
            $(".mtucebg").show().find("#mScrollerShow").css({
                "width": sonLen * $(window).width(),
            }).find("li").css({
                width: screenWid,
                height: screenHei,
                "text-align": "center",
            }).find("img").css({
                "max-width": screenWid,
                "max-height": screenHei
            });
            new IScroll("#mWrapper", {
                scrollX: true,
                scrollY: false,
                hScrollbar: false,
                vScrollbar: false,
                disableTouch: false,
                HWCompositing: true,
                snap: "li",
                click: true,
                momentum: false,
            }).scrollToElement(".mtucebg ul li:nth-child(" + $mtucebgLiIndex + ")", 0);
            time1 = new Date().getTime();
        });
        //pc左右鼠标滑过
        $(document).on("mouseover mouseout", ".btnControl", function(e) {
            e.type == "mouseover" && $(this).find("i").show();
            e.type == "mouseout" && $(this).find("i").hide();
        });
        //手机关闭弹窗         
        $(document).on("click", "#mWrapper", function(e) {
            time2 = new Date().getTime(); //截胡双击<<<<<<<-----mbd
            if (time2 - time1 < 500) {
                return;
            };
            $(".mtucebg").css({
                display: "none"
            });
        });
    };
    pictureEvent.bindEvent();
});
//加载完成后的效果
$.getScript("/js/phone/plugin/wqdIscroll.js", function(data, textStatus, jqxhr) {
      var pc = $(window).width() > 768 ? true : false;
    var screenWid = $(window).width();
    var screenHei = $(window).height();
    //前四个可以调用
    $(".wqd-atlas").not(".pohotoindex .wqd-atlas").each(function(i) {
        $(this).find("a").each(function() {
            if ($(this).attr("href").indexOf("javascript:void(0)") != -1) {
                $(this).attr({
                    "href": "javascript:void(0)"
                }).addClass("y-enlarge" + i).attr({
                    "onclick": "return false"
                });
            }
        });
        slider($(".y-enlarge" + i), ".wqd-atlas");
    });
    //滚动设置
    if ($(".pohotoindex").length != 0 || $(".scrollBox").length != 0) {
        //第五索引
        $(".pohotoindex").each(function(i) {
            var $this = $(this);
            $this.attr("id", "wrapper1_" + i);
            // $this.children().eq(0).width($this.find("ul li").length * $this.find("ul li").innerWidth());
            setTimeout(function() {
                $this.scroll = new IScroll("#wrapper1_" + i, {
                    scrollX: true,
                    scrollY: false,
                    hScrollbar: false,
                    vScrollbar: false,
                    disableTouch: false,
                    mouseWheel: true,
                    click: true,
                    preventDefault: false,
                    HWCompositing: $(window).width() >= 768 ? false : true,
                });
                $this.on('touchstart', mEvent);
                $this.on('touchmove', mEvent);
                $this.on('touchend', mEvent);
            }, 100)
        });
        //第五展示
        $(".pohotoshow").each(function(i) {
            var $show = $(this);
            var html = "";
            var sonLen = $show.siblings(".pohotoindex").find(".wqd-atlas li").length;
            $show.attr("id", "wrapper2_" + i).siblings(".pohotoindex").find(".wqd-atlas li a").each(function() {
                var realTarget = $(this).attr("target") == "_blank" ? "target='_blank'" : "";
                var menban = $(this).find(".mask").css("background-color");
                html += "<li style='display:inline-block'><a href='" + $(this).attr("href") + "' " + realTarget + " style='background-image:" + $(this).css("background-image") + ";background-size:cover;width:" + $show.parents("div[data-elementtype=picture]").width() + "px;height:"+$show.height()+"px'><div style='background-color:" + menban + ";position:absolute;top:0;left:0;right:0;bottom:0'></div></a></li>";
                $(this).attr({
                    "href": "javascript:void(0);"
                }).removeAttr("target");
            });
            $show.html("<div id='scrollerShow' style='width:" + sonLen*$show.parents("div[data-elementtype=picture]").width() + "px;height:" + $show.height() + "px;overflow:hidden'><ul style='white-space:nowrap'>" + html + "</ul></div>");
            $show.find("a").each(function() {
                if ($(this).attr("href").indexOf("javascript:void(0)") != -1) {
                    $(this).attr({
                        "href": "javascript:void(0)"
                    }).addClass("y-enlargeTuce5_" + i).attr({
                        "onclick": "return false",
                        "ondragstart": "return false"
                    });
                }
            });
            slider($(".y-enlargeTuce5_" + i), ".pohotoshow");
            setTimeout(function() {
                $show.scroll = new IScroll("#wrapper2_" + i, {
                    scrollX: true,
                    scrollY: false,
                    hScrollbar: false,
                    vScrollbar: false,
                    disableTouch: false,
                    snap: "li",
                    click: true,
                    momentum: false,
                    HWCompositing: $(window).width() >= 768 ? false : true,
                    preventDefault: false,
                });
                $show.siblings().on("click ", ".wqd-atlas li a", function(e) {
                    if (e.type == "click") {
                        var index = $(this).parents("[data_pic]").index() + 1;
                        $show.scroll.scrollToElement("#wrapper2_" + i + " li:nth-child(" + index + ")", 500);
                    };
                });
                $show.on('touchstart', mEvent);
                $show.on('touchmove', mEvent);
                $show.on('touchend', mEvent);
            }, 100)
        }).css("opacity", 1);
        if ($(window).width() <= 768) {
            //第三滚动
            $(".scrollBox").each(function(i) {
                $this = $(this);
                $this.attr("id", "wrapper3_" + i);
                setTimeout(function() {
                    $this.scroll = new IScroll("#wrapper3_" + i, {
                        scrollX: true,
                        scrollY: false,
                        hScrollbar: false,
                        vScrollbar: false,
                        disableTouch: false,
                        click: true,
                        preventDefault: false,
                        HWCompositing: $(window).width() >= 768 ? false : true,
                    });
                }, 100)
                $this.on('touchstart', mEvent);
                $this.on('touchmove', mEvent);
                $this.on('touchend', mEvent);
            });
        };

    };
    //幻灯片
    function slider(ele, par) {
        if ($(window).width() > 786) {
            // var num=1;
            ele.colorbox({
                rel: ele.attr("class"),
                slideshow: true,
                photo: true,
                onOpen: function() {
                    $("#colorbox").css("outline", "none");
                    $("[data-elementtype]").length != 0 && $("body").append("<p style='position:fixed;z-index:10000;top:10px;right:10px' class='btnControlClose'><i class='pictureShowClose'></i></p><p style='position:absolute;z-index:9999;top:0;left:0;height:100%;width:150px' class='btnControl'><i class='pictureShowL '></i></p><p style='position:absolute;z-index:9999;top:0;right:0;height:100%;width:150px' class='btnControl'><i class='pictureShowR'></i></p>");
                    $("#cboxPrevious,#cboxNext,#cboxClose,#cboxSlideshow,#cboxLoadingGraphic,.cboxLoadingOverlay").css("opacity", 0);
                    $(".pictureShowL,.pictureShowR").hide();
                    $("#cboxLoadedContent").css({
                        "overflow": "hidden"
                    });
                    $(".btnControl,.pictureShowClose").show();
                    $("#cboxClose").css("opacity", 0);
                    // $("#cboxOverlay,#colorbox").css("display", "block");
                    ele.parents(par).find("a[href='javascript:void(0)']").each(function() {
                        var $a = $(this);
                        $a.attr({
                            "saveHref": $(this).attr("href"),
                            "href": $a.parents(".atlasWrap3,.atlasWrap4,.atlasWrap5").length != 0 ? $a.css("background-image").replace(/\"|\(|\)|url/g, "") : $a.find("img").attr("src"),
                        });
                    });
                },
                onComplete: function(e) {
                    //第一项的蒙版设置
                    $("#cboxLoadedContent").css({
                        position: "relative"
                    }).find("div").remove().end().append("<div style='background-color:" + $(this).find("div").css("background-color") + ";position:absolute;top:0;left:0;width:100%;height:100%;'></div>");
                    $(this).colorbox.resize();
                },
                next: "",
                previous: "",
                slideshowStart: "",
                slideshowStop: "",
                close: "",
                speed: 0,
                preloading: !0,
                fixed: !0,
                current: "",
                slideshowAuto: !1,
                loop: !1,
                onClosed: function() {
                    ele.parents(par).find("a[saveHref]").each(function() {
                        $(this).attr({
                            "href": $(this).attr("saveHref"),
                        });
                    });
                    return false;
                },
                opacity: 0.5,
                maxWidth: ($(window).width() > 786) ? "60%" : "90%",
                maxHeight: "90%"
            });
        };
    };
    //手机事件
    var startX, startY, moveX, moveY;

    function mEvent(e) {
        if (e.type == "touchstart") {
            touch = e.originalEvent.changedTouches[0];
            startX = touch.pageX;
            startY = touch.pageY;
            // e.preventDefault();
        } else if (e.type == "touchmove") {
            touch = e.originalEvent.changedTouches[0];
            moveX = touch.pageX;
            moveY = touch.pageY;
            if (Math.abs(moveY - startY) / Math.abs(moveX - startX) < 1) {
                e.preventDefault();
            };
        } else if (e.type == "touchend") {
            // touch = e.targetTouches[0]
            // moveX = touch.pageX;
            // moveY = touch.pageY;
            // if (Math.abs(moveY - startY) < 100) {
            //     e.preventDefault();
            // };
            // e.target.removeEventListener('touchmove',phone.move, false);
            // e.target.removeEventListener('touchend', phone.end, false);
        };
    };
    //中心弹出
    function centerModal($modal,$source){
      var centerX=$source.offset().left+$source.width()*0.5;
      var centerY=$source.offset().top+$source.height()*0.5;
      $modal.css({
        "transform-orgin":centerX+"px  "+centerY+"px",
        "transform":"scale(0)"
      });
    };

});
