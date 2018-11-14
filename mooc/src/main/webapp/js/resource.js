function srcDownloadAjax(type) { //添加标注后调用
	var flag = document.getElementsByClassName("flag").length;
	var count = 0;
	var files = "";
	
	$(".flag").each(function(i){
		//alert($(this).html());
		if($(this).html() == "label")
		{
			var next = $(this).next();
			
				files += $(this).next().html() + ",";
			//alert($(this).next().html());
				count++;
		}

		//alert(files);
	});	
	//alert(count);
	if(count == 0)
	{
		alert("未选择文件！");
		return false;
	}
	var f = {'files':files};
	$.get('downloadResourceRequest',f, function (content) {
		
		//alert(content);
		//alert(课程大纲修改成功)
		//$(".bigass").html(fix);
		var href = "/mooc/downloadResource";
        var $iframe = $('#iframeForExport');
        if ($iframe.length == 0) {
            $iframe = $('<iframe id="iframeForExport" style="display:none;" />');
            $('body').append($iframe);
        }
        $iframe.attr('src', href);
    })

}
$(".downloadSRC").click(function(){
	//alert($('#ID').is(':checked'));
	//alert("不能吃东西");
	srcDownloadAjax();
});

$("#down").click(function(){
	
	var flag = document.getElementsByClassName("flag").length;
	//var count = 0;
	var files = "";
	
	$(".flag").each(function(i){
		var x = i + 1;
		var name = "src" + x;
		
		if($("[id='"+name+"']").is(':checked'))
		{
			
			var parent = $(this).parent().parent().parent().next().next();
			
			files += parent.html() + ",";
			//alert(parent.html());
		}

		//alert(files);
	});	
	
	var f = {'files':files};
	$.get('downloadResourceRequest',f, function (content) {
		
		//alert(content);
		//alert(课程大纲修改成功)
		//$(".bigass").html(fix);
		var href = "/mooc/downloadResource";
        var $iframe = $('#iframeForExport');
        if ($iframe.length == 0) {
            $iframe = $('<iframe id="iframeForExport" style="display:none;" />');
            $('body').append($iframe);
        }
        $iframe.attr('src', href);
    })

});

$(".publish").click(function(){
	//alert($("#name").html());
//	var name = $("#name").html();
//    //var strs = tmp.split(".");
//	
//	//alert(name.split('，'));
//	var name1 = name.split('，');
//	name1 = name1[1];
	//alert(name1);
	var countli = document.getElementsByTagName("li").length - 10;
	//alert(countli);
	var num = "src" + countli;
	//alert("不能吃东西");
	if($("#srcheadline").val() == "")
	{
		alert("标题为空！");
		$("#srcheadline").focus();
		return false;
	}
	if($("#srccontent").val() == "")
	{
		alert("内容为空！");
		$("#srccontent").focus();
		return false;
	}
	if($("#srcfile").val() == "")
	{
		alert("未选择文件！");
		$("#srcfile").focus();
		return false;
	}
	
    var header=$('#srcheadline').val();
    var content=$('#srccontent').val();
    var filename=$("#srcfile").val().split("\\");
    //var strs = tmp.split(".");
	filename = filename[filename.length-1];
    
    var headerhtml='<li> <div class="collapsible-header"> <div class="col s1 m1 selectDown"> <form> <p> <input type="checkbox" name="checkbox" class="filled-in" id="'
    + num +'"> <label for="'+ num +'"></label> </p> </form> </div> <i class="material-icons">filter_drama</i>';
    var middlehtml1='<i class="material-icons text-black right">play_for_work</i> </div> <div class="collapsible-body"> <span>';
    var middlehtml2='</span></div><div class="collapsible-body file"><span>';
    var footerhtml='</span> </div> </li>';

    $('.show-src').append(headerhtml + header + middlehtml1 + content + middlehtml2 + filename + footerhtml);

	
	
	/*var uploadfile = {'name': name1, 'title': $("#srcheadline").val(), 'content': $("#srccontent").val(), 'file': $("#srcfile").val()};		
	if(typeof jQuery !='undefined') {	 
	    alert("jQuery library is loaded!");	 
	}
	else { 
	    alert("jQuery library is not found!"); 
	}
	$.ajax({
		type:'POST',	
		data:JSON.stringify(uploadfile),
		contentType: "application/json; charset=utf-8", 
		dataType:'json',	
		url :'/mooc/uploadSRC',		
		success :function(data) {		
			alert("OK");	
		}		
	});*/
	$(".newsrc").submit();	
	alert("发布成功！");
});

$(".deletesrc").click(function(){
	//alert("sad");
	var files = "";
	$(".flag").each(function(i){
		var x = i + 1;
		var name = "src" + x;
		
		if($("[id='"+name+"']").is(':checked'))
		{
			
			var parent = $(this).parent().parent().parent().next().next();
			
			files += parent.html() + ",";

			$(this).parent().parent().parent().parent().parent().remove();


		}
	});
	$.ajax({
		
		type:'POST',
		
		data: files,
		
		contentType: "application/json; charset=utf-8", 
		dataType:'text',
		
		url :'/mooc/deleteSRC',
			
		success :function(data) {
			
			//alert("OK");
		
		}		
	});
	alert("删除成功！");
});

