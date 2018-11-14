<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@page import ="java.sql.*" %>
<%@page import="com.mysql.jdbc.Driver" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>课程作业</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/materialize-custom.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/homework-stu.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/index.css" media="screen,projection">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

    <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
    <script type="text/javascript" src="js/materialize.min.js"></script>
</head>
<%String name = request.getSession().getAttribute("sessionusername").toString();
String groupid = request.getSession().getAttribute("sessiongroupid").toString();%>
<%String id= request.getSession().getAttribute("sessionuserid").toString();%>
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
                <li id="stuID"><%=id %></li>
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
        <li class="bold side-bar">
            <a href="resource" class="waves-effect waves-cyan"><i class="material-icons">theaters</i>资源</a>
        </li>
        <li class="bold side-bar active">
            <a href="homework-stu" class="waves-effect waves-cyan"><i class="material-icons">description</i>作业</a>
        </li>
        <li class="bold side-bar">
            <a href="http://kevinfeng.moe/chatroom.php?stuID=<%=id %>" class="waves-effect waves-cyan"><i class="material-icons">chat</i>交流</a>
        </li>
    </ul>
</header>
<main>
    <div class="container">
	<%
                      Connection conn = null;
                      Connection conn1 = null;
                      int i = 1;
                      //for (int j =1; j<=20; j++) {
						  
						  String ta = "ta";
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
					    conn1 =  DriverManager.getConnection(url,user,password);
						//String desc = j + "";
					    
					    String sql = "select * from task where Course_id = 1";		// 查询数据的sql语句
					    Statement st = (Statement) conn.createStatement();	//创建用于执行静态sql语句的Statement对象，st属局部变量
																
					    ResultSet rs = st.executeQuery(sql);	//执行sql查询语句，返回查询数据的结果集
					    
					    
				    	
					    //System.out.println("最后的查询结果为：");
					   
					    int x = 0;
					  
					    while ((rs.next())) {	// 判断是否还有下一个数据
					    	//String file;
					    	String taname = ta + i;
							String title = rs.getString("Title");
							//int id = rs.getInt("Resources_id");
							String info = rs.getString("info");
							String bili = rs.getString("weight");
							
							String sql1 = "select * from sub_text where Task_Title = \'" + title + "\'";		// 查询数据的sql语句
						    Statement st1 = (Statement) conn.createStatement();	//创建用于执行静态sql语句的Statement对象，st属局部变量
																	
						    ResultSet rs1 = st1.executeQuery(sql1);	//执行sql查询语句，返回查询数据的结果集
						    //System.out.println(rs1.next());
						    int z = 0;

						%>			                           			 
                            
                        <div class="row">
				            <div class="col m10 valign-wrapper homework opacity z-depth-2 hwTitle">
				            <!--<i class="material-icons check">label</i>-->
				                <span><%= title%>
				                                	   	<%
                	   	while (rs1.next()) {
                	   			//String file = rs1.getString("Text_id");
                	   			String group = rs1.getString("Group_id");
                	   			if((group.equals(groupid))&&(z==0)) {
			            %>
							<div class="col m2 valign-wrapper download opacity right"> 已提交 </div>
			   
						<%
                	   			z = 1;
                	   			}
                	   			}%>
				                </span>
				            </div>
    					</div>
				        <div class="row">
				            <div class="col m12 opacity hwContent z-depth-1">
				                <p><%= info%></p>
				                <form id="<%=i %>" class="work"  method = "post" enctype="multipart/form-data" action="/mooc/uploadHW">
				                	<input  type="text" class="col m2 valign-wrapper download opacity right" style="opacity: 0; width: 1; height: 1;" name= "title" value="<%= title%>"></input>
				                    <div class="file-field input-field">
				                        <div class="btn cyan">
				                            <span>打开</span>
				                            <input type="file" multiple name="file">
				                        </div>
				                        <div class="file-path-wrapper">
				                            <input class="file-path validate" type="text" placeholder="请选中文件">
				                        </div>
				                    </div>
				                    <div class="input-field">
				                        <textarea id="<%= taname%>" class="materialize-textarea" name="info"></textarea>
				                        <label for="<%= taname%>">附件说明:</label>
				                    </div>
				                    <button id="submit" class="waves-effect waves-light cyan btn submit-btn submit"><i class="material-icons right">send</i>提交</button>
				                </form>
				            </div>
				        </div>             			 
                			 


			           	<%
			           	i++;    
					    }%>
						
	<%
                    Connection conn2 = null;

				 
			    //加载数据库驱动类
			    Class.forName("com.mysql.jdbc.Driver").newInstance();
			    //数据库连接URL
			    String url2="jdbc:mysql://localhost:3306/rua";
			    //数据库用户名和密码
			    String user2="root";
			    String  password2="";
			    //根据数据库参数取得一个数据库连接值
			    conn2 =  DriverManager.getConnection(url2,user2,password2);

			    String sql2 = "select * from sub_text where Group_id = \'" + groupid + "\'";		// 查询数据的sql语句
			    Statement st2 = (Statement) conn2.createStatement();	//创建用于执行静态sql语句的Statement对象，st属局部变量
														
			    ResultSet rs2 = st.executeQuery(sql2);	//执行sql查询语句，返回查询数据的结果集
			    
			    
		    	
			    //System.out.println("最后的查询结果为：");
			   
			   // int x = 0;
			  
			    while ((rs2.next())) {	// 判断是否还有下一个数据
			    	//String file;
			    	//String taname = ta + i;
					String titl = rs2.getString("Task_Title");
					//int id = rs.getInt("Resources_id");
					String grade = rs2.getString("grade");
					String comm = rs2.getString("comment");

				%>		
					<div>
						<span>作业题目：<%=titl %></span>
						<span>作业分数：<%=grade %></span>
						<span>作业评论：<%=comm %></span>
					</div>
				<%}
                conn.close();
                conn1.close();	
			    conn2.close();
			    %>	 

    		
    </div>
</main>
<script>
    $('.homework').click(function () {
        var _this=this;
//        $(_this).find('.hwContent').toggle('normal');
        if($(_this).css('margin-bottom')=='8px') {
            $(_this).closest('.row').next().find('.hwContent').slideDown('normal');
            $(_this).css('margin-bottom','0px');
            $(_this).next().css('margin-bottom','0px');
        }else{
            $(_this).closest('.row').next().find('.hwContent').slideUp('normal');
            setTimeout(function(){
                $(_this).css('margin-bottom','8px');
                $(_this).next().css('margin-bottom','8px');
            },300);
        }
    })
    $("#submit").click(function(){
	
    	var parent = $(this).parent().parent().parent().prev().children().children();
    	//alert(parent.children().html());
    	if(parent.children().html() == undefined) {
    		var flag = ' <div class="col m2 valign-wrapper download opacity right"> 已提交 </div> ';
			parent.append(flag);
    	}
    	alert("提交成功！");
		//var flag = ' <div class="col m2 valign-wrapper download opacity right"> 已提交 </div> ';
		//parent.append(flag);
		//alert($(this).parent().is('form'));
		$(this).parent().submit();
		

	});

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

    
//    $('.check').click(function () {
//        var _this=this;
//        if($(_this).html()=='label_outline'){
//            $(_this).html('label')
//        }else{
//            $(_this).html('label_outline')
//        }
//    })
</script>
</body>
</html>