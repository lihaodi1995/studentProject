<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@page import ="java.sql.*" %>
<%@page import="com.mysql.jdbc.Driver" %>
<!DOCTYPE html>
<html>
<head>
    <!--Import Google Icon Font-->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!--Import materialize.css-->
    <link type="text/css" rel="stylesheet" href="css/materialize.min.css" media="screen,projection"/>

    <!--Let browser know website is optimized for mobile-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

    <link type="text/css" rel="stylesheet" href="css/index.css">
</head>
<% String name = request.getSession().getAttribute("sessionusername").toString(); %>
<%String tid= request.getSession().getAttribute("sessionuserid").toString();%>
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
<div class="content">
    <ul id="nav-mobile" class="side-nav fixed" style="width: 250px;transform: translateX(0%);">
        <li id="courses" class="side-bar baractive"><a class="waves-effect waves-teal" href="indexTeacher"><i class="material-icons">date_range</i>课程管理</a></li>
        <li id="sources" class="side-bar"><a class="waves-effect waves-teal" href="tcresource"><i class="material-icons">theaters</i>资源管理</a></li>
        <li id="homework" class="side-bar"><a class="waves-effect waves-teal" href="tc-hw"><i class="material-icons">description</i>作业管理</a></li>
        <li id="teamwork " class="side-bar"><a class="waves-effect waves-teal" href="tc-tm"><i class="material-icons">group</i>团队管理</a></li>
        <li id="grade" class="side-bar"><a class="waves-effect waves-teal" href="tc-mk"><i class="material-icons">spellcheck</i>成绩登记</a></li>
        <li id="signin" class="side-bar"><a class="waves-effect waves-teal" href="tc-ci"><i class="material-icons">assessment</i>签到统计</a></li>
        <li id="olddata" class="side-bar"><a class="waves-effect waves-teal" href="tc-od"><i class="material-icons">find_replace</i>以往数据</a></li>
        <li id="communication" class="side-bar"><a class="waves-effect waves-teal" href="http://kevinfeng.moe/chatroom.php?stuID=<%=tid %>"><i class="material-icons">chat</i>师生交流</a></li>
    </ul>
</div>
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
				    //System.out.println("最后的查询结果为：");
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
			    }
			%>


                    <div class="row edit-dagang col s12 ">
                        <form class="col s12">
                            <div class="row">
                                <div class="input-field col s12">
                                    <input type="text" id="icon_prefix2" class="materialize-textarea fixText"></input>
                                    <label for="icon_prefix2">教学大纲</label>
                                </div>
                            </div>

                        </form>
                        <button class="btn waves-effect waves-light cyan edit-submit submit" type="submit" name="action">提交
                            <i class="material-icons right">send</i>
                        </button>
                        <a class="waves-effect waves-light btn cyan edit-cancel">取消</a>
                    </div>


                    <br/>

                    <br/>
                    <br/>
                    <a class="btn-floating halfway-fab waves-effect waves-light red " id="dagang-btn"><i
                            class="material-icons">mode_edit</i></a>

                </div>

                <!--<div class="card-action">-->
                <!--<a href="#">这是一个链接</a>-->

                <!--</div>-->
            </div>
        </div>
    </div>
</main>

<!--Import jQuery before materialize.js-->

</body>

<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script type="text/javascript" src="js/materialize.min.js"></script>
<script type="text/javascript" src="js/tc.js"></script>
<script type="text/javascript" src="js/index.js"></script>

</html>