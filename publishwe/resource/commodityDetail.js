$(function() {
	var modityDetail = {
		init : function(){
			this.bindEvent();

			var _height = $(".modBannerimg").width()*3/4, li_height = $(".modBannercheck li:first-child").width()*4/5;
			$(".modBannerimg").css("height",_height);
			$(".modBannercheck li").css("height",li_height);

			//分享链接
			$(".modityDetails").find(".modShareIcon").attr({

				"data-url" : location.href,
				"data-pic" : $(".modityDetails").find(".modBannerimg img").attr("src"),
				"data-summary" : "我发现了一款不错的商品，快点击查看吧~"
			});
			//是否已赞
			var modityId = $(".modityDetails").attr("data-moddetailid") || "!!!",
				modityCookie = this.getCookie(modityId);
			modityCookie && $(".modityDetails .modAdmire").addClass("active");

			//是否可购买
			var nowPrice = $(".modDetlnowPrice .modnowPrice span span").text(),
				inventory = $(".modDetlInventory .modInventory span").text();

			(!nowPrice || !inventory || /[^\d\.]/.test(nowPrice) || inventory == "0") && $(".purchaseBtn, .shoppingCartBtn").addClass("disabled");
			(!inventory || inventory == "0") && $(".modityDetails .modityControl input").val(0);

		},
		bindEvent : function(){

			$(document).on("click",".modBannercheck li",function(){
				if($(this).hasClass("active")) return;

				var src = $(this).find("img").attr("src");
				$(this).parents(".modCarousel").siblings(".modBannerimg").find("img").attr("src",src);
				$(this).addClass("active").siblings().removeClass("active");
			});

			//选择规格
			$(document).on("click",".modSizeItem li",modityDetail.selectSize);

			//点赞
			$(document).on("click",".modityDetails .modAdmire svg",modityDetail.praise);
			
			//加入购物车、购买
			$(".modityDetails .shoppingCartBtn, .modityDetails .purchaseBtn").on("click",function(){
				if($(this).hasClass("disabled")) return;

				var modSize = [], modId = [], num = $(".modityDetails .modityControl input").val();

				if(!$(".wqd-buyCar").hasClass("goods-pay") && !$(".wqd-buyCar").hasClass("goods-members")){
					$(document).trigger("login.commodityDetail");
					return;
				}
					
				if(num == "0"){

					$(".modityDetails .modDetlWarning").show().find(".warningText").text("购买数量不能为零！");
					return;
				}
				if($(".modSizeItem li.active").length != $(".modSizeList > li").length){

					$(".modityDetails .modDetlWarning").show().find(".warningText").text("请选择商品规格！");
					return;
				}
				
				$(".modSizeItem li.active").each(function(){
					modSize.push($(this).text());
					modId.push($(this).attr("sizeid"));

				});

				var Item = {
					id : $(".modityDetails").attr("data-moddetailid") || "",
					name : $(".modDetlTitle h1").text(),
					price : $(".modnowPrice span span").text(),
					picPath : $(".modBannerimg img").attr("src") || "",
					itemLink : location.href,
					count : num,
					specificationValue : modSize.join("_"),
					specificationId:modId.join("_")
				};
				
				//触发加入购物车事件
				if($(this).hasClass("shoppingCartBtn")){

					$(this).trigger("addShoppingCart",{cartItem:JSON.stringify(Item), method:"add"});
				}else{
					var parame = [],
						modObj  = {
							buySource : "1",
							goodsId : Item.id,
							specificationId : Item.specificationId,
							count : String(num),
							itemLink : location.href
							//price : String(Item.price * num)
						};
					parame[0] = modObj;
					location.href = "/customer/settlement/index.html?goodsInfo="+encodeURIComponent(JSON.stringify({goodsInfo:parame}));
				}
			});

			//输入购买数量
			$(".modityDetails .modityControl input").on("input",function(){

				this.value = this.value.replace(/\D/g, '');

			}).on("blur",function(){

				var val = parseInt(this.value || 0),
					inventory = parseInt($(".modDetlInventory .modInventory span").text() || 0);
				val = val > inventory ? inventory : val;
				this.value = val;

			});
			// + -
			$(".modityDetails .modityControl .controlBtn").on("click",function(){

				$(".modityDetails .modDetlWarning").hide()

				var val = parseInt($(this).siblings("input").val()),
					inventory = parseInt($(".modDetlInventory .modInventory span").text() || 0);

				if($(this).hasClass("reduce")) val = val < 1 ? 0 : --val;

				else val = val >= inventory ? inventory : ++val;

				$(this).siblings("input").val(val);
			});

		},
		//选择规格
		selectSize : function(){
			var that = $(this),
				USERID = location.search.indexOf("=") < 0 ? "" : location.search.substring(location.search.indexOf("=")+1);

			if(that.hasClass("active")) return;
			//$(".modSizeItem li").removeClass("modStockout");

			that.addClass("active").siblings().removeClass("active");
			if($(".modSizeList > li").length == $(".modSizeItem li.active").length){
				var idArr = [] , modId = that.parents(".modityDetails").attr("data-moddetailid") || "";
				$(".modSizeItem li.active").each(function(){
					idArr.push($(this).attr("sizeid"));
				});

				idArr = idArr.join("_") + "&";

				$.ajax({
		            type: "post",
		            url: "/fixed/itemSpecPrice/"+modId,
		            data : {userId:USERID, specValue:idArr},
		            dataType: "json",
		            success:function(data){
		            	if(data.status == 200){

		            		//data.data.stock==0 && that.addClass("modStockout");
		            		if(data.data.price && !/[^\d\.]/.test(data.data.price) && data.data.stock!="" && data.data.stock!="0"){
		            			$(".purchaseBtn, .shoppingCartBtn").removeClass("disabled");
		            		} else{
		            			$(".purchaseBtn, .shoppingCartBtn").addClass("disabled");
		            		}
		            		
		            		$(".modityDetails .modnowPrice span span").text(data.data.price);
		            		$(".modityDetails .modInventory span").text(data.data.stock=="" ? "0" : data.data.stock);
		            		$(".modityDetails .modityControl input").val(data.data.stock && data.data.stock!="0" ? 1 : 0);
		            		$(".modityDetails .modDetlWarning").hide();

		            	}else{
		            		alert(data.msg);
		            	}
		            }
		        });
			}
		},
		//点赞
		praise : function(){
			if($(this).parent().hasClass("active")) return;

			var that = $(this),
				count = that.siblings("span").text() - 0,
				modityId = that.parents(".modityDetails").attr("data-moddetailid") || "";

			if(count >= 9999999){
				that.parent().addClass("active");
	            modityDetail.setCookie(modityId,"admire");
	            return;
			}

			$.ajax({
	            type: "post",
	            url: "/fixed/item/review",
	            data : {modityId:modityId},
	            dataType: "json",
	            success:function(data){
	            	if(data.status == 200){

	            		that.parent().addClass("active").end().siblings("span").text(that.siblings("span").text()-0+1);
	            		modityDetail.setCookie(modityId,"admire");

	            	}else{
	            		alert(data.msg)
	            	}
	            }
	        });
		},
    	setCookie : function(key, value, expireDays){

	        var date=new Date();
	        expireDays = expireDays || 7;
	        date.setTime(date.getTime()+expireDays*24*3600*1000);
	        document.cookie = key + "=" + escape(value)+";expires="+date.toGMTString()+";path=/";

	    },
    	getCookie : function(name){

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
	};

	modityDetail.init();
});	
