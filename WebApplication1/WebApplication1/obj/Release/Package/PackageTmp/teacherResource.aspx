﻿
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="teacherResource.aspx.cs" Inherits="WebApplication1.teacherResource" %>
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
        
    <div class="centercontent">
    
       
        <div id="contentwrapper" class="contentwrapper">
        
             
      
            
      
<br/><br/>
			<p class="pagetitle" style="font-size:18px;">上传教学资源</p>
       		
              <form id="uploader" runat="server">
                 <asp:FileUpload ID="resourceUpload" runat="server"  />
                  <br />
                  <asp:Label runat="server">选择上传类别</asp:Label>
                  <asp:DropDownList ID ="resourceType" runat="server" >
                      <asp:ListItem>课件</asp:ListItem>
                      <asp:ListItem>文档</asp:ListItem>
                      <asp:ListItem>视频</asp:ListItem>
                  </asp:DropDownList>
                 <asp:Button ID="recourceBtn" OnClick="resourceBtn_Click" runat="server"   Text="上传"/>
                  <br /><br />
                   <asp:GridView ID="GridView1" DataKeyNames="sourceid" runat="server" CellPadding="4"  ForeColor="Black" GridLines="Horizontal" Width="719px" AutoGenerateColumns="False" RowStyle-HorizontalAlign="Center"
                       OnRowDeleting="GridView1_RowDeleting" BackColor="White" BorderColor="#CCCCCC" BorderStyle="None" BorderWidth="1px" OnRowDataBound="GridView1_RowDataBound"  >
                      <FooterStyle BackColor="#CCCC99" ForeColor="Black" />
                      <HeaderStyle BackColor="#333333" Font-Bold="True" ForeColor="White" />
                      <PagerStyle BackColor="White" ForeColor="Black" HorizontalAlign="Right" />
                      <SelectedRowStyle BackColor="#CC3333" Font-Bold="True" ForeColor="White" />
                      <SortedAscendingCellStyle BackColor="#F7F7F7" />
                      <SortedAscendingHeaderStyle BackColor="#4B4B4B" />
                      <SortedDescendingCellStyle BackColor="#E5E5E5" />
                      <SortedDescendingHeaderStyle BackColor="#242121" />
                      <Columns>
                          <asp:BoundField HeaderText="序号" >  
    <ItemStyle HorizontalAlign="Center" />  
    <HeaderStyle HorizontalAlign="Center" Width="30px" />  
</asp:BoundField> 
                          <asp:BoundField DataField="sourceid" HeaderText="资源序号" />   
                      <asp:BoundField DataField="sourcename" HeaderText="资源名称" />   
                      <asp:CommandField ShowDeleteButton="True" />             
                      </Columns>
                  </asp:GridView>
             </form>
            </div><!-- #activities -->
        
        </div><!--contentwrapper-->
        <br clear="all" />
        
	</div><!-- centercontent -->
    
    
</div><!--bodywrapper-->

</body>
</html>
