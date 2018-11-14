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
    <link type="text/css" rel="stylesheet" href="css/materialize.css" media="screen,projection"/>
    <link type="text/css" rel="stylesheet" href="css/materialize-custom.css" media="screen,projection"/>
    <link type="text/css" rel="stylesheet" href="css/resource-stu.css" media="screen,projection"/>
    <link type="text/css" rel="stylesheet" href="css/index.css" media="screen,projection">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

</head>
<%String name = request.getSession().getAttribute("sessionusername").toString();%>
<%String sid= request.getSession().getAttribute("sessionuserid").toString();%>
<body>
<div class="header navbar-fixed">
    <nav>
        <div class="nav-wrapper cyan fixed">
            <a href="#!" class="brand-logo">SEPS</a>
            <ul class="right hide-on-med-and-down">
            	<li>你好，</li>
            	<li id="name"><%= name%></li>
            	<li>-</li>
            	<li>ID:</li>
                <li id="stuID"><%=sid %></li>
                <li><a href="#" id="sign">签到</a></li>
                <li><a href="logout" id="logout">注销</a></li>
            </ul>
        </div>
    </nav>
</div>
<header>
    <ul id="nav-mobile" class="side-nav fixed">
        <li class="bold side-bar">
            <a href="indexStudent" class="waves-effect waves-cyan"><i class="material-icons">date_range</i>课程信息</a>
        </li>
        <li class="bold side-bar">
            <a href="team-stu" class="waves-effect waves-cyan"><i class="material-icons">group</i>团队</a>
        </li>
        <li class="bold side-bar active">
            <a href="resource" class="waves-effect waves-cyan"><i class="material-icons">theaters</i>资源</a>
        </li>
        <li class="bold side-bar">
            <a href="homework-stu" class="waves-effect waves-cyan"><i class="material-icons">description</i>作业</a>
        </li>
        <li class="bold side-bar">
            <a href="http://kevinfeng.moe/chatroom.php?stuID=<%=sid %>" class="waves-effect waves-cyan"><i class="material-icons">chat</i>交流</a>
        </li>
    </ul>
</header>
<main>
    <div class="container">
        <div class="row">
            <button class="col offset-m10 m2 waves-effect waves-light cyan btn downloadSRC">下载</button>
        </div>
        <div class="row">

			  <%
                      Connection conn = null;
			  		  String ex = "";
                      int i = 1;
                      int y = 0;
                      for (int j =1; j<=40; j++) {
						  
						  String src = "src";
						  //Connection conn = null;
						 
					    //加载数据库驱动类
					    Class.forName("com.mysql.jdbc.Driver").newInstance();
					    //数据库连接URL
					    String url="jdbc:mysql://localhost:3306/rua";
					    //数据库用户名和密码
					    String user="root";
					    String  password="";
					    //根据数据库参数取得一个数据库连接值
					    conn =  DriverManager.getConnection(url,user,password);
					 
						String desc = j + "";
					    //out.print("取得一个数据库连接:\n");
					    //out.print(conn.toString());
					    //System.out.println(j);
					    //判断是否登录，如果登录按照用户名查询
					    //String sql = "select * from entity_label where username = \'" + username + "\'";
					    //String sql = "insert into upload values"+"("+"\""+resourceid+"\","+"\""+title+"\",\""+hw+"\",\""+id+"\",\""+strdate+"\",\""+fileName+"\")";
					    String sql = "select * from upload where Resources_id = \'" + desc + "\'";		// 查询数据的sql语句
					    Statement st = (Statement) conn.createStatement();	//创建用于执行静态sql语句的Statement对象，st属局部变量
																
					    ResultSet rs = st.executeQuery(sql);	//执行sql查询语句，返回查询数据的结果集
				    	
					    //System.out.println("最后的查询结果为：");
					    String srcname = src + i;
					    
					    while ((rs.next())) {	// 判断是否还有下一个数据
					    	int x = 0;
					    	//String file;
					    	//System.out.println("最后的查询结果1为：");
					
						  //String srcname = src + i;
						  //System.out.println(name);
							// 根据字段名获取相应的值
							
							String title = rs.getString("title");
							int id = rs.getInt("Resources_id");
							String file = rs.getString("path");
							//System.out.println(rs.getString("path"));
							//System.out.println("a" + x);
							if(title.equals(ex)) {
								x = 1;
								y = 1;
							}
							//System.out.println(title.equals(ex));
							if(!(title.equals(ex)))
								y = 0;
							//i++;
							if(x == 0) {
						%>		
									            
                      <div id="<%= id%>" class="col m12 resource opacity z-depth-2">
			                <i class="material-icons check flag">label_outline</i>
			                <span class="kind"><%= title%></span>
			            </div>
			            
			                <p><span><%= file%></span></p>
                			 
                	   	<%
			                x++;
			                //System.out.println("b" + x);
						}
							else {
								//System.out.println("c" + x);
			            %>
           					 <p><span><%= file%></span></p>
			   
						<%
						    }%>

			           	<%
			           	i++; 
			           	ex = title;
					    }
					    System.out.println(y);
					    if(y==0) {
					    %>
	    
			           <%
					    }
					    }%>
	                   
	                      <%
                      conn.close();
			%>

        </div>
    </div>
</main>
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
    <script type="text/javascript" src="js/resource.js"></script>
<script>
   /* $('.resource').click(function () {
        var _this=this;
//        $(_this).find('.resContent').toggle('normal');
        if($(_this).css('margin-bottom')=='0px'){
            $(_this).next().slideUp('normal');
            $(_this).css('margin-bottom','8px');
        }else{
            $(_this).css('margin-bottom','0px');
            $(_this).next().slideDown('normal');
        }
    })*/

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

    $('.check').click(function () {
        var _this=this;
        if($(_this).html()=='label_outline'){
            $(_this).html('label')
        }else{
            $(_this).html('label_outline')
        }
    })
</script>
</body>
</html>