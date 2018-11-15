<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="studentCourse.aspx.cs" Inherits="WebApplication1.studentCourse" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
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
            <span class="slogan">学生平台</span>
            
            
            
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
            <div class="userinfodrop">
            	<div class="avatar">
                	<a href=""><img src="images/thumbs/avatarbig.png" alt="" /></a>
                    <div class="changetheme">
                    	切换主题: <br />
                    	<a class="default"></a>
                        <a class="blueline"></a>
                        <a class="greenline"></a>
                        <a class="contrast"></a>
                        <a class="custombg"></a>
                    </div>
                </div><!--avatar-->
                <div class="userdata">
                	<h4>Juan</h4>
                    <span class="email">youremail@yourdomain.com</span>
                    <ul>
                    	<%--<li><a href="editprofile.html">编辑资料</a></li>
                        <li><a href="accountsettings.html">账号设置</a></li>
                        <li><a href="help.html">帮助</a></li>--%>
                          <li><a href="logout.aspx" >退出</a></li>
                    </ul>
                </div><!--userdata-->
            </div><!--userinfodrop-->
            
        </div><!--right-->
    </div><!--topheader-->
    
   
    
    <div class="vernav2 iconmenu">
    	<ul>
            <li><a href="studentCourse.aspx" class="widgets">课程信息</a> </li>
            <li><a href="studentResource.aspx" class="elements">下载资源</a></li>
	    <li><a href="studentCreatteam.aspx" >团队组建</a></li>
            <li><a href="studentTeam.aspx" class="gallery">我的团队</a></li>
            <li><a href="studentWork.aspx" class="tables">作业</a></li>
            <li><a href="studentChat.aspx" >在线交流</a></li>

            
        </ul>
        <a class="togglemenu"></a>
        <br /><br />
    </div><!--leftmenu-->
        
    <div class="centercontent">
    
        <div class="pageheader">
            <h1 class="pagetitle">课程信息</h1>
            <span class="pagedesc">教务信息和课程设置</span>
            
            
        </div><!--pageheader-->
        
        <div id="contentwrapper" class="contentwrapper">
        
        	
                    
	      <div>
              <table cellpadding="0" cellspacing="0" border="0" class="stdtable"  contentEditable="true">
                    <colgroup>
                        <col class="con0">
                        <col class="con1">
                        <col class="con0">
                        <col class="con1">
                        <col class="con0">
			<col class="con1">
                        <col class="con0">
                    </colgroup>
                    <thead>
                        <tr>
                            <th class="head0" >项目</th>
                            <th class="head1">值</th>
                            
                        </tr>
                    </thead>
                   
                    <tbody>
                        <tr>
                            <td>年份</td>
                            <td><asp:Label runat="server" ID="year"></asp:Label></td>
                            
                        </tr>
                        <tr>
                            <td>开始时间</td>
                            <td><asp:Label runat="server" ID="bgtime"></asp:Label></td>
                            
                        </tr>
                        <tr>
                            <td>结束时间</td>
                            <td><asp:Label runat="server" ID="edtime"></asp:Label></td>
                          
                        </tr>
                        <tr>
                            <td>团队人数上限</td>
                            <td><asp:Label runat="server" ID="memup"></asp:Label></td>
                            
                        </tr>
                        <tr>
                            <td>团队人数下限</td>
                            <td><asp:Label runat="server" ID="memdn"></asp:Label></td>
                            
                        </tr>
                    </tbody>
                </table>
		</div>
          
            
           
            	
		 
			<br></br>
            <form runat="server">
            <p class="pagetitle" style="font-size:18px;">下载教学大纲</h1>
			<asp:Button  runat="server" ID="DownloadButton" Text="下载" OnClick="DownloadButton_Click" button class="stdbtn btn_yellow"/>
       	    </form>
 
        
        </div><!--contentwrapper-->
        
        <br clear="all" />
        
	</div><!-- centercontent -->
    
    
</div><!--bodywrapper-->

</body>
</html>
