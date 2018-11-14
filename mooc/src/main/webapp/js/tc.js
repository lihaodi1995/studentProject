$(".submit").click(function(){
	//alert("不能吃饭");
	var fix = $(".fixText").val();
	var cf = {'tp': fix};
//	$.post('/mooc/bigAss', cf, function (content) {
//		
//		//alert(fix);
//		alert("课程大纲修改成功");
//		$(".bigass").html(fix);
//		
//    })
	$.ajax({
		
		type:'POST',
		
		data: JSON.stringify(cf),
		
		contentType: "application/json; charset=utf-8", 
		dataType:'json',
		
		url :'/mooc/bigAss',
			
		success :function(data) {
			
			alert("OK");
		
		}		
	});
	$(".bigass").html(fix);
	alert("课程大纲修改成功");
});
