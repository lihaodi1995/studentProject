<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="termManage.aspx.cs" Inherits="WebApplication1.termManage" %>

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
    <form runat="server">
<div class="bodywrapper">
    <div class="topheader">
        <div class="left">
            <h1 class="logo">在线.<span>协同教学平台</span></h1>
            <span class="slogan">教务人员系统</span>
            
  
            
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
                        <li><a href="WebForm1.aspx">退出</a></li>
                    </ul>
                </div><!--userdata-->
            </div><!--userinfodrop-->
        </div><!--right-->
    </div><!--topheader-->
    
      
        

    <div class="vernav2 iconmenu">
    	<ul>
        	
            <!--<li><a href="filemanager.html" class="gallery">学期管理</a></li>-->
            <li><a href="termManage.aspx" class="elements">学期管理</a></li>
            <li><a href="courseManage.aspx" class="widgets">课程管理</a></li>
        </ul>
        <a class="togglemenu"></a>
        <br /><br />
    </div><!--leftmenu-->
        
    <div class="centercontent">
    
       <div class="pageheader">
            <h1 class="pagetitle">今天是
            <script type="text/javascript">
                var today = new Date(); 
                var date = today.getDate();
                var day = today.getDay();
                var month = today.getMonth()+1;
                var year = today.getFullYear();
                document.write(year + "年" + month + "月" + date + "日<br />");
            </script>
            </h1>
            <p class="pagedesc">本周为2017年春季学期第19周</p>
            
            
        </div><!--pageheader-->
    <br></br>
    <br></br>
    <br></br>
    <h1 class="pagetitle" style="font-size:26px;">学期信息管理</h1>
    <table cellpadding="0" cellspacing="0" border="0" class="stdtable"  contentEditable="true" id="terminfo">
                    <colgroup>
                        <col class="con0">
                        <col class="con1">
                        <col class="con0">
                        <col class="con1">
                        <col class="con0">
                    </colgroup>
                    <thead>
                        <tr>
                            <th class="head0" contenteditable="false">项目</th>
                            <th class="head1" contenteditable="false">值</th>
                            
                        </tr>
                    </thead>
                   
                    <tbody>
                        <tr>
                            <td contenteditable="false">年份</td>
                            <td>
                                <asp:TextBox runat="server" ID="yearTb"></asp:TextBox>
                            </td>
                            
                        </tr>
                        <tr>
                            <td contenteditable="false">开始时间</td>
                            <td>
                               <asp:TextBox runat="server" ID="termStartTb"></asp:TextBox>
                            </td>
                            
                        </tr>
                        <tr>
                            <td contenteditable="false">结束时间</td>
                            <td>
                                <asp:TextBox runat="server" ID="termEndTb"></asp:TextBox>
                            </td>
                          
                        </tr>
                        <tr>
                            <td contenteditable="false">周次</td>
                            <td>
                                <asp:TextBox runat="server" ID="termWeekTb"></asp:TextBox>
                            </td>
                            
                        </tr>
                        
                    </tbody>
                </table>
             
            

           <div class="courseButton">     
                      <asp:Button runat="server" class="stdbtn btn_orange" Text="开始学期" ID="startTermButton" OnClick="startTermButton_Click"/>                  	
                      <asp:Button runat="server" class="stdbtn btn_orange" Text="结束学期" ID="endTermButton" OnClick="endTermButton_Click"/>  
           </div><!--courseBeginButton-->              	
                                     
                               
          
        <br clear="all" />
        
	</div><!-- centercontent -->
    
    
</div><!--bodywrapper-->
        </form>

</body>
</html>

