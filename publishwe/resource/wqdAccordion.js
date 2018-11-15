/**
 * Created by user on 2016/7/25.
 */
(function ($) {
    var accordion = {};
    accordion.init = function(){
        if(!$(".wqd-accordion").length)return;
        this.bindEvent();
    };
    accordion.bindEvent= function (e) {


        $(document).find(".wqd-accordion").each(function (i, _) {
            var _model = parseFloat($(this).attr("wqd-model"));
            var _effect = parseFloat($(this).attr("wqd-effect"));
            var _trigger = parseFloat($(this).attr("wqd-trigger"));
            var unwind = $(this).attr("wqd-fadein");
            var method= function (_this) {
                var $accordionTwo = $(_this).next(".accordion_two");
                var $allAccordionOne=$(_this).parents(".wqd-relate").siblings(".wqd-relate").find(".accordion_one .accordionOne");
                var $allAccordionTwo=$(_this).parents(".wqd-relate").siblings(".wqd-relate").find(".accordion_two");
                if(_model){
                    $(_this).find(".accordionOne").addClass("active");
                    //排列式
                    if(_model==1){
                        if ($accordionTwo.is(":hidden")) {
                            if(unwind==""){
                                $accordionTwo.slideDown(300);
                                return;
                            }
                            //$accordionTwo.css("display", "block").addClass(unwind);
                            $accordionTwo.slideDown(300 ).addClass(unwind);
                        }else{
                            $accordionTwo.slideUp(300);
                            $(_this).find(".accordionOne").removeClass("active");
                        }
                        //切换式
                    }else{
                        if($accordionTwo.is(":visible"))return;
                        if ($accordionTwo.is(":hidden")) {
                            $allAccordionTwo.slideUp(300);
                            $allAccordionOne.removeClass("active");
                            $(_this).find(".accordionOne").addClass("active");
                            if(unwind==""){
                                $accordionTwo.slideDown(300);
                                return;
                            }
                            //$accordionTwo.css("display", "block").addClass(unwind);
                            $accordionTwo.slideDown(300 ).addClass(unwind);
                        }
                    }
                    return
                }
                if(_effect){
                    if($accordionTwo.is(":visible"))return;
                    if ($accordionTwo.is(":hidden")) {
                        $allAccordionTwo.css("display", "none");
                        $allAccordionOne.removeClass("active");
                        $(_this).find(".accordionOne").addClass("active");
                        if(unwind==""){
                            $accordionTwo.css("display", "block");
                            return;
                        }
                        $accordionTwo.css("display", "block").addClass(unwind);
                    }
                }
            };

            //点进容器
            if(_trigger==5){
                $(this).off("click.accordion").on("click.accordion", ".accordion_one", function (e) {
                    //e.stopPropagation();
                    method(this)
                });
                return;
            }else{
                $(this).off("mouseenter.accordion").on("mouseenter.accordion",".accordion_one",function (e) {
                    e.stopPropagation();
                    method(this)
                })

            }
        });















    };
    accordion.init();


})($);