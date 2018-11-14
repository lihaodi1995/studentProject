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
        <li id="grade" class="side-bar baractive"><a class="waves-effect waves-teal" href="tc-mk"><i class="material-icons">spellcheck</i>成绩登记</a></li>
        <li id="signin" class="side-bar"><a class="waves-effect waves-teal" href="tc-ci"><i class="material-icons">assessment</i>签到统计</a></li>
        <li id="olddata" class="side-bar"><a class="waves-effect waves-teal" href="tc-od"><i class="material-icons">find_replace</i>以往数据</a></li>
        <li id="communication" class="side-bar"><a class="waves-effect waves-teal" href="http://kevinfeng.moe/chatroom.php?stuID=<%=tid %>"><i class="material-icons">chat</i>师生交流</a></li>
    </ul>
</div>
<main>
    <div class=" row right-content">
        <div class="toolbox">
            <a class="waves-effect waves-light btn down-temp" href="exportGradeTemplate">下载打分模板</a>
            <a class="waves-effect waves-light btn " href="#modal1">上传批量打分</a>
            <!--<a class="waves-effect waves-light btn right red grade-edit">提交修改</a>-->
            <a class="waves-effect waves-light btn right down-grade" href="exportGrade">下载成绩单</a>

        </div>

        <div id="modal1" class="modal">
            <div class="modal-content">
                <form action="/mooc/uploadGradeXls" method="post" enctype="multipart/form-data">
                    <div class="file-field input-field">
                        <h5>上传填写好的模板</h5>
                        <br>
                        <div class="btn">
                            <span>文件</span>
                            <input type="file" name="file">
                        </div>
                        <div class="file-path-wrapper">
                            <input class="file-path validate" type="text">
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat up-temp" onclick="document.forms[0].submit()">上传</a>
                <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat">取消</a>

            </div>
        </div>

        <div class="stu-tbl">
            <table class="striped">
                <thead>
                <tr>
                    <th>编号</th>
                    <th>名字</th>
                    <th>已给分数</th>
                    <th>修改分数</th>
                    <th></th>
                </tr>
                </thead>

                <tbody>

                </tbody>
            </table>
        </div>
    </div>
</main>

<!--Import jQuery before materialize.js-->

</body>

<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script type="text/javascript" src="js/materialize.min.js"></script>
<script type="text/javascript" src="js/index.js"></script>
<script type="text/javascript" src="js/tc-mk.js"></script>

</html>
