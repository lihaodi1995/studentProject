$(function() {
	var commodityList = {};

	commodityList.init = function(){
		this.commonInit();
		this.outsideEvent();
	};
	commodityList.commonInit = function(){
		$(document).on("mouseenter",".categoryFirst > li > a",function(){
			$(this).parent().siblings("li").find(".categorySecond").hide();
			$(this).siblings(".categorySecond").show();
		}).on("mouseleave",".categoryFirst > li",function(){
			$(this).find(".categorySecond").hide();
		}).on("mouseenter",".categorySecond > li > a",function(){
			if(!$(this).siblings(".categoryThird").length) return;
			var li = $(this).parent(),
				third = $(this).siblings(".categoryThird").css("left","100%"),
				left = -(third.width()||0);
			li.offset().left + li.outerWidth() + third.outerWidth() > $(window).width() && third.css("left",left);
			//li.index() != 0 && third.find("li").length > li.index() && third.css("top",-li.position().top);
			li.siblings("li").find(".categoryThird").hide();
			third.show();
		}).on("mouseleave",".categorySecond > li",function(){
			$(this).find(".categoryThird").hide();
		});

		this.updataModity();	//更新数据
	}
	//发布后
	commodityList.outsideEvent = function(){
		//浏览分类数据
		$(document).on("click",".modityCategory a",function(){
			//if($(this).hasClass("active")) return;
			var contactId = $(this).parents(".wqdcommodityCategory").attr("wqdmark") || "ssss",
				modityDom = $(".wqdcommodityList[wqdmark="+contactId+"]"),
				stype = modityDom.attr("sorttype") || "time",
				USERID = modityDom.attr("userid") || "",
				categoryid = $(this).attr("data-category") || (modityDom.attr("data-categoryids") ? modityDom.attr("data-categoryids") : "");
			commodityList.requestDate("/fixed/item/getItems",{userId:USERID,categoryId:categoryid,sortType:stype},function(data){
				modityDom.data("cacheData",data.data);	//缓存数据
				data.status == 200 && commodityList.dataInit.call(modityDom,data.data);
			});
			$(this).parents(".wqdcommodityCategory").find(".modityCategory a").removeClass("active");
			$(this).addClass("active");
			$(this).parents(".categoryThird").siblings("a").addClass("active");
			$(this).parents(".categorySecond").siblings("a").addClass("active");
		}).on("click",".wqdcommodityList .admireMark svg",function(event){		//点赞
			return;  //列表不用点赞了，暂时保留代码
			event.stopPropagation();
			event.preventDefault();
			if($(this).parent().hasClass("active")) return;
			var that = $(this),
				modityId = that.parents(".commodityWrap").parent().attr("data-modity") || "!!!!!!";
			$.ajax({
	            type: "post",
	            url: "/fixed/item/review",
	            data : {modityId:modityId},
	            dataType: "json",
	            success:function(data){
	            	if(data.status == 200){
	            		that.parent().addClass("active").end().siblings("span").text(that.siblings("span").text()-0+1);
	            		commodityList.setCookie(modityId,"admire");
	            	}else{
	            		alert(data.msg)
	            	}
	            }
	        });
		}).on("click",".pagingWrap .pagingBtn, .pagingWrap .pagingList li",function(){	//翻页
			if($(this).hasClass("active")) return;
			var parent = $(this).parents(".pagingWrap"),
				pagenum = null,
				index = parent.find(".pagingList li.active").text()-1,
				maxVal = parent.find(".pagingList li:last-child").text()-0,
				modityDom = $(this).parents(".wqdcommodityList");
			if($(this).hasClass("firstPage")){	//首页
				if(index == 0) return;
				pagenum = 0;
				commodityList.caeatePaging.call(parent,1,1,maxVal);
			}else if($(this).hasClass("prevPage")){		//上一页
				if(index == 0) return;
				pagenum = index - 1;
				if(parent.find(".pagingList li:first-child").hasClass("active")){
					commodityList.caeatePaging.call(parent,index,index,maxVal);
				}else{
					parent.find(".pagingList li.active").prev().addClass("active").siblings().removeClass("active");
				}
			}else if($(this).hasClass("nextPage")){		//下一页
				if(parent.find(".pagingList li:last-child").hasClass("active")) return;
				pagenum = index + 1;
				if(parent.find(".pagingList li.active").next().text()=="..."){
					var star = maxVal-pagenum>6 ? pagenum+1 : maxVal-6;
					commodityList.caeatePaging.call(parent,star,pagenum+1,maxVal);
				}else{
					parent.find(".pagingList li.active").next().addClass("active").siblings().removeClass("active");
				}
			}else if($(this).hasClass("lastPage")){		//末页
				if(parent.find(".pagingList li:last-child").hasClass("active")) return;
				pagenum = parent.find(".pagingList li:last-child").text()-1;
				var star = maxVal>6 ? maxVal-6 : 1;
				commodityList.caeatePaging.call(parent,star,maxVal,maxVal);
			}else{
				if(parent.find(".pagingList li:last-child").text()-parent.find(".pagingList li:first-child").text()>6){
					var html = "";
					if($(this).index() == 5){
						pagenum = $(this).prev().text() - 0;
						var star = maxVal-$(this).prev().text()>6 ? pagenum + 1 : maxVal-6;
						commodityList.caeatePaging.call(parent,star,pagenum+1,maxVal);
					}else if($(this).index() == 6){
						pagenum = maxVal - 1;
						commodityList.caeatePaging.call(parent,maxVal-6,maxVal,maxVal);
					}else{
						pagenum = $(this).text() - 1;
						$(this).addClass("active").siblings().removeClass("active");
					}
				}else{
					pagenum = $(this).text() - 1;
					$(this).addClass("active").siblings().removeClass("active");
				}
				
			}
			var cacheData = modityDom.data("cacheData") || [];
				dataStyle = modityDom.attr("data-style") || "",
				column = commodityList.getParam(dataStyle,"modity-column") || 4,
				row = commodityList.getParam(dataStyle,"modity-row") || 1,
				star = row*column*pagenum,
				dataArr = cacheData.slice(star);
			commodityList.dataInit.call(modityDom,dataArr,true);
		});	
	};
	//生成分页
	commodityList.caeatePaging = function(star,active,maxVal){
		var html = "";
		for(var k=star; k<star+7 && k<=maxVal; k++){
			if(k == active){
				html += '<li class="hoverBtn active">'+k+'</li>';
			}else if(k == star+5 && maxVal-star > 6){
				html += '<li class="hoverBtn">...</li>';
			}else if(k == star+6 && maxVal-star > 6){
				html += '<li class="hoverBtn">'+maxVal+'</li>';
			}else{
				html += '<li class="hoverBtn">'+k+'</li>';
			}
		}
		$(this).find(".pagingList").html(html);
	};
	commodityList.requestDate = function(url,data,callback) {
		$.ajax({
            type: "GET",
            url: url,
            data : data,
            dataType: "json",
            success:callback
        });
	};
	//更新数据
	commodityList.updataModity = function(){
		$(".wqdcommodityCategory").each(function(){
			var that = $(this),
				contactId = $(this).attr("wqdmark") || "ssss",
				USERID = $(".wqdcommodityList[wqdmark="+contactId+"]").attr("userid") || "",
				categoryIds = $(".wqdcommodityList[wqdmark="+contactId+"]").attr("data-categoryIds") || "";
			commodityList.requestDate("/fixed/item/getAllCategory",{userId:USERID},function(data){
				//commodityList.categoryData = data.data;		//缓存数据
				data.status == 200 && commodityList.categoryInit.call(that,commodityList.getCatetoryDate(data.data, categoryIds));
			});
		});
		$(".wqdcommodityList").each(function(){
			var that = $(this),
				USERID = that.attr("userid") || "",
				stype = $(this).attr("sorttype") || "time",
				categoryIds = that.attr("data-categoryIds") || "";
			commodityList.requestDate("/fixed/item/getItems",{userId:USERID,categoryId:categoryIds,sortType:stype},function(data){
				that.data("cacheData",data.data);	//缓存数据
				data.status == 200 && commodityList.dataInit.call(that,data.data);
			});
		});
	};
	//渲染分类
	commodityList.categoryInit = function(data){
		var html = "";
		if(data && data.length){
			html += '<div class="categoryAll"><a href="javascript:void(0);" class="active">全部分类</a></div><ul class="categoryFirst">';
			for(var i=0; i<data.length; i++){
				html += '<li><a href="javascript:void(0);" data-category='+data[i].categoryId+'>'+data[i].name+'</a>';
				if(data[i].child && data[i].child.length){
					html += '<ul class="categorySecond">';
					for(var j=0; j<data[i].child.length; j++){
						html += '<li><a href="javascript:void(0);" data-category='+data[i].child[j].categoryId+'>'+data[i].child[j].name+'</a>';
						if(data[i].child[j].child && data[i].child[j].child.length){
							html += '<ol class="categoryThird">';
							for(var k=0; k<data[i].child[j].child.length; k++){
								html += '<li><a href="javascript:void(0);" data-category='+data[i].child[j].child[k].categoryId+'>'+data[i].child[j].child[k].name+'</a></li>';
							}
							html += '</ol>';
						}
						html += '</li>';
					}
					html += '</ul>';
				}
				html += '</li>';
			}
			html += '</ul>';
		}
		$(this).find(".modityCategory").html(html);
	};
	//渲染商品信息
	commodityList.dataInit = function(data,bool){
		var pageNum = 0,
			USERID = $(this).attr("userid") || "",
			pageId = $(this).attr("data-pageid") || "",
			modityStr = "",
			pagingStr = "",
			dataStyle = $(this).attr("data-style") || "",
			column = parseInt(commodityList.getParam(dataStyle,"modity-column") || 4),
			row = parseInt(commodityList.getParam(dataStyle,"modity-row") || 1);
		if(data && data.length){
			pageNum = parseInt(data.length/(column*row));
			pageNum = data.length % (column*row) == 0 ? pageNum : pageNum+1;
			for(var i=0; i<data.length && i<column*row; i++){
				i % column == 0 && i != 0 && (modityStr += '</ol></li>');
				var parentStr = i % column == 0 ? '<li><ol class="list_row">' : "",
					modityCookie = commodityList.getCookie(data[i].id),
					act_class = modityCookie ? "" : "",	//现在只作展示没有选中效果，代码保留
					_blank = data[i].widowsType=="news" ? ' target="_blank"' : "",
					hrefUrl = pageId ? "pageItem_"+pageId+"_"+data[i].id+".html?catch="+USERID : "javascript:;";
					hrefUrl =  data[i].detailsType=="external" ? data[i].itemLink : hrefUrl;
				modityStr += parentStr+'<li data-modity="'+data[i].id+'"><a'+_blank+' href="'+hrefUrl+'" class="commodityWrap">';
				modityStr += '<div class="modityImg"><img src="' + CSSURLPATH+data[i].picPath.split(",")[0] +'"></div>';
				modityStr += '<div class="textMessage"><p class="moditDescribe">'+data[i].name+'</p>';
				modityStr += '<div class="modityMark clearfix"><div class="priceMark">';
				modityStr += '<div class="nowPrice commomPrice">¥<span>'+data[i].currentPrice+'</span></div>';
				modityStr += '<div class="originalPrice commomPrice">¥<span>'+data[i].originalPrice+'</span></div></div>';
				modityStr += '<div class="countMark"><div class="admireMark'+act_class+'"><svg class="admireSvg" viewBox="-250 -250 2392 2392" xmlns="http://www.w3.org/2000/svg"><path fill="#999" d="M1664 596q0-81-21.5-143t-55-98.5-81.5-59.5-94-31-98-8-112 25.5-110.5 64-86.5 72-60 61.5q-18 22-49 22t-49-22q-24-28-60-61.5t-86.5-72-110.5-64-112-25.5-98 8-94 31-81.5 59.5-55 98.5-21.5 143q0 168 187 355l581 560 580-559q188-188 188-356zm128 0q0 221-229 450l-623 600q-18 18-44 18t-44-18l-624-602q-10-8-27.5-26t-55.5-65.5-68-97.5-53.5-121-23.5-138q0-220 127-344t351-124q62 0 126.5 21.5t120 58 95.5 68.5 76 68q36-36 76-68t95.5-68.5 120-58 126.5-21.5q224 0 351 124t127 344z"></path></svg>';
				modityStr += '<span>'+data[i].favorable+'</span></div><div class="salesMark">已售出<span>'+data[i].salesVolume+'</span>件</div></div></div></div></a></li>';
			}
			modityStr += '</ol></li>';
			if(!bool){
				//分页
				pagingStr += '<a class="pagingSize hoverBtn pagingBtn firstPage" href="javascript:void(0);">首页<svg class="pageSvg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 74 60" enable-background="new 0 0 74 60" xml:space="preserve"><path fill="#666666" d="M40.6,26.1c-1.1,1.1-1.7,2.5-1.7,3.9c0,1.4,0.6,2.9,1.7,3.9c0,0,20.4,21.4,22.5,23.5c2.1,2,5.8,2.2,8.1,0c2.2-2.2,2.4-5.2,0-7.9L52.4,30l18.7-19.5c2.4-2.7,2.2-5.7,0-7.9c-2.2-2.2-6-2-8.1,0C61,4.6,40.6,26.1,40.6,26.1z M1.1,30c0,1.4,0.6,2.9,1.7,3.9c0,0,20.4,21.4,22.5,23.5c2.1,2,5.8,2.2,8.1,0c2.2-2.2,2.4-5.2,0-7.9L14.6,30l18.7-19.5c2.4-2.7,2.2-5.7,0-7.9c-2.2-2.2-6-2-8.1,0c-2.1,2-22.5,23.5-22.5,23.5C1.7,27.1,1.1,28.6,1.1,30z"/></svg></a>';
				pagingStr += '<a class="pagingSize hoverBtn pagingBtn prevPage" href="javascript:void(0);">上一页<svg class="pageSvg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 36 60" enable-background="new 0 0 36 60" xml:space="preserve"><path fill="#666666" d="M25.2,2.6c-2.1,2-22.5,23.5-22.5,23.5C1.6,27.1,1,28.6,1,30c0,1.4,0.6,2.9,1.7,3.9c0,0,20.4,21.4,22.5,23.5c2.1,2,5.8,2.2,8.1,0c2.2-2.2,2.4-5.2,0-7.9L14.5,30l18.7-19.5c2.4-2.7,2.2-5.7,0-7.9C31,0.4,27.3,0.5,25.2,2.6z"/></svg></a>';
				pagingStr += '<ol class="pagingSize pagingList" pagenum="'+pageNum+'">';
				for(var k=1; k<=pageNum && k<=7; k++){
					var num = k;
					if(k==6){
						num = pageNum > 7 ? "..." : 6; 
					}else if(k==7){
						num = pageNum;
					}
					pagingStr += '<li class="hoverBtn">'+num+'</li>';
				}
				pagingStr += '</ol><a class="pagingSize hoverBtn pagingBtn nextPage" href="javascript:void(0);">下一页<svg class="pageSvg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 34 58" enable-background="new 0 0 34 58" xml:space="preserve"><path fill="#666666" d="M10.2,54.8c2-1.9,21.3-22.2,21.3-22.2c1-0.9,1.6-2.4,1.6-3.7s-0.6-2.7-1.6-3.7c0,0-19.3-20.2-21.3-22.2c-2-1.9-5.5-2.1-7.7,0c-2.1,2.1-2.3,4.9,0,7.5L20.3,29L2.7,47.4c-2.3,2.5-2.1,5.4,0,7.5S8.2,56.8,10.2,54.8z"/></svg></a>';
				pagingStr += '<a class="pagingSize hoverBtn pagingBtn lastPage" href="javascript:void(0);">末页<svg class="pageSvg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 74 60" enable-background="new 0 0 74 60" xml:space="preserve"><path fill="#666666" d="M10.9,2.6c-2.1-2-5.8-2.2-8.1,0c-2.2,2.2-2.4,5.2,0,7.9L21.6,30L2.9,49.5c-2.4,2.7-2.2,5.7,0,7.9c2.2,2.2,6,2,8.1,0c2.1-2,22.5-23.5,22.5-23.5c1.1-1.1,1.7-2.5,1.7-3.9c0-1.4-0.6-2.9-1.7-3.9C33.4,26.1,13,4.6,10.9,2.6zM71.2,26.1c0,0-20.4-21.4-22.5-23.5c-2.1-2-5.8-2.2-8.1,0c-2.2,2.2-2.4,5.2,0,7.9L59.4,30L40.6,49.5c-2.4,2.7-2.2,5.7,0,7.9c2.2,2.2,6,2,8.1,0c2.1-2,22.5-23.5,22.5-23.5c1.1-1.1,1.7-2.5,1.7-3.9C72.9,28.6,72.3,27.1,71.2,26.1z"/></svg></a>';
			}
				
		}else{
			modityStr = '<p class="nomodityHint"><strong>该分类暂无商品信息！</strong></p>';
		}
		$(this).find(".commodityList").html(modityStr);
		!bool && $(this).find(".pagingWrap").html(pagingStr).find(".pagingList li:first-child").addClass("active");
		commodityList.updateboxHeight($(this));
	};
	//提取参数
	commodityList.getParam = function (objString,name) {
		if(!objString || !name) return "";
		var paramVal = "",
			paramObj = {};
        $.each(objString.split(";"),function (i,_) {
            if(!_) return true;
            var key = _.split(":");
            paramObj[key[0]] = key[1];
        });
        paramVal = paramObj[name] || "";
        return paramVal;
    };
    //更新图片容器宽度
    commodityList.updateboxHeight = function (dom) {
    	var scale = 3/4, 
    		width = dom.find(".commodityWrap .modityImg").width(),
    		height = width*scale;
    	dom.find(".commodityWrap .modityImg").height(height);
    };
    //根据分类id提取相应的数据
    commodityList.getCatetoryDate = function(dataArr,categoryIds){
    	var newArr = [];
    	if(categoryIds){
			categoryIds = categoryIds.split(",");
			$.map(dataArr,function(_i){
				for(var k=0; k<categoryIds.length; k++){
					if(_i.categoryId==categoryIds[k]){
						newArr.push(_i);
						break;
					}
				}	
			});
			return newArr;
		}else{
			return dataArr;
		}
    };
    //保存cookie
    commodityList.setCookie = function(key, value, expireDays){
        var date=new Date();
        expireDays = expireDays || 7;
        date.setTime(date.getTime()+expireDays*24*3600*1000);
        document.cookie = key + "=" + escape(value)+";expires="+date.toGMTString()+";path=/";
    }
    //获取cookie
    commodityList.getCookie = function(name){
        var strCookie=document.cookie,
            arrCookie=strCookie.split(";");

        for(var i=0;i<arrCookie.length;i++){
            var arr=arrCookie[i].split("=");
            arr[0] = arr[0].replace(/\s/,"");
            if(arr[0]==name) {
                return arr[1];
            }
        }
        return "";
    }
	commodityList.init();
});	
