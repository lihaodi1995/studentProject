$(function() {
    /**
     * [简单模板方法，用来组装字符串 liumingren]
     * 仅替换，可用来替换变量生成字符串。未加入常见的each等操作，后续可使用流行的模板引擎
     * @param {[string]} 模板 格式为{{key}} , {{key|方法名 参数}} || {{key [运算符] key }} 可多个
     *          {{key|to [比较字符串] 返回值}} 当有比较字符串时，比较key是否等于比，是则返回返回值，无比较字符串时，判断是否有key的数据
     * @param {[object|array]} 替换的对象数据 格式为 (模板:值),多个放在数组里，多个可做each使用,{{INDEX}}为下标
     * @return {[string]} [替换后的htmlString]
     */
    var format = function(){
        var args = [].slice.call(arguments),str = String(args.shift() || ""), ar = [], first = args[0];
        args = $.isArray(first) ? first : typeof(first) == 'object' ? args : [args];
        var filter = {
                to : function (q,d,o) {
                    return d.length > 1 ? o[q] === d[0] ? d[1] : void 0 : o[q] ? d[0] : void 0;
                }
            },
            opp = function (o,exp,par) {
                var reg = /[a-zA-Z]/g;
                var exn = exp.replace(/([^\s\(\)\+\*\/]+)/g,function(m){
                    return reg.test(m) ? o[m] || "n" : m
                });
                return reg.test(exn) ? o[par] : new Function( "return " + exn )()
            };
        $.each(args, function(i, o){
            ar.push(str.replace(/\{\{([\d\w\.\-\@\_\(\)\*\+\/\|\s]+)\}\}/g, function(m, n){
                var reg = /\*\d+(\.\d+)?/g,op=/\*|\d|\+|\//g,v;
                n.replace(/([^|]*)\|([^|]+)/g,function(p,q,r){
                    var s = r.split(/\s+/g);
                    if(filter[s[0]]){
                        v = filter[s[0]](q,s.slice(1),o);
                    }
                });
                // if(!o[n]) n = n.replace(/\-hover|\-active/g,"");
                if(!v) v = n === 'INDEX' ? i : op.test(n) ? opp(o,n) : o[n];
                return v === undefined ? m : ($.isFunction(v) ? v.call(o, n) : v)
            }));
        });
        return ar.join('');
    };
    var artLiTemp;
    var articleList = {
        init:function () {
            this.allLoadNews();
            this.bindEvent();
        },
        bindEvent:function () {
            var self = this;
            $(document)
                .on("click",".newArticleList .artListPaging li",function (e) {
                    var $elem = $(this).parents(".newArticleList");
                    self.loadCurrentNews($elem,{
                        pageNo:$(this).attr("data-index")
                    });
                });
        },
        /**
         * 页面中的列表载入数据
         */
        allLoadNews:function () {
            var self = this;
            $(".wqdelementEdit.newArticleList").each(function (i,_) {
                self.loadNews($(_));
            });
        },

        /**
         * 列表控件载入数据
         */
        loadNews:function ($this,isFirstLoad,isPageLoad) {
            if($this.attr("data-tagid") || this.getAttr("orderby",$this) || $this.attr("data-artltype") == "static") this.loadCurrentNews($this);
        },
        /**
         * 载入文章列表数据
         */
        loadCurrentNews:function ($elem,data) {
            var self = this,
                isdynamic = $elem.attr("data-artltype") == "dynamic",html,url;
            data = data || {};
            if(isdynamic) {
                data.tagIds = data.tagIds || $elem.attr("data-tagid") || "";
                data.pageNo = data.pageNo || 0;
                data.pageSize = data.pageSize || this.getAttr("page-size",$elem) || 1;
                data.orderBy = data.orderBy || this.getAttr("orderby",$elem) || "PUBLISH_TIME";
                data.isPublish = true;
                url = "/article/page";
            }else {
                url = "/article/pageIds";
                data = {
                    ids : $elem.find('.artlist >li[data-id]').map(function(i, _){
                        return $(_).attr('data-id')||null
                    }).get().join(",")
                }
            }

            var tempPromise = this.getTempalte($elem);
            $.when(tempPromise).done(function () {
                $.get(url,data,function (data) {
                    if(!$.isArray(data.data.data) || data.endRows == 0) {
                        html = "";
                    } else {
                        html = self.getFormatedNews($elem,data.data.data);
                    }
                    $elem.find("ol.artlist").html(html);
                    if(isdynamic) self.showPaging(data.data,$elem);
                });
            })
        },
        getTempalte:function () {
            var tempPromise = $.Deferred(),self = this;
            if(artLiTemp) {
                tempPromise.resolve();
            } else {
                $.getJSON("../js/template/articleListTemp.json").done(function(json){
                    artLiTemp = json;
                    tempPromise.resolve();
                })
            }
            return tempPromise;
        },
        /**
         * 获取格式化的列表数据
         * @param data
         * @returns {string|*}
         */
        getFormatedNews:function ($elem,data) {
            var self = this,
                pageId = $elem.attr("data-pageid"),
                type = self.getAttr("model",$elem) || "model1",
                lis = [];
            data = $.isArray(data) ? data : [data];
            $.each(data,function(index, value) {
                lis.push(format(artLiTemp[type],{
                    id:value.id,
                    title:value.title,
                    time:self.formatTime($elem,value.publishTime || ""),
                    pv:value.pv || 0,
                    top:value.top,
                    negative:value.negative,
                    favourable:value.favourable||0,
                    summary:value.summary || value.descn,
                    image:value.icon ? CSSURLPATH + value.icon : value.otherIcons ? value.otherIcons.split(",")[0] : "http://img.wqdian.com/group4/M00/7E/18/yq0KYVdhQ5mABvPGAAB1StSglTI587.png",
                    url:pageId ? "page_" + pageId + "_" + value.id : "",
                    tag:value.categoryName ? format("<span>{{tag}}</span>",$.map(value.categoryName.split(","),function (v,i) {
                        return i > 2 ? null : {
                            tag:v
                        };
                    })) : ""
                }));
            });
            return lis.join("");
        },
        getAttr:function (type,$elem) {
            $elem = $elem || this.$element;
            var style    = $elem.attr("data-style")||"",
                reg      = new RegExp(type+":([^;]*);","g"),
                value;
            style.replace(reg,function (m,n) {
                value = n;
            });
            return value;
        },
        /**
         *  设置分页
         */
        showPaging:function (data,$elem,number) {
            $elem = $elem || this.$element;
            number = number || 5;
            var secLast = number-1,
                start   = data.pageNo < Math.ceil(number/2+1) ? 1 :
                            data.totalPages - data.pageNo > Math.floor(number/2) ? data.pageNo - Math.floor(number/2) :
                                data.totalPages > secLast ? data.totalPages - secLast : 1,
                end     = start > data.totalPages - secLast ? data.totalPages : start + secLast;
            var temp = '<li data-index="{{index}}" class="{{class}}">{{text}}</li>',
                pagingModel = [],
                pagingStyle = this.getAttr("paging.type",$elem) || "artlPagingStyle2",
                $artlPaging = $elem.find('.artListPaging');
            $artlPaging.attr("class",$artlPaging.attr("class").replace(/artlPagingStyle\d/g,pagingStyle))
            end = end > data.totalPages ? data.totalPages : end;
            if(end == 1) {
                return $artlPaging.html("").hide();
            }
            for(var i = start ;i <= end ;i++){
                var isEnd = i == end;
                pagingModel.push({
                    index:i,
                    class:i == data.pageNo ? "on" : "",
                    text:i
                });
                if(i == start) {
                    pagingModel.unshift({
                        index:1,
                        class:"first",
                        text:pagingStyle=="artlPagingStyle1" ? "<<": "首页"
                    },{
                        index:data.pageNo-1,
                        class:"prev",
                        text:pagingStyle=="artlPagingStyle1" ? "<": "上一页"
                    });
                }
                if(isEnd) {
                    pagingModel.push({
                        index:data.pageNo + 1,
                        class:"next",
                        text:pagingStyle=="artlPagingStyle1" ? ">": "下一页"
                    },{
                        index:data.totalPages,
                        class:"last",
                        text:pagingStyle=="artlPagingStyle1" ? ">>": "末页"
                    });
                }
            }
            $artlPaging.html(format(temp,pagingModel)).show();
        },
        /**
         * 格式化时间
         * @param $elem
         * @param timeText
         * @param timetype
         * @returns {*}
         */
        formatTime:function ($elem,timeText,timetype) {
            timeText = $.trim(timeText).replace(/\s+(.+)+/g,"");
            var rxp     = /([0-9]+).([0-9]+).([0-9]+)(?:.)?/g,val;
            timetype = timetype || this.getAttr("time.type",$elem) || 1;
            if(timetype != 3){
                var sep = ["-","/","."][timetype];
                val = timeText.replace(rxp,'$1'+sep+'$2'+sep+'$3');
            } else {
                val = timeText.replace(rxp,'$1年$2月$3日');
            }
            return val;
        }
    };
    articleList.init();
});
