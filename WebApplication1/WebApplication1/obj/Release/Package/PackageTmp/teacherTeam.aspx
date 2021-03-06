﻿<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="teacherTeam.aspx.cs" Inherits="WebApplication1.teacherTeam" %>

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
    <script type="text/javascript">
        function HideBlock() {
            document.getElementById("divNewBlock").style.display = "none";
            return false;
        }


        function ShowBlock() {
            var set = SetBlock();
            document.getElementById("divNewBlock").style.display = "";
            return false;
        }


        function SetBlock() {
            var top = document.body.scrollTop;
            var left = document.body.scrollLeft;
            var height = document.body.clientHeight;
            var width = document.body.clientWidth;


            if (top == 0 && left == 0 && height == 0 && width == 0) {
                top = document.documentElement.scrollTop;
                left = document.documentElement.scrollLeft;
                height = document.documentElement.clientHeight;
                width = document.documentElement.clientWidth;
            }
            return { top: top, left: left, height: height, width: width };
        }
    </script>
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

            </div>
            <!--left-->

            <div class="right">
                <!--<div class="notification">
                <a class="count" href="ajax/notifications.html"><span>9</span></a>
        	</div>-->
                <div class="userinfo">
                    <img src="images/thumbs/avatar.png" alt="" />
                    <span>管理员</span>
                </div>
                <!--userinfo-->
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

            </div>
            <!--right-->
        </div>
        <!--topheader-->



        <div class="vernav2 iconmenu">
            <ul>
                <li><a href="teacher.aspx" class="widgets">课程信息</a> </li>
                <li><a href="teacherResource.aspx" class="elements">课程资源</a></li>
                <li><a href="teacherWork.aspx" class="gallery">作业</a></li>
                <li><a href="teacherChat.aspx" class="tables">在线交流</a></li>
                <li><a href="teacherTeam.aspx" class="elements">团队</a></li>
                <li><a href="teacherPreviouscourse.aspx" class="typo">往期课程</a></li>

            </ul>
            <a class="togglemenu"></a>
            <br />
            <br />
        </div>
        <!--leftmenu-->

        <div class="centercontent">
            <div class="pageheader">
                <h1 class="pagetitle">团队</h1>
                <span class="pagedesc">查看已有团队和处理团队申请</span>

                <ul class="hornav">
                    <li class="current"><a href="#updates">已有团队</a></li>
                    <li><a href="#activities">团队申请</a></li>
                </ul>
            </div>
            <!--pageheader-->
            <div id="contentwrapper" class="contentwrapper">
                <form id="teacherTeam" runat="server" method="post">

                    <div id="updates" class="subcontent" runat="server">
                        <div id="divNewBlock" style="border: solid 5px; padding: 10px; width: 600px; z-index: 1001; position: absolute; display: none; top: 50%; left: 10%; margin: -50px; background-color: white">
                            <div style="padding: 3px 15px 3px 15px; text-align: left; vertical-align: middle;">
                                <div>
                                    <asp:Label runat="server">选择团队编号</asp:Label>
                                    <asp:DropDownList runat="server" ID="droplistTeamid"></asp:DropDownList> <br /><br /><br />
                                    <asp:Label runat="server">选择学生</asp:Label>
                                    <asp:DropDownList ID="droplist" runat="server"></asp:DropDownList>
                                </div>
                                <div>
                                    <asp:Button ID="BtnOperation" runat="server" Text="添加" OnClick="addNewMember" />

                                    <asp:Button ID="BttCancel" runat="server" Text="关闭" OnClientClick="return HideBlock();" />
                                </div>
                            </div>
                        </div>
                        <div>
                            <asp:GridView ID="GridView1" DataKeyNames="teamid" runat="server" CellPadding="4" ForeColor="Black" GridLines="Horizontal" Width="719px" AutoGenerateColumns="False" RowStyle-HorizontalAlign="Center"
                                BackColor="White" BorderColor="#CCCCCC" BorderStyle="None" BorderWidth="1px">
                                <FooterStyle BackColor="#CCCC99" ForeColor="Black" />
                                <HeaderStyle BackColor="#333333" Font-Bold="True" ForeColor="White" />
                                <PagerStyle BackColor="White" ForeColor="Black" HorizontalAlign="Right" />
                                <SelectedRowStyle BackColor="#CC3333" Font-Bold="True" ForeColor="White" />
                                <SortedAscendingCellStyle BackColor="#F7F7F7" />
                                <SortedAscendingHeaderStyle BackColor="#4B4B4B" />
                                <SortedDescendingCellStyle BackColor="#E5E5E5" />
                                <SortedDescendingHeaderStyle BackColor="#242121" />
                                <Columns>
                                    <asp:BoundField DataField="teamid" HeaderText="团队编号" />
                                    <asp:BoundField DataField="teamname" HeaderText="团队名称" />
                                    <asp:BoundField DataField="name" HeaderText="队长名字" />
                                    <asp:BoundField DataField="teammem" HeaderText="团队人数" />
                                    <%--<asp:TemplateField HeaderText ="队员调整">
                           <ItemTemplate>
                               <asp:Button ID="addBtn" runat="server" Text ="添加队员" OnClientClick ="return ShowBlock();"/>
                           </ItemTemplate>
                       </asp:TemplateField>--%>
                                </Columns>
                            </asp:GridView>
                            <asp:Button ID="addBtn" runat="server" Text="添加队员" OnClientClick="return ShowBlock();" />
                        </div>
                    </div>
                    <!-- #updates -->
                    <div id="activities" class="subcontent" style="display: none;">
                        <asp:GridView ID="GridView2" DataKeyNames="leadid" runat="server" CellPadding="4" ForeColor="Black" GridLines="Horizontal" Width="719px" AutoGenerateColumns="False" RowStyle-HorizontalAlign="Center"
                            BackColor="White" BorderColor="#CCCCCC" BorderStyle="None" BorderWidth="1px" OnRowCommand="requestSolve">
                            <FooterStyle BackColor="#CCCC99" ForeColor="Black" />
                            <HeaderStyle BackColor="#333333" Font-Bold="True" ForeColor="White" />
                            <PagerStyle BackColor="White" ForeColor="Black" HorizontalAlign="Right" />
                            <SelectedRowStyle BackColor="#CC3333" Font-Bold="True" ForeColor="White" />
                            <SortedAscendingCellStyle BackColor="#F7F7F7" />
                            <SortedAscendingHeaderStyle BackColor="#4B4B4B" />
                            <SortedDescendingCellStyle BackColor="#E5E5E5" />
                            <SortedDescendingHeaderStyle BackColor="#242121" />
                            <Columns>
                                <asp:BoundField DataField="leadid" HeaderText="队长id" />
                                <asp:BoundField DataField="name" HeaderText="队长" />
                                <asp:BoundField DataField="teamname" HeaderText="团队名称" />
                                <asp:BoundField DataField="member" HeaderText="团队成员" />
                                <asp:TemplateField HeaderText="申请处理">
                                    <ItemTemplate>
                                        <asp:Button ID="acceptBtn" runat="server" Text="同意" CommandArgument="<%# Container.DataItemIndex  %>" CommandName="accept" />
                                        <asp:Button ID="rejectBtn" runat="server" Text="驳回" CommandArgument="<%# Container.DataItemIndex  %>" CommandName="reject" />
                                    </ItemTemplate>
                                </asp:TemplateField>

                            </Columns>
                        </asp:GridView>
                    </div>
                    <!-- #activities -->
                </form>
            </div>
            <!--contentwrapper-->

            <br clear="all" />

        </div>
        <!--bodywrapper-->
</body>
</html>
