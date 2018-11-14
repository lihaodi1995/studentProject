<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
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
        <li id="homework" class="side-bar"><a class="waves-effect waves-teal" href="tc-hw"><i class="material-icons">description</i>作业管理</a></li>
        <li id="teamwork " class="side-bar"><a class="waves-effect waves-teal" href="tc-tm"><i class="material-icons">group</i>团队管理</a></li>
        <li id="grade" class="side-bar"><a class="waves-effect waves-teal" href="tc-mk"><i class="material-icons">spellcheck</i>成绩登记</a></li>
        <li id="signin" class="side-bar baractive"><a class="waves-effect waves-teal" href="tc-ci"><i class="material-icons">assessment</i>签到统计</a></li>
        <li id="olddata" class="side-bar"><a class="waves-effect waves-teal" href="tc-od"><i class="material-icons">find_replace</i>以往数据</a></li>
        <li id="communication" class="side-bar"><a class="waves-effect waves-teal" href="http://kevinfeng.moe/chatroom.php?stuID=<%=tid %>"><i class="material-icons">chat</i>师生交流</a></li>
    </ul>
</div>
<main>
    <div class=" row right-content">
        <div class="row">
			<a class="waves-effect waves-light btn app-pass right beginci" >开始签到</a>
            <a class="waves-effect waves-light btn app-pass red right stopci"style="display: none;">结束签到</a>
            <div class="col s6">
                <ul class="tabs ">
                    <li class="tab col s6"><a class="active" href="#test2">缺勤记录</a></li>


                </ul>
            </div>
        
        <div id="test2" class="col s12">
            <table class="striped">
                <thead>
                <tr>
                    <th>学号</th>
                    <th>姓名</th>
                    <th>所属团队</th>
                    <th>缺勤记录</th>
                </tr>
                </thead>

                <tbody>

                </tbody>
            </table>
        </div>
        </div>
    </div>
</main>

<!--Import jQuery before materialize.js-->

</body>

<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script type="text/javascript" src="js/materialize.min.js"></script>
<script type="text/javascript" src="js/index.js"></script>
<script type="text/javascript" src="js/tc-ci.js"></script>

</html>
