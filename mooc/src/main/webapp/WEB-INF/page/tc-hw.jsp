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
	<%String name = request.getSession().getAttribute("sessionusername").toString();%>
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
        <li id="courses" class="side-bar"><a class="waves-effect waves-teal" href="indexTeacher"><i class="material-icons">date_range</i>课程管理</a></li>
        <li id="sources" class="side-bar"><a class="waves-effect waves-teal" href="tcresource"><i class="material-icons">theaters</i>资源管理</a></li>
        <li id="homework" class="side-bar baractive"><a class="waves-effect waves-teal" href="tc-hw"><i class="material-icons">description</i>作业管理</a></li>
        <li id="teamwork " class="side-bar"><a class="waves-effect waves-teal" href="tc-tm"><i class="material-icons">group</i>团队管理</a></li>
        <li id="grade" class="side-bar"><a class="waves-effect waves-teal" href="tc-mk"><i class="material-icons">spellcheck</i>成绩登记</a></li>
        <li id="signin" class="side-bar"><a class="waves-effect waves-teal" href="tc-ci"><i class="material-icons">assessment</i>签到统计</a></li>
        <li id="olddata" class="side-bar"><a class="waves-effect waves-teal" href="tc-od"><i class="material-icons">find_replace</i>以往数据</a></li>
        <li id="communication" class="side-bar"><a class="waves-effect waves-teal" href="http://kevinfeng.moe/chatroom.php?stuID=<%=tid %>"><i class="material-icons">chat</i>师生交流</a></li>
    </ul>
</div>
<main>
    <div class=" row right-content">
        <div class="container1">
            <div class="toolbox">
                <a class="waves-effect waves-light btn choosesrc">全选</a>
                <a class="waves-effect waves-light btn choosenot">反选</a>
                
                <a class="waves-effect waves-light btn publishsrc" href="#modal1">发布新作业</a>
                <a class="waves-effect waves-light btn hwtable" href="exportHw">下载作业报表</a>
                <a class="waves-effect waves-light btn downloasrc" id="down">批量下载</a>
                <a class="waves-effect waves-light btn deletesrc red deletehw ">删除</a>


            </div>
            <div id="modal1" class="modal">
                <div class="modal-content">
                    <div class="row">
                        <form class="col s12 newhw" action="/mooc/publishHW" >
                            <div class="row">
                                <div class="input-field col s6">
                                    <input  id="hwheadline" type="text" class="validate" name = "title">
                                    <label for="hwheadline">标题</label>
                                </div>
                                <div class="input-field col s6">
                                    <input  id="hwbili" type="text" class="validate" name = "weight">
                                    <label for="hwbili">占分比例</label>
                                </div>
                                
                                <div class="input-field col s12">
                                    <input  type="text" id="hwcontent" class="validate" name ="explain">
                                    <label for="shwcontent">文字说明</label>
                                </div>
                            </div>


                        </form>
                    </div>
                </div>
                <div class="modal-footer">
                    <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat publish">发布</a>
                    <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat">取消</a>
                </div>
            </div>
             <div id="modal2" class="modal">
                <div class="modal-content">
                    <div class="row">
                            <div class="row">
                                <div class="input-field col s6">
                                    <input  id="hwgrade" type="text" class="validate">
                                    <label for="hwgrade">作业打分</label>
                                </div>
                                 <div class="input-field col s12">
                                    <input  id="hwcomment" type="text" class="validate">
                                    <label for="hwcomment">作业评论</label>
                                </div>
                            </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat confirm">确认</a>
                    <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat">取消</a>
                </div>
            </div>
            
            <br>
            <div class="row">

                <div class="col s12 m12">
                    <ul class="collapsible popout show-hw" data-collapsible="accordion">
                    
                      <%
                      Connection conn = null;
                      Connection conn1 = null;
                      int i = 1;
                      //for (int j =1; j<=20; j++) {
						  
						  String hw = "hw";
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
					    	String hwname = hw + i;
							String title = rs.getString("Title");
							//int id = rs.getInt("Resources_id");
							String info = rs.getString("info");
							String bili = rs.getString("weight");
							
							String sql1 = "select * from sub_text where Task_Title = \'" + title + "\'";		// 查询数据的sql语句
						    Statement st1 = (Statement) conn1.createStatement();	//创建用于执行静态sql语句的Statement对象，st属局部变量
																	
						    ResultSet rs1 = st1.executeQuery(sql1);	//执行sql查询语句，返回查询数据的结果集

						%>			                           			 
                		<li>
                            <div class="collapsible-header hwtitle">
                                <div class="col s1 m1 selectDown">
                                    <form>
                                        <p>
                                            <input type="checkbox" name="checkbox" class="filled-in flag" id="<%= hwname%>">
                                            <label for="<%= hwname%>"></label>
                                        </p>
                                    </form>
                                </div>
                                <i id=<%= i%> class="material-icons">filter_drama</i><p><%= title%></p>
                            </div>
                            <div class="collapsible-body"><span><%= info%> </span><span class="right">占分比例：<%= bili%> </span></div>               			 
                			 
                	   	<%
                	   		System.out.println(title);
                	   		while (rs1.next()) {
                	   			System.out.println("1");
                	   			String file = rs1.getString("Text_id");
                	   			String group = rs1.getString("Group_id");
                	   			System.out.println(group);
			            %>
           				    <div class="collapsible-body file"><span><%= file %></span>
                           		<p class="text-black right">团队ID：<%= group %></p>
                            	<a href="#modal2"><i class="material-icons text-black right score">check</i></a>
                            </div>
			   
						<%
						System.out.println("3");
						    }
                	   		System.out.println("2");
						    %>

			           	<%
			           	i++;    
					    }%>
						    </li>
			           <%
	                     
                      conn.close();
                      conn1.close();
						%>
                    </ul>

                </div>
            </div>
        </div>
    </div>
</main>

<!--Import jQuery before materialize.js-->

</body>

<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script type="text/javascript" src="js/materialize.min.js"></script>
<script type="text/javascript" src="js/index.js"></script>
<script type="text/javascript" src="js/homework.js"></script>

</html>