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

<body>

<% String name = request.getSession().getAttribute("sessionusername").toString(); %>
<%String tid= request.getSession().getAttribute("sessionuserid").toString();%>

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
        <li id="sources" class="side-bar baractive"><a class="waves-effect waves-teal" href="tcresource"><i class="material-icons">theaters</i>资源管理</a></li>
        <li id="homework" class="side-bar"><a class="waves-effect waves-teal" href="tc-hw"><i class="material-icons">description</i>作业管理</a></li>
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
                <a class="waves-effect waves-light btn publishsrc" href="#modal1">发布新资源</a>
                <a class="waves-effect waves-light btn publishsrc" href="#modal2">拖拽上传</a>
                <a class="waves-effect waves-light btn downloasrc" id="down">批量下载</a>
                <a class="waves-effect waves-light btn deletesrc red ">删除</a>


            </div>
            <div id="modal1" class="modal">
                <div class="modal-content">
                    <div class="row">
                        <form class="col s12 newsrc" method = "post" enctype="multipart/form-data" action="/mooc/uploadSRC">
                            <div class="row">
                                <div class="input-field col s6">
                                    <input  id="srcheadline" type="text" class="validate" name="title">
                                    <label for="srcheadline">标题</label>
                                </div>
                                <div class="input-field col s12">
                                    <input  type="text" id="srccontent" class="validate" name="content">
                                    <label for="srccontent">文字说明</label>
                                </div>
                            </div>
                            <div class="file-field input-field">
                                <div class="btn">
                                    <span>文件</span>
                                    <input id="srcfile" type="file" name="file" multiple>
                                </div>
                                <div class="file-path-wrapper">
                                    <input class="file-path validate" type="text" placeholder="Upload one or more files">
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="modal-footer">
                    <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat src-public publish">发布</a>
                    <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat">取消</a>
                </div>
            </div>
            <div id="modal2" class="modal">
                <div class="modal-content drag-box"  id="drag-box">
                    <div class="row " >
                        <form class="col s12 ">
                            <div class="row">
                                <div class="input-field col s6">
                                    <input  id="srcheadlinedg" type="text" class="validate">
                                    <label for="srcheadline">标题</label>
                                </div>
                                <div class="input-field col s12">
                                    <input  type="text" id="srccontentdg" class="validate">
                                    <label for="srccontent">文字说明</label>
                                </div>
                            </div>
                            <div class="file-field input-field">
                                <div class="btn">
                                    <span>文件</span>
                                    <input type="file" multiple>
                                </div>
                                <div class="file-path-wrapper">
                                    <input class="file-path validate" type="text" placeholder="点击或拖拽上传文件">
                                </div>
                            </div>


                        </form>
                    </div>
                </div>
                <div class="modal-footer">
                    <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat src-publicdg">发布</a>
                    <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat">取消</a>
                </div>
            </div>
            
            <br>
            <div class="row">

                <div class="col s12 m12">
                    <ul class="collapsible popout show-src" data-collapsible="accordion">
                      <%
                      Connection conn = null;
                      int i = 1;
                      String ex = "";
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
							//System.out.println(rs.next().getString("title"))
							//System.out.println(ex);
							String title = rs.getString("title");
							//System.out.println("1" + title);
							
							if(title.equals(ex))
								x = 1;
							int id = rs.getInt("Resources_id");
							String file = rs.getString("path");
							//System.out.println(rs.getString("path"));
							//System.out.println("a" + x);
							//i++;
							if(x == 0) {
						%>			            
						<li>
			                <div class="collapsible-header">
			                    <div class="col s1 m1 selectDown">
			                        <form>
			                            <p>
			                                <input type="checkbox" name="checkbox" class="filled-in flag" id="<%= srcname%>">
			                                <label for="<%= srcname%>"></label>
			                            </p>
			                        </form>
			                    </div>
							 <i id=<%= i%> class="material-icons">whatshot</i><p><%= title%></p>     
							 </div>   
			                
                			 <div class="collapsible-body src"><span><%= file%></span></div>
                			 
                	   	<%
			                x++;
			                //System.out.println("b" + x);
						}
							else {//System.out.println("c" + x);
			            %>
           					<div class="collapsible-body src"><span><%= file%></span></div>
			   
						<%
						    
							}%>

			           	<%
			           	i++; 
			           	//System.out.println("2" + title);
			           	ex = title;
			           	//System.out.println("2" + ex);
					    }%>
						   
			           <%
	                  }%>
	                  </li>
                      <%
                      conn.close();
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
<script type="text/javascript" src="js/resource.js"></script>
<script type="text/javascript" src="js/index.js"></script>
<script type="text/javascript" src="js/tc-src.js"></script>
</html>