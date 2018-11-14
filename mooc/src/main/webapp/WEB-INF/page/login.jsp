<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html>
  <html>
    <head>
      <meta charset="utf-8" />
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
      <link type="text/css" rel="stylesheet" href="css/index.css"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
	<style type="text/css">
		.user {
			margin-top: 10%;
			width: 35%;
			border: solid #00BCD4;
			text-align: center;
			
		}
		.userId {
			margin-top: 5%;
		}

		.loginBtn{
			margin-bottom: 5%;
			width: 40%;
		}
	</style>
    <body>
       <div class="header">
	    <nav>
	        <div class="nav-wrapper cyan fixed">
	            <a href="#!" class="brand-logo">SEPS</a>
	            <ul class="right hide-on-med-and-down">
	            	<li><a>你好，请先登录</a></li>
	            </ul>
	        </div>
	    </nav>
	</div>
    
	  <div class="row user">
	    <form class="col s12" role="form" method="POST"
			action="/annotationTool/loginCheck">
	      <div class="row">
	        <div class="input-field col s12 userId">
	          <i class="material-icons prefix">account_circle</i>
	          <input id="icon_prefix" type="text" class="validate userName">
	          <label for="icon_prefix">学生/教师/教务 ID</label>
	        </div>
	        <div class="input-field col s12">
	          <i class="material-icons prefix">vpn_key</i>
	          <input id="icon_key" type="password" class="validate userPsd">
	          <label for="icon_key">密码</label>
	        </div>
	      </div>
	    </form>
	    <a id="log" class="waves-effect waves-light btn loginBtn cyan"><i class="material-icons right">label_outline</i>登录</a>
	  </div>
      <!--Import jQuery before materialize.js-->
      <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
      <script type="text/javascript" src="js/materialize.min.js"></script>
      <script type="text/javascript" src="js/login.js"></script>
      <script type="text/javascript" src="js/index.js"></script>
    </body>
  </html>