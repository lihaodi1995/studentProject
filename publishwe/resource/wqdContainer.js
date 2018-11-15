$(function() {
	var container = {};
	container.init = function(){
		$("#HTMLDATA").length ? this.insideEvent() : this.outsideEvent();
	};
	//编辑器内的事件绑定
	container.insideEvent = function(){
		//模式一：拖动容器一同时改变容器二
		$(document).on("element.change",".groupContainerOne, .groupContainerTwo",function(e){
			var	that = $(this),
				thisMark = that.attr("wqdmark") || "wqdNomark",
				menuObj = that.siblings(".wqdelementEdit"+"[wqdmark="+thisMark+"]"),
				cssObj = {};
			cssObj.left = that.position().left;
			cssObj.top = that.position().top;
			cssObj.height = that.height();
			cssObj.width = that.width();
			menuObj.css(cssObj);
		});
		//模式二：容器一点击效果
		$(document).on("click.wqdContainer",".freeContainerOne",function(){
			//手风琴样式在这里先禁止掉
			if($(this).hasClass("accordion_one"))return;
			var that = $(this),
				thisMark = that.attr("wqdmark") || "wqdNomark",
				groupmark = that.attr("groupmark") || "",
				menuObj = that.siblings(".wqdelementEdit"+"[wqdmark="+thisMark+"]");
			if(menuObj.is(":visible")){
				that.find(".containerWarp").children(".wqdelementEdit").find(".wqdelementEditBox").removeClass("active");
				menuObj.hide();
			}else{
				that.find(".containerWarp").children(".wqdelementEdit").find(".wqdelementEditBox").addClass("active");
				if(groupmark){
					that.siblings(".wqdelementEdit"+"[groupmark="+groupmark+"]").each(function(){
						$(this).find(".containerWarp").children(".wqdelementEdit").find(".wqdelementEditBox").removeClass("active");
						var otherMark = $(this).attr("wqdmark") || "wqdNomark";
						$(this).siblings(".wqdelementEdit"+"[wqdmark="+otherMark+"]").hide();
					});
				}
				menuObj.show();
			}
			$(document).trigger("appSetCatch");
		});
		//删除容器
		$(document).on("element.remove",".groupContainerOne, .groupContainerTwo, .freeContainerOne, .freeContainerTwo",function(e){
			if(!$(e.target).find(".containerWarp").length) return;
			var	that = $(this),
				thisMark = that.attr("wqdmark") || "wqdNomark",
				menuObj = that.siblings(".wqdelementEdit"+"[wqdmark="+thisMark+"]"),
				elemId = menuObj.attr("id") || "";
			that.find(".containerWarp").children(".wqdelementEdit").each(function(){
				var childId = $(this).attr("id") || "";
				childId && $("style."+childId).remove();
			});
			menuObj.find(".containerWarp").children(".wqdelementEdit").each(function(){
				var childId = $(this).attr("id") || "";
				childId && $("style."+childId).remove();
			});
			elemId && $("style."+elemId).remove();
			menuObj.remove();	
		});
		//添加一组关联容器
		$(document).on("addFreeContainer",".freeContainerOne, .groupContainerOne, .groupContainerTwo",function(){
			!$(this).attr("groupmark") && $(this).hasClass("freeContainerOne") && $(this).attr("groupmark","groupmark" + new Date().getTime());
			var	that = $(this),
				thisMark = that.attr("wqdmark") || "wqdNomark",
				menuObj = that.siblings(".wqdelementEdit"+"[wqdmark="+thisMark+"]"),
				thatClone = container.cloneElement(that,that.clone()),
				menuobjClone = container.cloneElement(that,menuObj.clone(),"s"),
				newMark = "mark" + new Date().getTime();
			thatClone.find(".containerWarp").children(".wqdelementEdit").each(function(i){container.cloneElement(that,$(this),i+1);});
			menuobjClone.find(".containerWarp").children(".wqdelementEdit").each(function(i){container.cloneElement(that,$(this),i+1001);});
			thatClone.attr("wqdmark",newMark).css({"left":that.position().left+10,"top":that.position().top+10}).appendTo(that.parents(".sectionV2"));
			if(!that.hasClass("freeContainerOne")) menuobjClone.css({"left":that.position().left+10,"top":that.position().top+10});
			else menuobjClone.hide();
			menuobjClone.attr("wqdmark",newMark).appendTo(that.parents(".sectionV2"));
			$(document).trigger("appSetCatch");
		});
	};
	//发布后的事件绑定
	container.outsideEvent = function(){
		//模式一：触发二级容器
		$(".groupContainerOne").each(function(){
			var wqdtarget = $(this).attr("wqdtarget") || "click";
			$(this).on(wqdtarget,function(e){
				if($(this).attr("isanimahide")|| $(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formInput"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formButton"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formTextarea") return;
				thisMark = $(this).attr("wqdmark") || "wqdNomark",
				menuObj = $(this).siblings(".wqdelementEdit"+"[wqdmark="+thisMark+"]");
				menuObj.show();
				// if(menuObj.attr("wqdfadein")){
				// 	menuObj.attr("isanimashow","true");
				// 	setTimeout(function(){menuObj.removeAttr("isanimashow");},500);
				// }
			});
		});
		//模式一：隐藏二级容器
		$(".groupContainerTwo").each(function(){
			var wqdtarget = $(this).attr("wqdtargethide") || "click";
			if(wqdtarget == "click"){
				$(this).on("click",function(e){
					if($(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formInput"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formButton"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formTextarea"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formSelect"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formSelect"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formCheckbox"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formRadio"){return}
					container.containerHide($(this));
				});
			}else if(wqdtarget == "mouse"){
				$(this).on("mouseleave",function(){
					if(!$(this).is(":visible")) return;
					container.containerHide($(this));
				});
			}else if(wqdtarget == "clickOther"){
				var that = $(this);
				$(document).on("click touchstart",function(event){
					if($(event.target).closest(".groupContainerOne").attr("wqdmark") != that.attr("wqdmark") && $(event.target).closest(".groupContainerTwo").attr("wqdmark") != that.attr("wqdmark")){
						container.containerHide(that);
					}
				});
			}
		});
		//模式二：触发二级容器
		$(".freeContainerOne").not(".tabContainer").each(function(){
			var wqdtarget = $(this).attr("wqdtarget") || "click";
			$(this).on(wqdtarget,function(){
				var thisMark = $(this).attr("wqdmark") || "wqdNomark",
					groupmark = $(this).attr("groupmark") || "",
					wqdfadein = $(this).attr("wqdfadein") || "",
					menuObj = $(this).siblings(".wqdelementEdit"+"[wqdmark="+thisMark+"]");
				if(menuObj.is(":visible")) return;
				//手风琴样式在这里先禁止掉
				if($(this).hasClass("accordion_one"))return;
				$(this).find(".containerWarp").children(".wqdelementEdit").find(".wqdelementEditBox").addClass("active");
				if(groupmark){
					$(this).siblings(".wqdelementEdit"+"[groupmark="+groupmark+"]").each(function(){
						$(this).find(".containerWarp").children(".wqdelementEdit").find(".wqdelementEditBox").removeClass("active");
						var otherMark = $(this).attr("wqdmark") || "wqdNomark";
						$(this).siblings(".wqdelementEdit"+"[wqdmark="+otherMark+"]").removeAttr("wqdfadein").hide();
					});
				}
				menuObj.show().attr("wqdfadein",wqdfadein);
			});
		});

		//模式三 :触发二级容器
		$(".tabContainer").each(function (i, _) {
			var thisMark = $(this).attr("wqdmark") || "wqdNomark",
				menuObj = $(this).siblings(".wqdelementEdit"+"[wqdmark="+thisMark+"]"),//得到mark
				wqdtarget = $(this).attr("wqdtarget") || "click",//得到一级触发方式
				wqdfadein = $(this).attr("wqdfadein") || "",//得到一级触发方动画
				wqdelementhide=menuObj.attr("wqdelementhide")||"",//得到二级隐藏触发源
				wqdtargethide=menuObj.attr("wqdtargethide")||"click",//得到二级隐藏方式
				wqdfadeout=menuObj.attr("wqdfadeout")||"",//得到二级隐藏动画
				flag;

			var that=$(this);
			if(wqdelementhide=="tabcontainer"){//由一级触发隐藏动画  几种情况

				if(wqdtarget=="click" && wqdtargethide=="click"){//由一级点击 出现隐藏
					$(this).off("click.tab").on("click.tab", function (e) {
						if ($(this).hasClass("accordion_one"))return;//手风琴样式在这里先禁止掉
						if(menuObj.is(":visible")){
							if(menuObj.attr("isanimahide"))return ;
							if($(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formInput"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formButton"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formTextarea"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formSelect"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formSelect"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formCheckbox"||$(e.target).closest(".wqdelementEdit").attr("data-elementtype")=="formRadio"){return}
							container.tabHide(this,menuObj,wqdfadeout);
						}else{
							if( menuObj.attr("isanimahide"))return ;
							container.tabShow(this,menuObj,wqdfadein);
						}
					});
				}else if(wqdtarget=="mouseenter" && wqdtargethide=="mouse"){//由一级滑动 出现隐藏
					flag=menuObj.is(":hidden")?true:false;
					$(this).off("mouseenter").on("mouseenter", function () {
						if(container.breakEnter(flag,menuObj))return ;

						flag?container.tabShow(this,menuObj,wqdfadein):container.tabHide(this,menuObj,wqdfadeout);
					}).off("mouseleave").on("mouseleave", function () {
						if(container.breakLeave(flag,menuObj))return ;
						flag?container.tabHide(this,menuObj,wqdfadeout):container.tabShow(this,menuObj,wqdfadein);
					});
				}else if(wqdtarget=="click" && wqdtargethide=="mouse"){//由一级点击出现 滑动隐藏
					flag=menuObj.is(":hidden")?true:false;
					$(this).off("click").on("click", function (e) {
						if(container.breakEnter(flag,menuObj))return ;
						flag?container.tabShow(this,menuObj,wqdfadein):container.tabHide(this,menuObj,wqdfadeout);
					}).off("mouseleave").on("mouseleave", function () {
						if(container.breakLeave(flag,menuObj))return ;
						flag?container.tabHide(this,menuObj,wqdfadeout):container.tabShow(this,menuObj,wqdfadein);
					});

				}else if(wqdtarget=="mouseenter" && wqdtargethide=="click"){//由一级滑动出现 点击隐藏
					flag=menuObj.is(":hidden")?true:false;
					$(this).off("mouseenter").on("mouseenter", function (e) {
						if(container.breakEnter(flag,menuObj))return ;
						flag?container.tabShow(this,menuObj,wqdfadein):container.tabHide(this,menuObj,wqdfadeout);
					}).off("click").on("click", function () {
						if(container.breakLeave(flag,menuObj))return ;
						flag?container.tabHide(this,menuObj,wqdfadeout):container.tabShow(this,menuObj,wqdfadein);
					});

				}
			}
			if(wqdelementhide!="tabcontainer"){
				$(this).off(wqdtarget).on(wqdtarget,function(){//触发动画一定是由一级触发
					if(menuObj.is(":visible")|| menuObj.attr("isanimahide"))return;
					container.tabShow(this,menuObj,wqdfadein);
				});
				if(wqdelementhide=="subtabcontainer" && wqdtargethide=="click"){ //隐藏动画由二级触发--点击
					menuObj.off("click").on("click", function () {
						if(menuObj.attr("isanimahide"))return ;
						container.tabHide(that,menuObj,wqdfadeout)
					});
				}
				if(wqdelementhide=="subtabcontainer" && wqdtargethide=="mouse"){
					menuObj.off("mouseleave").on("mouseleave", function () { //隐藏动画由二级触发--滑出
						if(menuObj.attr("isanimahide"))return ;
						container.tabHide(that,menuObj,wqdfadeout)
					});
				}
				if(wqdelementhide=="elementOther" && wqdtargethide=="click"){ //隐藏动画由其他元素触发--点击
					$(document).on("click touchstart",function(event){
						if(menuObj.attr("isanimahide"))return ;
						if($(event.target).closest(".tabContainer").attr("wqdmark") != thisMark && $(event.target).closest(".subTabContainer").attr("wqdmark") != thisMark){
							container.tabHide(that,menuObj,wqdfadeout)
						}
					});
				}
			}

		})

	};
	//复制
	container.cloneElement = function(obj,elem,val){
		var elementId = elem.attr("id") || "",
			val = val || "",
			newelementId = "elementId" + (new Date().getTime() + val),
			reg = new RegExp(""+elementId,"g");
		elementId && $("style."+elementId).length && $("style."+elementId).clone().removeClass(elementId).addClass(newelementId).html($("style."+elementId).html().replace(reg,newelementId)).prependTo(obj.parents(".wqdSectiondiv"));
		elem.attr("id",newelementId).attr("elementid",newelementId);
		return elem;
	};
	//发布后模式一：二级容器隐藏
	container.containerHide = function(obj){
		var wqdfadeout = obj.attr("wqdfadeout") || "";
		if(wqdfadeout){
			obj.addClass(wqdfadeout).attr("isanimahide","true");
			setTimeout(function(){
				obj.removeClass(wqdfadeout).removeAttr("isanimahide").hide();
			},500);
		}else{
			obj.hide();
		}
	};

	//出现动画
	container.tabShow= function (that,menuObj,wqdfadein) {
		if($(that).hasClass("accordion_one"))return;
		$(that).find(".containerWarp").children(".wqdelementEdit").find(".wqdelementEditBox").addClass("active");
		if(wqdfadein){


			var wqdfadeout=menuObj.attr("wqdfadeout")||"";//得到二级隐藏动画

			var wqdelementhide=menuObj.attr("wqdelementhide")||"";//得到二级隐藏触发源

			var wqdtargethide=menuObj.attr("wqdtargethide")||"click";//得到二级隐藏方式

			if(wqdtargethide=="mouse")wqdtargethide="mouseleave";

			if(wqdelementhide=="subtabcontainer")menuObj.off(wqdtargethide);
			menuObj.css("display","block").attr("wqdfadein",wqdfadein);

			setTimeout(function(){
				menuObj.removeAttr("wqdfadein");

				if(wqdelementhide=="subtabcontainer"){
					setTimeout(function () {
						menuObj.on(wqdtargethide, function () {
							if(menuObj.attr("isanimahide"))return ;
							container.tabHide(that,menuObj,wqdfadeout)
						})
					},100)
				}

			},500);
		}else{
			menuObj.css("display","block");
		}
	};
	//隐藏动画
	container.tabHide= function (that,menuObj) {
		if($(that).hasClass("accordion_one"))return;
		$(that).find(".containerWarp").children(".wqdelementEdit").find(".wqdelementEditBox").removeClass("active");
		container.containerHide(menuObj);
	};
	//判断是否中断 出现动画
	container.breakEnter= function (flag,menuObj) {
		return flag ? menuObj.is(":visible") || menuObj.attr("isanimahide") : menuObj.is(":hidden") && menuObj.attr("wqdfadein");
	};
	//判断是否中断 隐藏动画
	container.breakLeave= function (flag,menuObj) {
		return flag ? menuObj.is(":hidden")|| menuObj.attr("wqdfadein") : menuObj.is(":visible")|| menuObj.attr("isanimahide");
	};

	//阻止日历元素的冒泡
	$(".elementsContainer").on("click","[data-elementtype='formDate']",function(e){
		e.stopPropagation();
	});
	container.init();
});

