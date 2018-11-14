var pigai, group, file;

$("#down").click(function(){
	//alert('a');
	var flag = document.getElementsByClassName("flag").length;
	//var count = 0;
	var files = "";
	
	$(".flag").each(function(i){
		var x = i + 1;
		var name = "hw" + x;
		//alert("c");
		if($("[id='"+name+"']").is(':checked'))
		{
			var parent = $(this).parent().parent().parent().next().next();

			files += parent.html() + ",";
			//var parent = $(this).parent().parent().parent().parent().next().next().children();
			//alert("b");
//			var parent = $(this).parent().parent().parent().parent().next();
//			while(parent.next().length != 0) {
//				//alert(parent.hasClass("src"));
//				if(parent.hasClass("file")) {
//					files += x + ",";
//					//files += x + "/" + parent.children().html() + ",";
//					alert(parent.children().html());
//					
//				}
//				parent = parent.next();
//			}
			//files += x + ",";
			//files += x + "/" + parent.children().html() + ",";
			//alert(parent.html());
		}
		//alert(files);
	});	
	
	var f = {'files':files};
	$.get('downloadHomeworkRequest',f, function (content) {
		
		//alert(content);
		//alert(课程大纲修改成功)
		//$(".bigass").html(fix);
		var href = "/mooc/downloadHomework";
        var $iframe = $('#iframeForExport');
        if ($iframe.length == 0) {
            $iframe = $('<iframe id="iframeForExport" style="display:none;" />');
            $('body').append($iframe);
        }
        $iframe.attr('src', href);
    })

});

$(".publish").click(function(){
	
	var countli = document.getElementsByTagName("li").length - 10;
	//alert(countli);
	var num = "hw" + countli;
	//alert("不能吃东西");
	if($("#hwheadline").val() == "")
	{
		alert("标题为空！");
		$("#hwheadline").focus();
		return false;
	}
	if($("#hwbili").val() == "")
	{
		alert("比例为空！");
		$("#hwbili").focus();
		return false;
	}
	if($("#hwcontent").val() == "")
	{
		alert("内容为空！");
		$("#hwcontent").focus();
		return false;
	}
	
    var header=$('#hwheadline').val();
    var content=$('#hwcontent').val();
    
    var headerhtml='<li> <div class="collapsible-header"> <div class="col s1 m1 selectDown"> <form> <p> <input type="checkbox" name="checkbox" class="filled-in" id="'
    + num +'"> <label for="'+ num +'"></label> </p> </form> </div> <i class="material-icons">filter_drama</i>';
    var middlehtml1='<i class="material-icons text-black right">play_for_work</i> </div> <div class="collapsible-body"> <span>';
    var middlehtml2='</span></div><div class="collapsible-body file"><span>';
    var footerhtml='</span> </div> </li>';

   

	$(".newhw").submit();	
	 $('.show-hw').append(headerhtml + header + middlehtml1 + content + middlehtml2 + footerhtml);
	 alert("发布成功！");
});

$(".confirm").click(function(){

	//alert("");
	if($("#hwgrade").val() == "") {
		alert("评分为空！");
		$("#hwgrade").focus();
		return false;
	}
	$(".grade").submit();

});

$(".deletehw").click(function(){
	//alert("sad");
	var files = "";
	$(".flag").each(function(i){
		var x = i + 1;
		var name = "hw" + x;
		//alert(x);
		if($("[id='"+name+"']").is(':checked'))
		{
			
			
			
			var parent = $(this).parent().parent().parent().next().next();
			
			files += parent.html() + ",";
			//files += x + "/" + parent.children().html() + ",";
			//alert(files);
			parent.parent().parent().remove();

		}
	});
	$.ajax({
		
		type:'POST',
		
		data: files,
		
		contentType: "application/json; charset=utf-8", 
		dataType:'text',
		
		url :'/mooc/deleteHW',
			
		success :function(data) {
			
			//alert("OK");
		
		}		
	});
	alert("删除成功！");
});

$(".score").click(function(){

	var aa = $(this).parent().parent().prev().prev();
	while(!(aa.hasClass("hwtitle")))	
		aa = aa.prev();
	
	var parent =aa.children().next().next();
	
	pigai = parent.html();
	group = $(this).parent().prev().html();
	group = group.split("：")[1];
	file = $(this).parent().prev().prev().html();
//	alert(pigai);
	//alert(group);
//	alert(file);

});

$(".confirm").click(function(){

	//alert("");
	if($("#hwgrade").val() == "") {
		alert("评分为空！");
		$("#hwgrade").focus();
		return false;
	}
	if($("#hwcomment").val() == "") {
		alert("评论为空！");
		$("#hwcomment").focus();
		return false;
	}
	
	var dafen = {'group': group, 'title': pigai, 'file': file, 'grade': $("#hwgrade").val(), 'comment': $("#hwcomment").val()};
	//var course = {'name': name, 'info': info, 'teacher': teacher, 'place': place, 'score': score, 'people': people, 'start': start, 'end': end};
	
	$.ajax({
	
		type:'POST',
		
		data:JSON.stringify(dafen),
		
		contentType: "application/json; charset=utf-8", 
		dataType:'json',
		
		url :'/mooc/hwgrade',
			
		success :function(data) {
			
			alert("OK");
		
		}		
	});
	
	alert("打分成功！");
	//alert(pigai);
	//$(".grade").submit();

});
