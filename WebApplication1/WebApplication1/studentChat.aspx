﻿<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="studentChat.aspx.cs" Inherits="WebApplication1.studentChat" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>客户支持页面</title>
<link rel="stylesheet" href="css/style.default.css" type="text/css" />
<script type="text/javascript" src="js/plugins/jquery-1.7.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery-ui-1.8.16.custom.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery.cookie.js"></script>
<script type="text/javascript" src="js/custom/general.js"></script>
<script type="text/javascript" src="js/custom/support.js"></script>
<!--[if IE 9]>
    <link rel="stylesheet" media="screen" href="css/style.ie9.css"/>
<![endif]-->
<!--[if IE 8]>
    <link rel="stylesheet" media="screen" href="css/style.ie8.css"/>
<![endif]-->
<!--[if lt IE 9]>
	<script src="js/plugins/css3-mediaqueries.js"></script>
<![endif]-->
    <style type="text/css">
        .auto-style1 {
            height: 19px;
        }
        .auto-style2 {
            height: 19px;
            width: 884px;
        }
        .auto-style3 {
            width: 884px;
        }
        .auto-style4 {
            width: 884px;
            height: 405px;
        }
        .auto-style5 {
            height: 405px;
        }
    </style>
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
                <a class="count" href="notifications.html"><span>9</span></a>
        	</div>
			-->
            <div class="userinfo">
            	<img src="images/thumbs/avatar.png" alt="" />
                <span>学生</span>
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
                	<h4>Wang</h4>
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
        <form runat="server">
  
        <table class="stdtable">
            <tr>
                <td class="auto-style2">简易聊天室</td>
                <td class="auto-style1">&nbsp;</td>
            </tr>
            <tr>
                <td class="auto-style4">
                    <asp:TextBox ID="contentTextBox" runat="server" Height="370px" Width="873px" ReadOnly="true" TextMode="MultiLine" style="overflow-y:hidden"></asp:TextBox>
                </td>
                <td class="auto-style5">
                    &nbsp;</td>
            </tr>
            <tr>
                <td class="auto-style3">
                    <asp:TextBox ID="messageTextBox" runat="server" Width="698px"></asp:TextBox>
                    <asp:Button ID="Button1" runat="server" Height="37px" Text="发送" Width="87px" OnClick="Button1_Click" />
                    <asp:Button ID="Button2" runat="server" Text="刷新" Width="79px" OnClick="Button2_Click" />
                </td>
                <td>&nbsp;</td>
            </tr>
        </table>
       
    </form>
  
	</div><!-- centercontent -->
</div><!--bodywrapper-->

</body>
</html>