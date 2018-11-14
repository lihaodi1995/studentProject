/**
 * 
 */

$(function(){
	
	var url = {
	        tmapp: "/mooc/tc-getG",
	        tminfo: "/mooc/tc-getAcc",
	        tmdel:"/mooc/tc-delG",
	       tmmanage:"/mooc/tc-manageG"
	    };
	   

	    

	$('.tm-app').on('click', '.app-pass', function () {
        var _this = this;
        var newbutton = '<a class="waves-effect waves-light btn tm-edit">调整团队</a> <a class="waves-effect waves-light btn red tm-del">解散团队</a>';

        var li = $(_this).parent().parent();
        var div = $(_this).parent();
        $(div).append(newbutton);

        var divbro = $(div).prev();
        var divspan = $(divbro).children('.badge')

        $(divspan).remove();
        $(divbro).append('<span class="badge cyan new" data-badge-caption="已审核"></span>');

        $('.show-tm').append(li);
        $(_this).next().remove();
        $(_this).remove();

        var teamname = $($(li).find('.collapsible-header')).find('.tm-name').text();
        var params = {
            name: teamname,
            status: 1
        };

        $.post(url.tmmanage, params, function () {
            console.log('accepted');
        });
    });

    $('.tm-app').on('click', '.app-reject', function () {
        var _this = this;
        var li = $(_this).parent().parent();
        $(li).css('display', 'none');

        var teamname = $(li).find('.tm-name').text();
        var params = {
            name: teamname,
            status: 0
        };

        $.post(url.tmmanage, params, function () {
            console.log('rejected');
        });
    });


	    /*$('.tm-del').on('click', function () {
	        var _this = this;
	        var li = $(_this).parent().parent();
	        $(li).css('display', 'none');

	        var teamname=$(li).find('tm-name').html();

	        var params={
	            name:teamname
	        };

	        $.post(url.tmdel,params,function () {
	            console.log('deleted');
	        });
	        $.ajax({
            	type:"POST",
            	url:url.tmdel,
            	data:params,
            	trditional:true,
            	success:function(){
            		Materialize.toast('删除成功', 4000);
                    $(grade).html(gradeNum);
            	},
            	error:function(){
            		Materialize.toast('删除失败', 4000);
                  
            	}
            })
	    });*/

	    $('.show-tm').on('click', '.tm-del', function () {
	        var _this = this;
	        var li = $($(_this).parent()).parent();
	        $(li).css('display', 'none');
	        var teamname=$(li).find('.tm-name').html();

	        var params={
	            name:teamname
	        };
	        $.ajax({
            	type:"POST",
            	url:url.tmdel,
            	data:params,
            	trditional:true,
            	success:function(){
            		Materialize.toast('删除成功', 4000);
                    $(grade).html(gradeNum);
            	},
            	error:function(){
            		Materialize.toast('删除失败', 4000);
                  
            	}
            })
	    });
	    $('.collapsible-body').on('click', '.tm-del', function () {
	        var _this = this;
	        var li = $(_this).parent().parent();
	        $(li).css('display', 'none');
	    });

	    $('.tm-edit').click(function () {
	        //TODO
	    });

	    function loadtm() {
	        //ajax here

	        //gettminfo();
	        //gettmapp();
	        $.get(url.tmapp, function (json) {
	            var tmapp = eval('(' + json + ')');
	            //tmapp = json;


	            var appcount = tmapp.count;


	            for (var i = 0; i < appcount; i++) {
	                var model1 = $('.model-app').clone();
	                
	                $(model1).find('.tm-name').html(tmapp.team[i].name);
	                $(model1).find('.tm-leader').html("组长："+tmapp.team[i].leader);
	                $(model1).find('.tm-member').html("男生："+tmapp.team[i].member);
	                $(model1).find('.tm-gmember').html("女生："+tmapp.team[i].gmember);
	                //alert("1");
	                $('.tm-app').append(model1);

	                model1.removeClass('model-app');

	            }

	            $('.model-app').remove();
	        });
	     

	    }

	    function loadAcc(){
	    	$.get(url.tminfo, function (json1) {
	             var tminfo = eval('(' + json1 + ')');
	            //tminfo = json;

	            var infocount = tminfo.count;
	            for (var j = 0; j < infocount; j++) {
	                var model2 = $('.model-info').clone();

	                $(model2).find('.tm-name').html(tminfo.team[j].name);
	                $(model2).find('.tm-leader').html("组长："+tminfo.team[j].leader);
	                $(model2).find('.tm-member').html("男生："+tminfo.team[j].member);
	                $(model2).find('.tm-gmember').html("女生："+tminfo.team[j].gmember);

	                $('.show-tm').append(model2);
	                model2.removeClass('model-info');

	            }
	            $('.model-info').remove();
	        })
	    }

	    loadtm();
	    loadAcc();

})
   