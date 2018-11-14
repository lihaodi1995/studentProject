<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@page import ="java.sql.*" %>
<%@page import="com.mysql.jdbc.Driver" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/materialize-custom.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/index.css" media="screen,projection">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body>
<%String name = request.getSession().getAttribute("sessionusername").toString();%>
<%String id= request.getSession().getAttribute("sessionuserid").toString();%>
<div class="header navbar-fixed">
    <nav>
        <div class="nav-wrapper cyan fixed">
            <a href="#!" class="brand-logo">SEPS</a>
            <ul class="right hide-on-med-and-down">
            	<li>你好，</li>
            	<li id="name"><%= name%></li>
            	<li>-</li>
            	<li>ID:</li>
                <li id="stuID"><%=id %></li>
                <li><a href="#" id="sign">签到</a></li>
                <li><a href="logout" id="logout">注销</a></li>
            </ul>
        </div>
    </nav>
</div>

<header>
    <ul id="nav-mobile" class="side-nav fixed">
        <li class="bold side-bar active">
            <a href="indexStudent" class="waves-effect waves-cyan"><i class="material-icons">date_range</i>课程信息</a>
        </li>
        <li class="bold side-bar">
            <a href="team-stu" class="waves-effect waves-cyan"><i class="material-icons">group</i>团队</a>
        </li>
        <li class="bold side-bar">
            <a href="resource" class="waves-effect waves-cyan"><i class="material-icons">theaters</i>资源</a>
        </li>
        <li class="bold side-bar">
            <a href="homework-stu" class="waves-effect waves-cyan"><i class="material-icons">description</i>作业</a>
        </li>
        <li class="bold side-bar">
            <a href="http://kevinfeng.moe/chatroom.php?stuID=<%=id %>" class="waves-effect waves-cyan"><i class="material-icons">chat</i>交流</a>
        </li>
    </ul>
</header>
	  <%
					Connection conn = null;
				    //加载数据库驱动类
				    Class.forName("com.mysql.jdbc.Driver").newInstance();
				    //数据库连接URL
				    String url="jdbc:mysql://localhost:3306/rua?characterEncoding=UTF-8";
				    //数据库用户名和密码
				    String user="root";
				    String  password="";
				    //根据数据库参数取得一个数据库连接值
				    conn =  DriverManager.getConnection(url,user,password);
				    //out.print("取得一个数据库连接:\n");
				    //out.print(conn.toString());
				   
				    //判断是否登录，如果登录按照用户名查询
				    String sql = "select * from course where ID = '1'";		// 查询数据的sql语句
				    Statement st = (Statement) conn.createStatement();	//创建用于执行静态sql语句的Statement对象，st属局部变量
					
				    ResultSet rs = st.executeQuery(sql);	//执行sql查询语句，返回查询数据的结果集
				    System.out.println("最后的查询结果为：");
				    while (rs.next()) {	// 判断是否还有下一个数据
					   
						// 根据字段名获取相应的值
						String tp = rs.getString("tp");
						String coname = rs.getString("Name");
						String start = rs.getString("Start_time");
						String end = rs.getString("End_time");
						String info = rs.getString("Info");
						String place = rs.getString("place");
						String teacher = rs.getString("teacher");
						String score = rs.getString("score");
						String people = rs.getString("people");
						//System.out.println(content);
			%>
<main>
    <div class="container">
        <div class="col m12 s12">
            <div class="card ">

                <div class="card-content black-text">
                    <span class="card-title"><%= coname%></span>
                    <p>
                        	课程简介：<%= info%>
                    </p>
                    <br/>
                    <p>
                        	任课教师：<%= teacher%>
                    </p>
                    <br/>
                    <p>
                       		 上课地点：<%= place%>
                    </p>
                    <br/>
                    <p>学分：<%= score%></p>
                    <br/>

                    <p>学生人数：<%= people%></p>
                    <br/>
                    <p>开课时间：<%= start%>---<%= end%></p>
                    <br/>
			      <p class="show-dagang bigass">
		              <%= tp%>
		            </p>
			   
			<%
			    //conn.close();
				    }
				    conn.close();
			%>


                    <br/>

                    <br/>
                    <br/>

                </div>

                <!--<div class="card-action">-->
                <!--<a href="#">这是一个链接</a>-->

                <!--</div>-->
            </div>
        </div>
    </div>
</main>
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script type="text/javascript" src="js/materialize.min.js"></script>
<script>
$("#sign").click(function(){
	//alert($("#stuID").html());
	var stu = "id=" + $("#stuID").html();
	//var users = {'stuID': $("#stuID").html()};
	
	$.ajax({
	
		type:'GET',
		
		data:stu,
		
		contentType: "application/json; charset=utf-8", 
		dataType:'text',
		
		url :'/mooc/signIn',
			
		success :function(data) {
			
			//alert("OK");
		
		}		
	});
	alert("签到成功！")
});
</script>

</body>
</html>