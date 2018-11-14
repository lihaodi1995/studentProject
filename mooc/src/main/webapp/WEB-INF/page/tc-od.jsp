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
        <li id="signin" class="side-bar"><a class="waves-effect waves-teal" href="tc-ci"><i class="material-icons">assessment</i>签到统计</a></li>
        <li id="olddata" class="side-bar baractive"><a class="waves-effect waves-teal" href="tc-od"><i class="material-icons">find_replace</i>以往数据</a></li>
        <li id="communication" class="side-bar"><a class="waves-effect waves-teal" href="http://kevinfeng.moe/chatroom.php?stuID=<%=tid %>"><i class="material-icons">chat</i>师生交流</a></li>
    </ul>
</div>
<main>
    <div class=" row right-content">
        <div class="olddata">
            <div class="row">
                <div class="col s10 m10 offset-m1">
                    <div class="card white darken-1 hoverable year">
                        <div class="card-content black-text">
                            <span class="card-title">2016年软件工程实践</span>
                            <p>
                                课程简介：“软件工程”是介绍软件开发方法，提高学生软件开发能力的一门重要的专业课程。本教程主要以工程化的软件开发方法为主导，系统、全面地介绍这门课程的原理、方法及应用。
                                《软件工程与实践》适合作为高职高专院校计算机或信息类专业的教材，还可作为系统设计人员、程序员、软件架构人员、业务和系统分析人员、项目经理等软件工程技术人员，以及准备参加全国软件工程课程自学考试的读者的参考书。
                            </p>
                            <br/>
                            <p>
                                任课教师：林广艳、贾经冬
                            </p>
                            <br/>
                            <p>
                                教室：工程训练中心302
                            </p>
                            <br/>
                            <p>学分：2</p>
                            <br/>

                            <p>学生人数：144</p>
                            <br/>
                            <p>开课时间：6/24-7/5</p>
                            <br/>
                            <p class="show-dagang">
                                教学大纲：《软件工程与实践》适合作为高职高专院校计算机或信息类专业的教材，还可作为系统设计人员、程序员、软件架构人员、业务和系统分析人员、项目经理等软件工程技术人员，以及准备参加全国软件工程课程自学考试的读者的参考书。

                            </p>                        </div>
                        <div class="card-action">
                            <a id="down1" class="down" href="downOld?id=1">下载资源文件</a>
                            <a id="down2" class="down" href="downOld?id=2">下载作业文件</a>
                        </div>
                    </div>
                </div>
                <div class="col s10 m10 offset-m1">
                    <div class="card white darken-1 hoverable year">
                        <div class="card-content black-text">
                            <span class="card-title">2015软件工程实践</span>
                            <p>
                                课程简介：“软件工程”是介绍软件开发方法，提高学生软件开发能力的一门重要的专业课程。本教程主要以工程化的软件开发方法为主导，系统、全面地介绍这门课程的原理、方法及应用。
                                《软件工程与实践》适合作为高职高专院校计算机或信息类专业的教材，还可作为系统设计人员、程序员、软件架构人员、业务和系统分析人员、项目经理等软件工程技术人员，以及准备参加全国软件工程课程自学考试的读者的参考书。
                            </p>
                            <br/>
                            <p>
                                任课教师：林广艳、贾经冬
                            </p>
                            <br/>
                            <p>
                                教室：工程训练中心302
                            </p>
                            <br/>
                            <p>学分：2</p>
                            <br/>

                            <p>学生人数：144</p>
                            <br/>
                            <p>开课时间：6/24-7/5</p>
                            <br/>
                            <p class="show-dagang">
                                教学大纲：《软件工程与实践》适合作为高职高专院校计算机或信息类专业的教材，还可作为系统设计人员、程序员、软件架构人员、业务和系统分析人员、项目经理等软件工程技术人员，以及准备参加全国软件工程课程自学考试的读者的参考书。

                            </p></div>
                        <div class="card-action">
                            <a id="down3" class="down" href="downOld?id=3">下载资源文件</a>
                            <a id="down4" class="down" href="downOld?id=4">下载作业文件</a>
                        </div>
                    </div>
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
<script type="text/javascript" src="js/down.js"></script>

</html>
