<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@page import ="java.sql.*" %>
<%@page import="com.mysql.jdbc.Driver" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>课程管理</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/materialize-custom.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/dn-course.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/index.css" media="screen,projection">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<%String name = request.getSession().getAttribute("sessionusername").toString();%>
<body>
<div class="header navbar-fixed">
    <nav>
        <div class="nav-wrapper cyan fixed">
            <a href="#!" class="brand-logo">SEPS</a>
            <ul class="right hide-on-med-and-down">
            	<li>你好，<%= name%></li>
                <li><a href="logout" id="logout">注销</a></li>
            </ul>
        </div>
    </nav>
</div>
<header>
    <ul id="nav-mobile" class="side-nav fixed">
        <li class="bold side-bar active">
            <a href="#" class="waves-effect waves-cyan"><i class="material-icons">date_range</i>课程管理</a>
        </li>
        <li class="bold side-bar">
            <a href="dn-account" class="waves-effect waves-cyan"><i class="material-icons">group</i>学生/教师账号</a>
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
            <div class="card">
                <div class="card-content black-text row">
                    <span class="card-title origin-info" id="course-name"><%= coname%></span>
                    <div class="edit input-field">
                        <input type="text" class="validate" id="course-name-edit">
                        <label for="course-name-edit">课程名:</label>
                    </div>
                    <p>
                        <span id="course-info-title">课程简介: </span>
                        <span id="course-info" class="origin-info"><%= info%>
                        </span>
                    <div class="edit input-field">
                        <input class="validate" id="course-info-edit" type="text" class="materialize-textarea"></input>
                        <label for="course-info-edit"></label>
                    </div>
                    </p>
                    <br/>
                    <p>
                        <span>任课教师：</span>
                        <span id="course-teacher" class="origin-info"><%= teacher%></span>
                   		 <div class="edit input-field">
                        <input type="text" class="validate" id="course-teacher-edit">
                        <label for="course-teacher-edit"></label>
                    </div>
                    </p>
                    <br/>
                    <p>
                        <span>上课地点：</span>
                        <span id="course-place" class="origin-info"><%= place%></span>
                        <div class="edit input-field inline" style="display: none">
                        <input type="text" class="validate" id="course-place-edit">
                        <label for="course-place-edit"></label>
                    </div>
                    </p>
                    <br/>
                    <p>
                        <span >学分：</span>
                        <span id="course-score" class="origin-info"><%= score%></span>
                        <div class="edit input-field">
                        <input type="number" class="validate" id="course-score-edit">
                    <label for="course-score-edit"></label>
                    </div>
                    </p>
                    <br/>
                    <p>
                        <span >学生人数：</span>
                        <span id="course-people" class="origin-info"><%= people%></span>
                        <div class="edit input-field">
                        <input type="number" class="validate" id="course-people-edit">
                    <label for="course-people-edit"></label>
                    </div>
                    </p>
                    <br/>
                    <p>
                        <span >开课时间：</span>
                        <span id="course-date-start" class="origin-info"><%= start%></span>
                        <input type="date" class="edit datepicker" id="course-date-start-edit" placeholder="开始时间">
                        <span class="" style="text-align: center">---</span>
                        <span id="course-date-end" class="origin-info"><%= end%></span>
                        <input type="date" class="edit datepicker" id="course-date-end-edit" placeholder="结束时间">
                    </p>
                    <br/>
                    <p>
                        	教学大纲：<%= tp%>

                    </p>

                    <button id="course-save" class="edit-button btn waves-effect waves-light cyan" type="submit"
                            name="action" style="display: none">确认
                        <i class="material-icons right">send</i>
                    </button>
                    <button id="course-cancel" class="edit-button waves-effect waves-light btn cyan edit-cancel">取消
                    </button>

			<%
			    //conn.close();
				    }
				    conn.close();
			%>
                    <br/>

                    <br/>
                    <br/>
                    <a class="btn-floating halfway-fab waves-effect waves-light red " id="course-edit"><i
                            class="material-icons">mode_edit</i></a>

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
<script type="text/javascript" src="js/dn-course.js"></script>
</body>
</html>