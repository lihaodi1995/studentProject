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
        <li id="courses" class="side-bar"><a class="waves-effect waves-teal" href="indexTeacher"><i class="material-icons">date_range</i>课程管理</a></li>
        <li id="sources" class="side-bar"><a class="waves-effect waves-teal" href="tcresource"><i class="material-icons">theaters</i>资源管理</a></li>
        <li id="homework" class="side-bar"><a class="waves-effect waves-teal" href="tc-hw"><i class="material-icons">description</i>作业管理</a></li>
        <li id="teamwork " class="side-bar baractive"><a class="waves-effect waves-teal" href="tc-tm"><i class="material-icons">group</i>团队管理</a></li>
        <li id="grade" class="side-bar"><a class="waves-effect waves-teal" href="tc-mk"><i class="material-icons">spellcheck</i>成绩登记</a></li>
        <li id="signin" class="side-bar"><a class="waves-effect waves-teal" href="tc-ci"><i class="material-icons">assessment</i>签到统计</a></li>
        <li id="olddata" class="side-bar"><a class="waves-effect waves-teal" href="tc-od"><i class="material-icons">find_replace</i>以往数据</a></li>
        <li id="communication" class="side-bar"><a class="waves-effect waves-teal" href="http://kevinfeng.moe/chatroom.php?stuID=<%=tid %>"><i class="material-icons">chat</i>师生交流</a></li>
    </ul>
</div>
<main>
    <div class=" row right-content">
        <div class="container1">

            <br>
            <div class="row">
                <div class="col s12 m12">
                    <ul class="collapsible popout tm-app" data-collapsible="accordion">
                        <li style="display: block;" class="tm application model-app">
                            <div class="collapsible-header">
                                <i class="material-icons">filter_drama</i><span class="tm-name">团队申请1</span>
                                <span class="badge red new" data-badge-caption="待审核"></span>

                            </div>
                            <div class="collapsible-body">
                                <h5 class="tm-name">团队1</h5>
                                <br>
                                <span class="tm-leader">组长：刘春晓</span>
                                <br>
                                <br>
                                
								<span class="tm-member blue-text">组员：于济凡 冯凯文 朱耀华 宋晏祯 巩毅琛 王博 吴举豪</span>
                                <br>
                                <br>
                                <span class="tm-gmember purple-text">女生：刘春晓</span>
                                <br>
                                <br>

                                <br>
                                <a class="waves-effect waves-light btn app-pass">通过申请</a>
                                <a class="waves-effect waves-light btn red app-reject">驳回申请</a>
                            </div>
                        </li>
                        
                    </ul>

                </div>
                <div class="col s12 m12">
                    <ul class="collapsible popout show-tm " data-collapsible="accordion">
                        <li class="model-info">
                            <div class="collapsible-header">
                                <i class="material-icons">filter_drama</i><span class="tm-name">团队1</span>
                                <span class="badge cyan new" data-badge-caption="已审核"></span>

                            </div>
                            <div class="collapsible-body">
                                <h5 class="tm-name">团队1</h5>
                                <br>
                                <span class="tm-leader">组长：刘春晓</span>
                               
                                <br>
                                <br>
                                <span class="tm-member blue-text">组员：于济凡 冯凯文 朱耀华 宋晏祯 巩毅琛 王博 吴举豪</span>
                                <br>
                                <br>
                                <span class="tm-gmember purple-text">女生：刘春晓</span>
                                <br>
                                <br>
                                
                                <br>
                                <a class="waves-effect waves-light btn tm-edit">调整团队</a>
                                <a class="waves-effect waves-light btn red tm-del">解散团队</a>
                            </div>
                        </li>

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
<script>
$('.side-bar').addClass('hoverable');
</script>
<script type="text/javascript" src="js/tc-tm.js"></script>
</html>
