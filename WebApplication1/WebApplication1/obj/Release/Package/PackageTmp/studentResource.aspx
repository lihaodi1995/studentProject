<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="studentResource.aspx.cs" Inherits="WebApplication1.studentResource" %>

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
                    	<<%--li><a href="editprofile.html">编辑资料</a></li>
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
            <h1 class="pagetitle">课程资源</h1>

            
            
        </div><!--pageheader-->
        
        <div id="contentwrapper" class="contentwrapper">
                <script type="text/JavaScript">
                    function change(sender) {
                        var table = document.getElementById("GridView1");
                        for (var i = 1; i < table.rows.length; i++) {
                            table.rows[i].cells[0].getElementsById("checkBox2")[0].checked = sender.checked;
                        }
                    }
                </script><!--加上其就不会再刷新页面了-->    
	       <form runat ="server">
	          <div class="tableoptions">    
              <asp:Button ID="download" runat ="server"  CssClass ="deletebutton radius2" Text ="下载所选资源" OnClick="downLoad_Click"/>
              <asp:DropDownList ID ="resourceType" runat ="server">
                    <asp:ListItem>显示全部</asp:ListItem>
                    <asp:ListItem>课件</asp:ListItem>
                     <asp:ListItem>文档</asp:ListItem>
                     <asp:ListItem>视频</asp:ListItem>
               </asp:DropDownList>
               <asp:Button ID ="showResource" runat ="server" Text ="确定" CssClass ="radius2" OnClick="showResource_Click"/>
                </div>
               <div runat="server">
                    <asp:GridView ID="GridView1" DataKeyNames ="sourceid" runat="server" CellPadding="4"  ForeColor="Black" GridLines="Horizontal" Width="719px" AutoGenerateColumns="False" RowStyle-HorizontalAlign="Center"
                       BackColor="White" BorderColor="#CCCCCC" BorderStyle="None" BorderWidth="1px" OnRowDataBound="GridView1_RowDataBound"  >
                      <FooterStyle BackColor="#CCCC99" ForeColor="Black" />
                      <HeaderStyle BackColor="#333333" Font-Bold="True" ForeColor="White" />
                      <PagerStyle BackColor="White" ForeColor="Black" HorizontalAlign="Right" />
                      <SelectedRowStyle BackColor="#CC3333" Font-Bold="True" ForeColor="White" />
                      <SortedAscendingCellStyle BackColor="#F7F7F7" />
                      <SortedAscendingHeaderStyle BackColor="#4B4B4B" />
                      <SortedDescendingCellStyle BackColor="#E5E5E5" />
                      <SortedDescendingHeaderStyle BackColor="#242121" />
                      <Columns>
                      <asp:TemplateField >
                          <HeaderTemplate>
                              
                              <asp:CheckBox ID ="checkBox1" runat="server"  AutoPostBack ="true" OnCheckedChanged ="CheckBox_Click" />
                              <asp:Label runat="server">全选</asp:Label>
                          </HeaderTemplate>
                          <ItemTemplate>
                              <asp:CheckBox runat="server" ID ="checkBox2" />
                          </ItemTemplate>
                      </asp:TemplateField>
                      <asp:BoundField DataField="sourceid" HeaderText="资源编号" />
                      <asp:BoundField DataField="sourcename" HeaderText="资源名称" />  
                      <asp:BoundField DataField ="type" HeaderText ="资源类别" />    
                          <asp:BoundField  DataField="address" HeaderText="资源位置" ReadOnly="true" />
                      </Columns>
                  </asp:GridView>
               </div>
          </form>
                <!--	<button class="deletebutton radius3" title="table1">下载所选资源</button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <select class="radius3">
                    	<option value="">显示全部</option>
                        <option value="">课件</option>
                        <option value="">文档资料</option>
			       <option value="">视频</option>
		           <option value="">4</option>

                    </select> &nbsp;
                    <button class="radius3">确定</button>
	<div>
           <table cellpadding="0" cellspacing="0" border="0" class="stdtable stdtablecb">
                    <colgroup>
                        <col class="con0" style="width: 4%">
                        <col class="con1">
                        <col class="con0">
                        <col class="con1">
                        <col class="con0">
                        <col class="con1">
                    </colgroup>
                    <thead>
                        <tr>
                        	<th class="head0"><div class="checker" id="uniform-undefined"><span class=""><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" class="checkall" style="opacity: 0;"></span></div></span></div></th>
                            <th class="head1">标题</th>
                            <th class="head0">类型</th>
                            <th class="head1">上传时间</th>
                            <th class="head0">大小</th>
                            <th class="head1">创建者</th>
                        </tr>
                    </thead>
                   
                    <tbody>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet Explorer 4.0</td>
                            <td>Win 95+</td>
                            <td class="center">4</td>
                            <td class="center">X</td>
                        </tr>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet Explorer 5.0</td>
                            <td>Win 95+</td>
                            <td class="center">5</td>
                            <td class="center">C</td>
                        </tr>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet  Explorer 5.5</td>
                            <td>Win 95+</td>
                            <td class="center">5.5</td>
                            <td class="center">A</td>
                        </tr>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet Explorer 6</td>
                            <td>Win 98+</td>
                            <td class="center">6</td>
                            <td class="center">A</td>
                        </tr>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet Explorer 7</td>
                            <td>Win XP SP2+</td>
                            <td class="center">7</td>
                            <td class="center">A</td>
                        </tr>
                    </tbody>
                </table>
 	</div>
        
        </div>
          
            
           
            	
		 
			
        
        </div><!--contentwrapper-->-->
        
        <br clear="all" />
        
	</div><!-- centercontent -->
    
    
</div><!--bodywrapper-->

</body>
</html>

