<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
	<%@page import ="java.sql.*" %>
<%@page import="com.mysql.jdbc.Driver" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>学生/老师账户设置</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/materialize-custom.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/index.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/dn-account.css" media="screen,projection">
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
        <li class="bold side-bar">
            <a href="dncourse" class="waves-effect waves-cyan"><i class="material-icons">date_range</i>课程管理</a>
        </li>
        <li class="bold side-bar active">
            <a href=""# class="waves-effect waves-cyan"><i class="material-icons">group</i>学生/教师账号</a>
        </li>
    </ul>
</header>
<main>
    <div class="container">
        <div class="col m12 ">
            <div class="card cyan lighten-5">
                <div class="card-content">
                    <span class="card-title disable">已导入的账户</span>
                    <a id="imported-account-file" href="/mooc/exportUser">xxxx.xls</a>
                    <div class="card-dividing-line"></div>
                    <span class="card-title">上传/覆盖用户账号<a href="doc/账户导入模板.xls" id="template-download">账户导入模板下载</a></span>
                    <form action="/mooc/uploadUserXls" method="post" enctype="multipart/form-data">
                        <div class="file-field input-field">
                            <div class="btn cyan">
                                <span>文件</span>
                                <input type="file" name="file">
                            </div>
                            <div class="file-path-wrapper">
                                <input class="file-path validate" type="text" placeholder="请选择上传的文件">
                            </div>
                        </div>
                        <button type="submit" class="waves-effect waves-light cyan btn">上传</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</main>
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script type="text/javascript" src="js/materialize.min.js"></script>
<script type="text/javascript" src="js/dn-account.js"></script>
</body>
</html>
