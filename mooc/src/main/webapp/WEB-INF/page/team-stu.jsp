<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>团队管理</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="css/materialize.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/materialize-custom.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/team-stu.css" media="screen,projection">
    <link type="text/css" rel="stylesheet" href="css/index.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<%String name = request.getSession().getAttribute("sessionusername").toString();%>
<%String id= request.getSession().getAttribute("sessionuserid").toString();%>
</head>
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
        <li class="bold side-bar active">
            <a href="team-stu" class="waves-effect waves-cyan"><i class="material-icons">group</i>团队</a>
        </li>
        <li class="bold side-bar">
            <a href="resource" class="waves-effect waves-cyan"><i class="material-icons">theaters</i>资源</a>
        </li>
        <li class="bold side-bar">
            <a href="homework-stu" class="waves-effect waves-cyan"><i class="material-icons">description</i>作业</a>
        </li>
        <li class="bold side-bar">
            <a href="http://kevinfeng.moe/chatroom.php?stuID=<%=id %>" class="waves-effect waves-cyan"><i class="material-icons">chat</i>交流</a>
        </li>
    </ul>
</header>
<main>
    <div class="container" id="team-choose">
        <div class="row">
            <div class="card col offset-m1 m5">
                <div class="card-image waves-effect waves-block waves-light">
                    <img class="activator" src="img/team-leader.JPG">
                </div>
                <div class="card-content">
                    <span class="card-title activator grey-text text-darken-4">我要当组长！<i class="material-icons right">more_vert</i> </span>
                </div>
                <div class="card-reveal">
                    <span class="card-title grey-text text-darken-4">我要当组长！<i class="material-icons right">close</i></span>
                    <p>请确认是否要成为<strong class="color-red">团队负责人</strong>,本次选择之后将不可更改,如果选择错误请联系老师进行更改</p>
                    <a class="waves-effect waves-light cyan btn" href="#create-team">确认</a>
                </div>
            </div>
            <div class="card col offset-m1 m5">
                <div class="card-image waves-effect waves-block waves-light">
                    <img class="activator" src="img/team-member.jpg">
                </div>
                <div class="card-content">
                    <span class="card-title activator grey-text text-darken-4">我要当组员<i class="material-icons right">more_vert</i> </span>
                </div>
                <div class="card-reveal">
                    <span class="card-title grey-text text-darken-4">我要当组员<i
                            class="material-icons right">close</i></span>
                    <p>请确认是否要成为<strong class="color-red">团队组员</strong>,本次选择之后将不可更改,如果选择错误请联系老师进行更改</p>
                    <a id="find-team-confirm" class="waves-effect waves-light cyan btn" href="#find-team">确认</a>
                </div>
            </div>
        </div>
    </div>
    <div class="container" id="team-manage">
        <div class="row">
            <h1 id="team-manage-name" class="col m12 s12">RUA</h1><!--队名-->
            <div class="col m12 opacity team-info-mng z-depth-1">
                <h4>团队信息</h4>
                <p id="team-manage-info"></p>
                <h4>待审批</h4>
                <ul id="team-manage-app" class="collection">
                    <li class="collection-item"><div><span class="appStuName"></span><span class="appStuID"></span> <a class="secondary-content waves-effect waves-light red z-depth-1 disagree"></a><a class="secondary-content waves-effect waves-light cyan z-depth-1 agree"></a></div></li>
                </ul>
                <h4>队员信息</h4>
                <ul id="team-manage-mem" class="collection" id="teamMem">
                    <li class="collection-item"><span class="memName"></span><span class="memStuID"></span></li>
                </ul>
                <button type="submit" id="submit-team-apply" class="cyan waves-effect waves-light btn" onclick="teamManageSubmit()">提交团队申请</button>
                <button id="set-team-manage-score"class="waves-effect waves-light cyan btn" onclick="revealTeamScore()">为团队成员打分</button>
            </div>
        </div>
    </div>
    <div class="container" id="team-check">
        <div class="row">
            <h1 id="team-check-name" class="col m12 s12"></h1><!--队名-->
            <div class="col m12 opacity team-info-mng z-depth-1">
                <h4>团队信息</h4>
                <p id="team-check-info"></p>
                <h4>队员信息</h4>
                <ul id="team-check-mem" class="collection">
                    <li class="collection-item"></li>
                    <li class="collection-item"></li>
                </ul>
                <button id="set-team-score"class="waves-effect waves-light cyan btn" onclick="revealTeamScore()">为团队成员打分</button>
            </div>
        </div>
    </div>
</main>
<!--modal-->
<div id="create-team" class="modal">
    <form class="modal-content">
        <div class="input-field">
            <input placeholder="请输入团队名称" type="text" class="validate" id="teamname">
            <label for="teamname">团队名称</label>
        </div>
        <div class="input-field">
            <textarea placeholder="请输入团队信息" type="text" class="materialize-textarea" id="teaminfo"></textarea>
            <label for="teaminfo">团队信息</label>
        </div>
        <a href="#" type="submit" class="cyan waves-effect waves-light btn" onclick="teamCreate()">确认</a>
    </form>
</div>
<div id="find-team" class="modal">
    <div class="modal-content">
        
    </div>
</div>
<div id="team-score" class="modal">
    <div class="modal-content">
        <div class="label">为团队成员贡献度打分</div>
        <ul id="team-score-list" class="collection">

        </ul>
        <!--<button type="submit" id="set-team-score-btn" class="waves-effect waves-light cyan btn" onclick="setTeamScore()">确认</button>-->
        <button type="submit" id="set-team-score-btn" class="waves-effect waves-light cyan btn" onclick="setTeamScore()">确认</button>
    </div>
</div>
<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script type="text/javascript" src="js/materialize.min.js"></script>
<script type="text/javascript" src="js/team-stu.js"></script>
<script>

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
</script>
</body>
</html>
