/**
 * Created by M on 2017/5/11.
 */
(function ($) {
    var wqdVideo = {};
    wqdVideo.init = function () {
        this.bindEvent();
        wqdVideo.scroll()
    };
    wqdVideo.bindEvent = function (e) {
        var self = this;

        $(document).on("click",".wqdVideo .play,.wqdVideo .screenage",function() {

            var $parents=$(this).parents(".wqdelementEdit.wqdVideo");

            var $video = $parents.find("video");

            if (!$video.attr("vsrc"))return;

            $('<source src=' + $video.attr("vsrc") + ' type="video/mp4">').appendTo($video);

            new MediaEdit($parents);

            $parents.find(".play").trigger("click");

        });


        $(window).on("scroll", self.scroll);


    };

    wqdVideo.scroll=function() {

        var $elements = $(".wqdVideo[autoplay=autoplay]");
        var $visibleElement = $elements.filter(function () {
            var $e = $(this),
                $w = $(window),
                wt = $w.scrollTop(),
                wb = wt + $w.height(),
                et = $e.offset().top,
                eb = et + $e.height();

            return et >= wt && eb <= wb && $e.is(":visible");
        });


        $visibleElement.each(function (i, _) {

            var isPlaying = $(this).find("video")[0].currentTime > 0 && !$(this).find("video")[0].paused && !$(this).find("video")[0].ended && $(this).find("video")[0].readyState > 2;

            if (isPlaying || $(this).find("video")[0].currentTime > 0 || $(this).data("end")=="1")return; //单独处理自动播放  而且只播放一次  因为手机端要出发两次

            var $video = $(this).find("video");

            if (!$video.attr("vsrc"))return;


            if(!$video.find("source").length){
                $('<source src=' + $video.attr("vsrc") + ' type="video/mp4">').appendTo($video);

                new MediaEdit($(_));//自动播放需要自动加载

            }

            $(this).find(".play").trigger("click");

        });


    };

    $(document).on('touchstart', wqdVideo.scroll);


    function MediaEdit(dom){
        if (typeof(dom) != "object")return;

        this.dom=dom;
        this.elementId = dom.attr("elementid");//获取id
        this.$video = dom.find("video"); //视频
        this.$screenage = dom.find(".screenage");//中间的播放按钮
        this.$poster = dom.find(".poster"); //背景图片
        this.$layer = dom.find(".layer"); //背景遮罩
        this.$play = dom.find(".play"); //播放按钮
        this.$totalTime = dom.find(".remain");//总时间
        this.$currentTime = dom.find(".current");//当前播放时间
        this.$process = dom.find(".process");//总进度
        this.$loading = dom.find(".loading");//当前播放的进度
        this.$point = dom.find(".point");//当前播放的推进圆球
        this.$volume = dom.find(".volume");//音量控制
        this.$volumeWrap = dom.find(".volume-wrap");//音量进度
        this.$volumePoint = dom.find(".volume-point");//音量小球
        this.$curVolume = dom.find(".volume-progress");//音量进度
        this.$rePlay = dom.find(".re-play");//重播按钮
        this.$fullScreen = dom.find(".full-screen");//全屏按钮
        this.$controls= dom.find(".controls");//控制条

        this.ratio = (this.$point.width() / 2) / this.$process.width();//得到视频进度圆球所占的比例

        this.volumeRatio=(this.$volumePoint.width() / 2) / this.$volumeWrap.width();//得到音量进度圆球所占的比例


        this.origWidth = dom.width();  this.origHeight = dom.height(); this.origTop = dom.position().top; this.origLeft = dom.position().left;


        this.init();
    }


    $.extend(MediaEdit.prototype,{

        init:function() {

            this.initialize();

            this.bindEvent();
        },


        initialize:function() {

            this.autoplay=this.dom.attr("autoplay");

            this.loop=this.dom.attr("loop");

            var dataStyle = this.dom.attr("data-style") || "";

            var initVolume=(this.getAttribute(dataStyle,"initVolume")||50)/100;

            this.$video[0].volume = initVolume;//初始化音量

            this.$volume.data("volume", initVolume);//记录初始音量

            this.$curVolume.css('width', 100*initVolume + '%');//音量的进度条

            this.$volumePoint.css('left',100*(initVolume -  this.volumeRatio) + '%');//音量进度圆球


            var speed=this.getAttribute(dataStyle,"speed")|| '1x';

            this.$video[0].playbackRate = speed.substr(0,speed.length-1); //初始化播放速度

        },
        bindEvent:function() {

            var self=this;


            self.$video.on('loadedmetadata', function () { //媒体数据加载完成 (这个节点比canplay早)

                if (self.dom.data("end")=="1")self.dom.data("end", "0");

                self.$screenage.addClass("on");

                var duration=self.getFormatTime(this.duration);

                self.$totalTime.text(duration); //写入总时间

                //鉴别为手机端则另外添加总时间节点
                if ($(this).parents(".wqdIphoneView").length) $("<span class='duration'>"+duration+"</span>").appendTo(self.$layer);

            });


            self.$video.on('timeupdate', function () {//监控时间更新


                self.$currentTime.text(self.getFormatTime(this.currentTime));

                self.$loading.css('width', 100 * this.currentTime / this.duration + '%');

                self.$point.css('left', (self.$loading.width() - 6) + "px");

            });

            self.$video.on('playing', function() {//移动端兼容浏览器自己渲染的控制条

                !self.$screenage.hasClass("hide") && self.$screenage.addClass("hide");
                if(!self.identifyBrowser() && self.dom.parents(".wqdIphoneView").length)self.dom.find(".duration").remove();//如果是手机端并且不是uc 或者qq浏览器删掉视频时间节点

            });

            self.$video.on('pause', function() { //移动端兼容浏览器自己渲染的控制条

                self.$screenage.hasClass("hide") && self.$screenage.removeClass("hide");

            });





            self.$video.on('ended', function() {//监控视频结束 事件

                self.$loading.css('width', 0 );

                self.$point.css('left', -(self.$point.width() / 2));

                self.$currentTime.text( self.getFormatTime() );

                self.$video[0].currentTime = 0;

                self.$play.removeClass("on");
                self.$video.removeClass("on");
				self.$layer.removeClass("on");

                if(self.loop && self.$screenage.trigger("click"))return; //自动播放配置

                self.$screenage.removeClass("hide");

                if (self.dom.parents(".wqdIphoneView").length)self.dom.data("end", "1");


            });


            self.$volume.on("click", function (e) { //点击音量按钮

                var curVolume=parseFloat($(this).data("volume"));

                if(!curVolume)return;

                $(this).toggleClass("on");

                var flag = $(this).hasClass("on") ? true : false;

                //$video[0].muted = !flag;//关闭
                self.$video[0].volume = flag ? 0 : curVolume ;


                self.$curVolume.css('width', flag ? 0 : 100 * curVolume + '%');//当前播放的进度


                self.$volumePoint.css('left', flag ? -(self.$volumePoint.width() / 2) : 100 * (curVolume -  self.volumeRatio) + '%');//当前播放的进度圆球

                e.stopPropagation();
                return false;

            });


            self.$volumeWrap.on('click', function (e) { //音量跳跃
                e = e || window.event;

                self.jumpingV(e);

                e.stopPropagation();
                e.preventDefault();
                return false;
            });


            self.$process.on('click', function (e) { //跳跃播放

                //if (!self.$screenage.hasClass("on hide"))return;//如果不能播放或者没有正在播放 禁止

                e = e || window.event;

                self.jumpingP(e);

            });


            self.$point.on("mousedown.point", function (e) {//拖动视频

                //if (!self.$screenage.hasClass("on hide"))return;
                e.stopPropagation();
                e.preventDefault();

                $(document).off("mousemove.point").on("mousemove.point", function (e) {

                    self.jumpingP(e);

                }).off("mouseup.point").on("mouseup.point", function () {

                    $(document).off("mousemove.point").off("mouseup.point");
                })

            });


            self.$volumePoint.on("mousedown.volume", function (e) {//拖动音量

                e.stopPropagation();
                e.preventDefault();

                $(document).off("mousemove.volume").on("mousemove.volume", function (e) {

                    self.jumpingV(e);

                }).off("mouseup.volume").on("mouseup.volume", function () {

                    $(document).off("mousemove.volume").off("mouseup.volume");

                })

            });



            self.$rePlay.on('click', function (e) {//重播

                if (! self.$screenage.hasClass("on hide"))return;

                self.$loading.css('width', 0 );

                self.$point.css('left', -(self.$point.width() / 2));

                self.$currentTime.text( self.getFormatTime() );

                self.$video[0].currentTime = 0;

            });


            self.dom.off("click.play").on("click.play", ".play,.screenage.on,video,.layer", function(e) { //绑定播放

                e.stopPropagation();
                e.preventDefault();
                e = e || window.event;
                e.target = e.target || e.srcElement;

                if (self.dom.parents(".wqdIphoneView").length && e.target.tagName.toLowerCase() === "video")return;


                if (e.target.tagName.toLowerCase() === "video" && !$(".screenage.on").hasClass("hide"))return;

                var isPlaying = self.$video[0].currentTime > 0 && !self.$video[0].paused && !self.$video[0].ended && self.$video[0].readyState > 2;

                if(self.identifyBrowser()){
                    if (!isPlaying)self.$video[0].play();
                    return;
                }

                if (!isPlaying) {
                    self.$video[0].play();
                    self.exchangeBtnStatus("play",  true);
                }else{
                    self.$video[0].pause();
                    self.exchangeBtnStatus("play",  false);
                }

            });


            ["fullscreenchange", "webkitfullscreenchange", "mozfullscreenchange", "MSFullscreenChange"].forEach(function (eventType) {

                document.addEventListener(eventType, function (event) {

                    if($("body").data("fullElement")!= self.elementId ) return;

                    if (self.isFullScreen()) { //全屏
                        var cltHeight = window.screen.height, cltWidth = window.screen.width;

                        self.dom.css({  width: cltWidth, height: cltHeight, top: 0, left: 0 });

                        self.exchangeBtnStatus("fullscreen", true);


                    } else {//退出全屏

                        self.dom.css({  width: self.origWidth, height: self.origHeight, top: self.origTop, left: self.origLeft });

                        self.exchangeBtnStatus("fullscreen", false);

                    }

                    self.$point.css('left', (self.$loading.width() - 6) + "px");//监控屏幕变化

                })
            });

            self.$fullScreen.on("click", function () {
                if (!self.isFullScreen()) {

                    $("body").data("fullElement", self.elementId);

                    // go full-screen
                    if (self.dom[0].requestFullscreen) {
                        self.dom[0].requestFullscreen();
                    } else if (self.dom[0].webkitRequestFullscreen) {
                        self.dom[0].webkitRequestFullscreen();
                    } else if (self.dom[0].mozRequestFullScreen) {
                        self.dom[0].mozRequestFullScreen();
                    } else if (self.dom[0].msRequestFullscreen) {
                        self.dom[0].msRequestFullscreen();
                    }
                } else {
                    // exit full-screen
                    if (document.exitFullscreen) {
                        document.exitFullscreen();
                    } else if (document.webkitExitFullscreen) {
                        document.webkitExitFullscreen();
                    } else if (document.mozCancelFullScreen) {
                        document.mozCancelFullScreen();
                    } else if (document.msExitFullscreen) {
                        document.msExitFullscreen();
                    }
                }
            });

        },

        exchangeBtnStatus: function (element, bool) { //播放切换状态

            if (element == "play") {//播放按钮的切换状态
                if (bool) {
                    this.$poster.addClass("on");
                    this.$video.addClass("on");
                    this.$play.addClass("on");
                    this.$screenage.addClass("hide");
                    this.$layer.addClass("on");

                } else {
                    this.$play.removeClass("on");
                    //if(!this.dom.parents(".wqdIphoneView").length)this.$screenage.removeClass("hide");//pc端如果暂停出现全屏的
                    this.$screenage.removeClass("hide");
                    this.$layer.removeClass("on");
                }
            }
            if (element == "fullscreen") {//全屏按钮的切换状态

                this.$controls.toggleClass("fullControll", bool);

                this.$fullScreen.toggleClass("on", bool);


            }

        },

        isFullScreen: function () {
            return document.fullscreenElement ||
                document.webkitFullscreenElement ||
                document.mozFullScreenElement ||
                document.msFullscreenElement;
        },

        getFormatTime: function (time) {

            var time = time || 0;

            var h = parseInt(time / 3600),
                m = parseInt(time / 60),
                s = parseInt(time % 60);
            h = h < 10 ? "0" + h : h;
            //m = m < 10 ? "0" + m : m;
            s = s < 10 ? "0" + s : s;

            return  m + ":" + s;
        },

        jumpingP:function(e) { //跳跃播放视频

            var self = this;

            var positions = Math.max(0,Math.min(self.$process.width(),e.pageX -  self.$process.offset().left)); //Click pos

            var percentage = 100 * positions /  self.$process.width();

            self.$loading.css('width', percentage + '%');

            //self.$point.css('left', percentage - (100 *  self.ratio) + '%');
            self.$point.css('left', (self.$loading.width() - 6) + "px");//监控并且兼容全屏


            var curTime=percentage/100 *  self.$video[0].duration;

            self.$currentTime.text( self.getFormatTime(curTime) );

            self.$video[0].currentTime = curTime;

        },

        jumpingV:function(e) { //跳跃播放音量

            e.cancelable=false;

            var self = this;

            var positions = Math.max(0, Math.min(self.$volumeWrap.width(),e.pageX - self.$volumeWrap.offset().left));//点击的绝对位置

            var volumeScale = positions / self.$volumeWrap.width();//此时的音量比例

            self.$curVolume.css('width', 100 * volumeScale + '%');//当前音量的进度

            self.$volumePoint.css('left', 100 * (volumeScale -  self.volumeRatio) + '%');//当前音量的进度圆球


            self.$video[0].volume = volumeScale;
            self.$volume.data("volume", volumeScale); //记录变化音量


            self.$volume.toggleClass("on", volumeScale <= 0);

        },

        getAttribute: function (objString, name) { //得到设置data style的具体样式

            if (!objString || !name) return "";
            var paramVal = "",
                paramObj = {};
            $.each(objString.split(";"), function (i, _) {
                if (!_) return true;
                var key = _.split(":");
                paramObj[key[0]] = key[1];
            });
            paramVal = paramObj[name] || "";

            return paramVal;

        },

        identifyBrowser:function() {//鉴别手机端 uc和qq浏览器浏览器

            return((navigator.userAgent.indexOf('UCBrowser') > -1 || navigator.userAgent.indexOf('QQBrowser') > -1) && $(this).parents(".wqdIphoneView").length);

        }


    });




    wqdVideo.init();

})($);