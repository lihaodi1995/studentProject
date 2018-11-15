<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="teacherNewWork.aspx.cs" Inherits="WebApplication1.teacherNewWork" %>

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
    <script type="text/javascript" src="My97DatePicker/WdatePicker.js"></script>
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
                        <a href="">
                            <img src="images/thumbs/avatarbig.png" alt="" /></a>
                        <div class="changetheme">
                            切换主题:
                            <br />
                            <a class="default"></a>
                            <a class="blueline"></a>
                            <a class="greenline"></a>
                            <a class="contrast"></a>
                            <a class="custombg"></a>
                        </div>
                    </div>
                    <!--avatar-->
                    <div class="userdata">
                        <h4>Juan</h4>
                        <span class="email">youremail@yourdomain.com</span>
                        <ul>
                            <%--<li><a href="editprofile.html">编辑资料</a></li>
                        <li><a href="accountsettings.html">账号设置</a></li>
                        <li><a href="help.html">帮助</a></li>--%>
                            <li><a href="teacherlogout.aspx">退出</a></li>
                        </ul>
                    </div>
                    <!--userdata-->
                </div>
                <!--userinfodrop-->
            </div>
            <!--right-->
        </div>
        <!--topheader-->



        <div class="vernav2 iconmenu">
            <ul>
                <li><a href="teacher.aspx" class="widgets">课程信息</a> </li>
                <li><a href="teacherResource.aspx" class="elements">课程资源</a></li>
                <li><a href="teacherWork.aspx" class="gallery">作业</a></li>
                <li><a href="teacherWork" class="tables">在线交流</a></li>
                <li><a href="teacherTeam.aspx">团队</a></li>
            <li><a href="teacherPreviouscourse.aspx" class="typo">往期课程</a></li>

            </ul>
            <a class="togglemenu"></a>
            <br />
            <br />
        </div>
        <!--leftmenu-->

        <div class="centercontent">

            <div class="pageheader">
                <h1 class="pagetitle">发布学生作业</h1>
                <span class="pagedesc">编辑作业信息</span>


            </div>
            <!--pageheader-->

            <div class="workdetail">
                <div class="statusbox" style="width: 70%;">
                        <form id="poststatus" method="post" runat="server">
                        <asp:Label runat="server">标题</asp:Label>
                        <asp:TextBox ID="hwTitle" runat="server"></asp:TextBox>
                        <br />
                        <br />
                         <asp:Label runat="server">开始时间</asp:Label>
                         <input type="text" id="hwBegintime" onfocus="WdatePicker({dateFmt:'yyyy-MM-dd HH:mm:ss'})" class="text" runat ="server" />
                        <br />
                        <br />
                        <asp:Label runat="server">结束时间</asp:Label>
                        <input type="text" id="hwEndtime" onfocus="WdatePicker({dateFmt:'yyyy-MM-dd HH:mm:ss'})" class="text" runat ="server" />
                        <br />
                         <br />
                        <asp:Label runat="server">提交次数</asp:Label>
                        <asp:TextBox ID="hwTimes" runat="server"></asp:TextBox><br />
                        <br />
                        <asp:Label runat="server">占分比例</asp:Label>
                        <asp:TextBox ID="hwParts" runat="server"></asp:TextBox><br />
                        <br />
                        <p>作业要求</p>
                        <div class="status_content">
                            <div class="workdetailinput">
                                <textarea name="" cols="5" rows="20" id="statustext" runat="server"></textarea>
                            </div>

                        </div>
                        <div style="float: left;">
                            <asp:Button ID="hwRelease" CssClass="stdbtn btn_yellow" runat="server" OnClick="hwRelease_Click" Text="发布" />
                            <asp:Button runat="server" OnClick="cancleBtn_Click" Text="取消" />
                            <!-- <button onclick="window.location.href='teacherWork.aspx'" runat ="server">取消</button>-->
                        </div>
                    </form>
                </div>
            </div>


            <br clear="all" />

        </div>
        <!-- centercontent -->


    </div>
    <!--bodywrapper-->

</body>
</html>
