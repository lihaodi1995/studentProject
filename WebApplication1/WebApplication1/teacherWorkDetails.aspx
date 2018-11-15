<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="teacherWorkDetails.aspx.cs" Inherits="WebApplication1.teacherWorkDetails" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>控制台页面</title>
<link rel="stylesheet" href="css/style.default.css" type="text/css" />
<script type="text/javascript" src="js/plugins/jquery-1.7.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery-ui-1.8.16.custom.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery.cookie.js"></script>
<script type="text/javascript" src="js/plugins/jquery.uniform.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery.flot.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery.flot.resize.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery.slimscroll.js"></script>
<script type="text/javascript" src="js/custom/general.js"></script>
<script type="text/javascript" src="js/custom/dashboard.js"></script>
<!--[if lte IE 8]><script language="javascript" type="text/javascript" src="js/plugins/excanvas.min.js"></script><![endif]-->
<!--[if IE 9]>
    <link rel="stylesheet" media="screen" href="css/style.ie9.css"/>
<![endif]-->
<!--[if IE 8]>
    <link rel="stylesheet" media="screen" href="css/style.ie8.css"/>
<![endif]-->
<!--[if lt IE 9]>
	<script src="js/plugins/css3-mediaqueries.js"></script>
<![endif]-->
</head>

<body class="withvernav">
<div class="bodywrapper">
    <div class="topheader">
        <div class="left">
            <h1 class="logo">在线<span>协同教学平台</span></h1>
            <span class="slogan">后台管理系统</span>
            
            
            
            <br clear="all" />
            
        </div><!--left-->
        
        <div class="right">
        	<!--<div class="notification">
                <a class="count" href="ajax/notifications.html"><span>9</span></a>
        	</div>-->
            <div class="userinfo">
            	<img src="images/thumbs/avatar.png" alt="" />
                <span>管理员</span>
            </div><!--userinfo-->
            
            
        </div><!--right-->
    </div><!--topheader-->
    
   
    
    <div class="vernav2 iconmenu">
    	<ul>
            <li><a href="teacher.aspx" class="widgets">课程信息</a> </li>
            <li><a href="teacherResource.aspx" class="elements">课程资源</a></li>
            <li><a href="teacherWork.aspx" class="gallery">作业</a></li>
            <li><a href="4.html" class="tables>在线交流</a></li>
            <li><a href="5.html" >团队</a></li>
            <li><a href="6.html" class="typo">往期课程</a></li>
            
        </ul>
        <a class="togglemenu"></a>
        <br /><br />
    </div><!--leftmenu-->
       
    <div class="centercontent">
    
   <div class="pageheader">
            <h1 class="pagetitle">修改学生作业</h1>
            <span class="pagedesc">编辑作业信息</span>
            
            
        </div><!--pageheader-->
		
		<div class="workdetail">
		<div class="statusbox" style="width:70%;">
                        <form id="poststatus" action="ajax/newsfeed/status.php" method="post">
		<label for="male">标题</label>
		<input type="text"  id="teacherWorkTitle" class="width100"/><br/><br/>
	
		<label for="female">开始时间</label>
		<input type="text" " id="teacherWorkBegintime"class="width100" /><br/><br/>

		<label for="female">截止时间</label>
		<input type="text"  id="teacherWorkEndtime" class="width100"/><br/><br/>
                            <p>作业要求</p>
                            <div class="status_content">
				<div class="workdetailinput">
                                <textarea name="" cols="5" rows="20" id="statustext" ></textarea>
				</div>       
			
                            </div>
                 <div class="submit" style="float:left;"><button class="stdbtn btn_yellow">发布</button>
		<button class="stdbtn btn_yellow">删除</button>
		<button onclick="window.location.href='teacherWork.html'" class="stdbtn btn_yellow">取消</button></div>
                        </form>
                    </div>
        </div>

        
        <br clear="all" />
        
	</div><!-- centercontent -->
    
    
</div><!--bodywrapper-->

</body>
</html>
