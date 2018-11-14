$("#log").click(function(){
	var user = {'Id': $(".userName").val(), 'password': $(".userPsd").val()};
	$.post('/mooc/loginCheck',user,function (result) {
		//alert(result);
		if(result == "no")
		{
			alert("用户名不存在！");
			$(".userName").focus();
		}
		else if(result == "wrong")
		{
			alert("密码错误！");
			$(".userPsd").focus();
		}
		else if(result == "jiaowu")
		{
			alert("教务登录成功！");
			window.location.href="dncourse";
		}
		else if(result == "teacher")
		{
			alert("教师登录成功！");
			window.location.href="indexTeacher";
		}
		else if(result == "student")
		{
			alert("学生登录成功！");
			window.location.href="indexStudent";
		}
    })
});
