/**
 * Created by user on 2016/10/19.
 */
$(function () {
    $("#wqd-about").nanoScroller({alwaysVisible: false});
    var wqdGoodsCar={};
    wqdGoodsCar.bindEvent= function () {
        var self=this;
        //购买支付功能后 出现列表
        $(document).on("click",".goods-pay .personal-car", function (e) {
            var $goodsPay=$(".goods-pay");
            if(!$goodsPay.hasClass("show")){
                $goodsPay.addClass("show");
                self.setAttr();
                self.totalAmount();
            }
            $(".detail-list>li").length?$(".null").removeClass("on"):$(".null").addClass("on");
            $("#wqd-about").nanoScroller({alwaysVisible: false});
        });
        //点击其他位置隐藏列表
        $(document).on("click", function (e) {
            if(!$(e.target).closest(".goods-pay").length){
                if($(".goods-pay").hasClass("show"))$(".goods-pay").removeClass("show");
            }
        });
        //增加||减少
        $(document).on("click",".goods-pay .num-add,.goods-pay .num-reduse", function (e) {
            var $parents=$(this).parents("li");
            var $editRadio=$parents.find(".edit-radio");
            var $num=$(this).hasClass("num-add")?$(this).prev():$(this).next();
            var val=parseInt($num.text(),10);
            var $price=parseFloat($parents.find(".unit-price").text());
            var flag=$(this).hasClass("num-add")?true:false;
            //发数据
            if(!flag&&$parents.find(".number").text()<=1)return;
            var data=self.setData($parents,this);
            $.ajax({
                url: "/shoppingcart/updateCart",
                type: "post",
                data: data,
                dataType: "json",
                success: function (json) {
                    if(json.status==200){
                        //成功之后数量计算 总金额计算
                        flag?self.numAdd($num,$editRadio,val,$price):self.numReduse($num,$editRadio,val,$price);
                        self.totalAmount();
                    }
                }
            });

        });
        //单项勾选
        $(document).on("click",".goods-pay .edit-radio", function (e) {
            $(this).toggleClass("active");
            var $radioAll=$(".goods-pay").find(".radio-all");
            if($(".goods-pay .edit-radio.active").length==$(".goods-pay .edit-radio").length){
                $radioAll.addClass("active");
            }else{
                $radioAll.removeClass("active");
            }
            self.totalAmount();
        });
        //全部勾选
        $(document).on("click",".goods-pay .item-all", function (e) {
            var $editRadio=$(".goods-pay").find(".edit-radio");
            var $child=$(this).find(".radio-all");
            $child.hasClass("active")?$editRadio.removeClass("active"):$editRadio.addClass("active");
            $child.toggleClass("active");
            self.totalAmount();
        });
        //点击删除
        $(document).on("click",".goods-pay em.delete", function (e) {
            e.stopPropagation();
            var $parents=$(this).parents("li");
            var data=self.setData($parents,this);
            data.count="0";
            $.ajax({
                url: "/shoppingcart/updateCart",
                type: "post",
                data: data,
                dataType: "json",
                success: function (json) {
                    if(json.status==200){
                        //成功之后 删除列表数据  并进行金额计算
                        $parents.remove();
                        self.totalAmount();
                        var $liList=$(".goods-pay .detail-list li");
                        $(".goods-pay").find(".num-btn").text($liList.length);
                        $(".goods-pay .personal-car strong").text($liList.length);
                        var $first=$(".goods-pay .detail-list li:eq(0)");
                        if(!$first.hasClass("list-first"))$first.addClass("list-first");
                        if($liList.length==0)$(".goods-pay").find(".personal-car strong").addClass("none").end().find(".null").addClass("on");
                    }
                }
            });
        });
        //结算
        $(document).on("click",".goods-pay .reckoning", function (e){
            e.stopPropagation();
            var data=self.setAllData();
            location.href="/customer/settlement/index.html?goodsInfo="+encodeURIComponent(JSON.stringify({goodsInfo:data}));

        })
    };

    //计算总金额
    wqdGoodsCar.totalAmount = function () {
        var totalAmount= 0,amount;
        var $active=$(".goods-pay .edit-radio.active");
        $active.each(function (i, _) {
            amount=parseFloat($(_).attr("price")||$(_).next().find(".unit-price").text());
            totalAmount+=amount;
        });
        $(".goods-pay").find(".all-price").text(totalAmount.toFixed(2)).end().find(".item-num").text($active.length);
        totalAmount==0?$(".goods-pay").find(".detail-bottom").addClass("clickable"):$(".goods-pay").find(".detail-bottom").removeClass("clickable");
    };
    //添加按钮方法
    wqdGoodsCar.numAdd= function ($num,$editRadio,val,$price) {
        $num.text(val+1);
        $editRadio.attr("price",(val+1)*$price);
    };
    //减少按钮方法
    wqdGoodsCar.numReduse= function  ($num,$editRadio,val,$price) {
        if(val<=1)return;
        $num.text(val-1);
        $editRadio.attr("price",(val-1)*$price);
    };
    //添加类名
    wqdGoodsCar.setAttr= function () {
        var $liList=$(".goods-pay .detail-list li");
        $liList && $liList.each(function (i, _) {
            var curPrice=parseInt($(this).find(".number").text(),10)*$(this).find(".unit-price").text();
            $(this).find(".edit-radio").attr("price",curPrice)
        })
    };
    //数据流
    wqdGoodsCar.setData= function ($this,that) {
        var modSize=[],data;
        $this.find(".detail-describe span").each(function (i, _) {
            modSize.push($(this).text());
        });
        var Item = {
            id : $this.attr("id"),
            name : $this.find(".detail-title").text(),
            price : $this.find(".unit-price").text(),
            picPath : $this.find("dt img").attr("src") || "",
            itemLink : location.href,
            count : $this.find(".number").text(),
            specificationValue : modSize.join("_"),
            specificationId:$this.find(".detail-describe").attr("sizeid")

        };
        var flag=$(that).hasClass("delete")?true:false;
        var method=flag?"delete":"add";
        var count=$(that).hasClass("num-add")?"1":"-1";
        return data=flag?{ cartItem: JSON.stringify(Item), method: method} : { cartItem: JSON.stringify(Item), method: method, count: count};
    };
    //结算数据流
    wqdGoodsCar.setAllData= function () {
        var $liList=$(".edit-radio.active").parents("li"),arr=[];
        $liList.each(function (i, _) {
            var modSize=[];
            $(_).find(".detail-describe span").each(function (i, _) {
                modSize.push($(this).text());
            });
            var Item = {
                goodsId : $(_).attr("id"),
                specificationId : $(_).find(".detail-describe").attr("sizeid"),
                count : $(_).find(".number").text(),
                itemLink : $(_).find(".detail-title a").attr("href"),
                buySource:"2"
            };
            arr.push(Item);
        });
        return arr;
    };


    wqdGoodsCar.bindEvent();
});