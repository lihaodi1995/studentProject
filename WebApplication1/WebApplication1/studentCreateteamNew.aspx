<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="studentCreateteamNew.aspx.cs" Inherits="WebApplication1.studentCreateteamNew" %>

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
        <form runat="server">
        <a class="togglemenu"></a>
        <br /><br />
    </div><!--leftmenu-->
        
    <div class="centercontent">
    <ul class="hornav">
             <li class="current"><a href="#updates">创建团队</a></li>
                <li><a href="#activities">管理团队</a></li>
            </ul>
        
        
    <div id="contentwrapper" class="contentwrapper">
        
        	<div id="updates" class="subcontent">
           
		<div class="pageheader notab">
            <h1 class="pagetitle">创建团队</h1>
		<label for="studentNewteam" >团队名称</label>
		<asp:textbox runat="server" ID="teamname" ></asp:textbox>
		<asp:Button  runat="server" ID="CreateTeamButton" Text="创建团队" OnClick="CreateTeam_Click" button class="stdbtn btn_yellow"/>
		
	    </div>
		 </div>
		 <div id="activities" class="subcontent" style="display:none;">
		<div class="pageheader notab">
       <p class="pagetitle" style="font-size:18px;">团队成员</p>
                  <br /><br />
                    <asp:GridView ID="GridView1" DataKeyNames="studentid" runat="server" CellPadding="4"  ForeColor="Black" GridLines="Horizontal" Width="719px" AutoGenerateColumns="False" RowStyle-HorizontalAlign="Center"
                        BackColor="White" BorderColor="#CCCCCC" BorderStyle="None" BorderWidth="1px"  >
                      <FooterStyle BackColor="#CCCC99" ForeColor="Black" />
                      <HeaderStyle BackColor="#333333" Font-Bold="True" ForeColor="White" />
                      <PagerStyle BackColor="White" ForeColor="Black" HorizontalAlign="Right" />
                      <SelectedRowStyle BackColor="#CC3333" Font-Bold="True" ForeColor="White" />
                      <SortedAscendingCellStyle BackColor="#F7F7F7" />
                      <SortedAscendingHeaderStyle BackColor="#4B4B4B" />
                      <SortedDescendingCellStyle BackColor="#E5E5E5" />
                      <SortedDescendingHeaderStyle BackColor="#242121" />
                      <Columns>
                      <asp:BoundField DataField="name" HeaderText="姓名" />
                      <asp:BoundField DataField="studentid" HeaderText="学号" />   
                      <asp:BoundField DataField="sex" HeaderText="性别" />            
                      </Columns>
                  </asp:GridView>

	      	 <button  class="stdbtn btn_yellow">提交我的团队</button> 
		</div>
   

	<div class="pageheader notab">
            <h1 class="pagetitle">申请列表</h1>
             <asp:GridView ID="GridView2" DataKeyNames="studentid" runat="server" CellPadding="4"  ForeColor="Black" GridLines="Horizontal" Width="719px" AutoGenerateColumns="False" RowStyle-HorizontalAlign="Center"
                      OnRowCommand="GridView1_RowCommand"  BackColor="White" BorderColor="#CCCCCC" BorderStyle="None" BorderWidth="1px"  >
                      <FooterStyle BackColor="#CCCC99" ForeColor="Black" />
                      <HeaderStyle BackColor="#333333" Font-Bold="True" ForeColor="White" />
                      <PagerStyle BackColor="White" ForeColor="Black" HorizontalAlign="Right" />
                      <SelectedRowStyle BackColor="#CC3333" Font-Bold="True" ForeColor="White" />
                      <SortedAscendingCellStyle BackColor="#F7F7F7" />
                      <SortedAscendingHeaderStyle BackColor="#4B4B4B" />
                      <SortedDescendingCellStyle BackColor="#E5E5E5" />
                      <SortedDescendingHeaderStyle BackColor="#242121" />
                      <Columns>
                      <asp:BoundField DataField="name" HeaderText="姓名" />
                      <asp:BoundField DataField="studentid" HeaderText="学号" />   
                      <asp:BoundField DataField="sex" HeaderText="性别" />     
                         <asp:TemplateField ShowHeader="False">
                <ItemTemplate>
                <asp:Button ID="Button1" runat="server" CausesValidation="False"
                CommandArgument='<%# Eval("studentid") %>' Text="同意" CommandName="access" />
                </ItemTemplate>
                    </asp:TemplateField>
                         <asp:TemplateField ShowHeader="False">
                <ItemTemplate>
                <asp:Button ID="Button2" runat="server" CausesValidation="False"
                CommandArgument='<%# Eval("studentid") %>' Text="拒绝" CommandName="deny" />
                </ItemTemplate>
                    </asp:TemplateField>
                      </Columns>
                  </asp:GridView>
        
		</div>
        </div>
	</div>
	</div>
        </div><!--contentwrapper-->
         </form>
        <br clear="all" />
        
	</div><!-- centercontent -->
    
</div><!--bodywrapper-->

</body>
</html>
