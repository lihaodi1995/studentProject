<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs" Inherits="WebApplication1.WebForm1" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>登录页面</title>
<link rel="stylesheet" href="css/style.default.css" type="text/css" />
<script type="text/javascript" src="js/plugins/jquery-1.7.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery-ui-1.8.16.custom.min.js"></script>
<script type="text/javascript" src="js/plugins/jquery.cookie.js"></script>
<script type="text/javascript" src="js/plugins/jquery.uniform.min.js"></script>
<script type="text/javascript" src="js/custom/general.js"></script>
<script type="text/javascript" src="js/custom/index.js"></script>
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

<body class="loginpage">
	<div class="loginbox">
    	<div class="loginboxinner">
        	
            <div class="logo">
            	<h1 class="logo">在线<span>协同教学平台</span></h1>
				
            </div><!--logo-->      
            <form id="login" runat="server" method="post">
                <div >
                    <asp:Label runat="server" ID="loginLabel"  ForeColor="Red" Font-Size="Larger"></asp:Label>
                </div>
                <div class="username">
                	<div class="usernameinner">
                    	<asp:TextBox runat="server" ID="tb1"></asp:TextBox>
                    </div>
                </div>
                
                <div class="password">
                	<div class="passwordinner">
                    	<asp:TextBox runat="server" TextMode="Password" ID="pw1"></asp:TextBox>
                    </div>
                </div>
                <div class="logininbutton">
                <asp:Button  runat="server" ID="LoginButton" Text="登录" OnClick="LoginButton_Click" Width="100%"/>
                 </div>
                <div>
                    <asp:Label ID="testLabel" runat="server"></asp:Label>
                </div>
                
                <div class="keep"><input type="checkbox" /> 记住密码</div>
            
            </form>
            
        </div><!--loginboxinner-->
    </div><!--loginbox-->


</body>
</html>

