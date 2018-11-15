<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="teacherChat.aspx.cs" Inherits="WebApplication1.teacherChat" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
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
            width: 1052px;
        }
        .auto-style2 {
            width: 964px;
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
                <span>管理员</span>
            </div><!--userinfo-->
            
            <div class="userinfodrop">            	<div class="avatar">
                	<a href=""><img src="images/thumbs/avatarbig.png" alt="" /></a>
                    <div class="changetheme">
                    	Change theme: <br />
                    	<a class="default"></a>
                        <a class="blueline"></a>
                        <a class="greenline"></a>
                        <a class="contrast"></a>
                        <a class="custombg"></a>
                    </div>
                </div><!--avatar-->
<div class="userdata">
                	<h4>管理员</h4>
                    <span class="email">youremail@yourdomain.com</span>
                    <ul>
                    	<%--<li><a href="editprofile.html">Edit Profile</a></li>
                        <li><a href="accountsettings.html">Account Settings</a></li>
                        <li><a href="help.html">Help</a></li>--%>
                        <li><a href="teacherlogout.aspx" >退出</a></li>
                    </ul>
                </div><!--userdata-->
            </div><!--userinfodrop-->
        </div><!--right-->
    </div><!--topheader-->
    
    
    
    <div class="vernav2 iconmenu">
    	<ul>
             <li><a href="teacher.aspx" class="widgets">课程信息</a> </li>
            <li><a href="teacherResource.aspx" class="elements">课程资源</a></li>
            <li><a href="teacherWork.aspx" class="gallery">作业</a></li>
            <li><a href="teacherChat.aspx" >在线交流</a></li>
            <li><a href="teacherTeam.aspx" >团队</a></li>
            <li><a href="teacherPreviouscourse.aspx" class="typo">往期课程</a></li>
        </ul>
        <a class="togglemenu"></a>
        <br /><br />
    </div><!--leftmenu-->
   <form runat="server">
    <div class="centercontent">
        
     <table class="stdtable">
            <tr>
                <td class="auto-style2">简易聊天室</td>
                <td class="auto-style1">&nbsp;</td>
            </tr>
            <tr>
                <td class="auto-style2">
                    <asp:TextBox ID="contentTextBox" runat="server" Height="370px" Width="873px" ReadOnly="true" TextMode="MultiLine" style="overflow-y:hidden"></asp:TextBox>
                </td>
                <td class="auto-style5">
                    &nbsp;</td>
            </tr>
            <tr>
                <td class="auto-style2">
                    <asp:TextBox ID="messageTextBox" runat="server" Width="698px"></asp:TextBox>
                    <asp:Button ID="Button1" runat="server" Height="37px" Text="发送" Width="93px" OnClick="Button1_Click" />
                    <asp:Button ID="Button2" runat="server" OnClick="Button2_Click" Text="刷新" />
                </td>
                <td>&nbsp;</td>
            </tr>
        </table>
        
        
    
</div>
  </form>
	</div><!-- centercontent -->
    
    
</div><!--bodywrapper-->

</body>
</html>
