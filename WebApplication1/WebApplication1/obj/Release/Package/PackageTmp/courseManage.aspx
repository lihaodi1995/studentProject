<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="courseManage.aspx.cs" Inherits="WebApplication1.courseManage" %>

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
           		 <h1 class="pagetitle">课程信息管理</h1>
           		 
            
            
       		 </div><!--pageheader-->
    <table cellpadding="0" cellspacing="0" border="0" class="stdtable"  contentEditable="true">
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
                            <td contenteditable="false">课程名称</td>
                            <td> 
                                <asp:TextBox runat="server" ID="classNameTb"></asp:TextBox>
                            </td>
                            
                        </tr>
                        <tr>
                            <td contenteditable="false">学分</td>
                            <td>
                                 <asp:TextBox runat="server" ID="classPointTb"></asp:TextBox>
                            </td>
                            
                        </tr>
                        <tr>
                            <td contenteditable="false">上课时间</td>
                            <td>
                                 <asp:TextBox runat="server" ID="classTimeTb"></asp:TextBox>
                            </td>
                            
                        </tr>
                        <tr>
                            <td contenteditable="false">上课地点</td>
                            <td>
                                 <asp:TextBox runat="server" ID="classPlaceTb"></asp:TextBox>
                            </td>
                          
                        </tr>
                        <tr>
                            <td contenteditable="false">老师</td>
                            <td>
                                 <asp:TextBox runat="server" ID="classTeacherTb"></asp:TextBox>
                            </td>
                            
                        </tr>
                        
                    </tbody>
                </table>
       
                     <div class="courseButton">     
                      <asp:Button runat="server" Text="保存修改" ID="classSaveButton" OnClick="classSaveButton_Click"/>                	
                                     
                       </div> 
        
        <br clear="all" />

	<p class="pagetitle" style="font-size:18px;">上传学生名单</p>
        <asp:FileUpload ID="fileUpload" runat="server" />
	 <asp:Button runat="server" Text="上传" ID="uploadButton" OnClick="uploadButton_Click"/>  
	</div><!-- centercontent -->

        
</div><!--bodywrapper-->
        </form>

</body>
</html>