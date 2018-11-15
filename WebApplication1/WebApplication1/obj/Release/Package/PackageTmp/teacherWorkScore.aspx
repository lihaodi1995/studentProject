<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="teacherWorkScore.aspx.cs" Inherits="WebApplication1.teacherWorkScore" %>

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
<script>
    $('#checkall').click(function () {
        if ($(this).attr('checked')) {
            //选中了全选，下面的全勾中
            $('#scoretable').find('checkbox').attr('checked', true);
        } else {
            $('#scoretable').find('checkbox').attr('checked', false);
        }
    });
    $('#scoretable').find('checkbox').change(function () {
        if ($('#scoretable').find('checkbox').not("input:checked").size() <= 0) {
            //如果其它的复选框全部被勾选了，那么全选勾中
            $('#checkall').attr('checked', true);
        } else {
            $('#checkall').attr('checked', false);
        }
    });
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
    <form id="form1" runat="server">
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
                    	<<%--li><a href="editprofile.html">编辑资料</a></li>
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
    
   
	<div class="tableoptions">
                	<%--<button class="deletebutton radius3" title="table1">下载所选资源</button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--%>
                   
                </div>
	<div>
           <%--<table cellpadding="0" cellspacing="0" border="0" class="stdtable stdtablecb">
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
                        	<th class="head0">
			
			</th>
                            <th class="head1">团队序号</th>
                            <th class="head0">是否提交</th>
                            <th class="head1">分数</th>
                            <th class="head0">上传</th>
                         
                        </tr>
                    </thead>
                   
                    <tbody>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" class="scoretable" style="opacity: 0;"></span></div></span></div></td>
                            <td>1</td>
                            <td>是</td>
                            <td>95(点击修改)</td>
                            <td class="center">点击上传</td>
                          
                        </tr>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" class="scoretable" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet Explorer 5.0</td>
                            <td>Win 95+</td>
                            <td class="center">5</td>
                       
                        </tr>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" class="scoretable" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet  Explorer 5.5</td>
                            <td>Win 95+</td>
                            <td class="center">5.5</td>
                          
                        </tr>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" class="scoretable" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet Explorer 6</td>
                            <td>Win 98+</td>
                            <td class="center">6</td>
               
                        </tr>
                        <tr class="">
                        	<td align="center"><div class="checker" id="uniform-undefined"><span><div class="checker" id="uniform-undefined"><span class=""><input type="checkbox" class="scoretable" style="opacity: 0;"></span></div></span></div></td>
                            <td>Trident</td>
                            <td>Internet Explorer 7</td>
                            <td>Win XP SP2+</td>
                            <td class="center">7</td>
                     
                        </tr>
                    </tbody>
                </table>--%>
        <p>  
<asp:Button ID="PackDown" runat="server" Text="打包下载" OnClick="PackDown_Click"  /></p>  

 	       <asp:GridView ID="GridView1" runat="server" DataKeyNames="shwname" RowStyle-HorizontalAlign="Center" BackColor="White" BorderColor="#CCCCCC" BorderStyle="None" BorderWidth="1px" CellPadding="4" ForeColor="Black" GridLines="Horizontal" AutoGenerateColumns="False" Width="707px" OnRowCommand="GridView1_RowCommand" OnRowCancelingEdit="GridView1_RowCancelingEdit" OnRowEditing="GridView1_RowEditing" OnRowUpdating="GridView1_RowUpdating" OnRowDataBound="GridView1_RowDataBound">
               <FooterStyle BackColor="#CCCC99" ForeColor="Black" />
               <HeaderStyle BackColor="#333333" Font-Bold="True" ForeColor="White" />
               <PagerStyle BackColor="White" ForeColor="Black" HorizontalAlign="Right" />

<RowStyle HorizontalAlign="Center"></RowStyle>

               <SelectedRowStyle BackColor="#CC3333" Font-Bold="True" ForeColor="White" />
               <SortedAscendingCellStyle BackColor="#F7F7F7" />
               <SortedAscendingHeaderStyle BackColor="#4B4B4B" />
               <SortedDescendingCellStyle BackColor="#E5E5E5" />
               <SortedDescendingHeaderStyle BackColor="#242121" />
                
                <Columns>
                    <asp:TemplateField HeaderText="选择">
     <ItemTemplate>
           <asp:CheckBox ID="ChkItem" runat="server" />
     </ItemTemplate>
     <ItemStyle HorizontalAlign="Center" VerticalAlign="Middle" Width="100px" />
</asp:TemplateField>

                      <asp:BoundField DataField="teamid" HeaderText="团队序号" ReadOnly="true" />    
                    <asp:BoundField DataField="shwname" HeaderText="作业名称" ReadOnly="true"/>
                    <asp:BoundField  DataField="shwgrade" HeaderText="作业成绩"/>
                    <asp:BoundField  DataField="shwaddress" HeaderText="资源位置" ReadOnly="true" />
                    <asp:CommandField EditText="修改成绩" ShowEditButton="True" />
                    
                      <asp:TemplateField ShowHeader="False">
                <ItemTemplate>
                <asp:Button ID="Button1" runat="server" CausesValidation="False"
                CommandArgument='<%# Eval("shwaddress") %>' Text="下载" CommandName="download" />
                </ItemTemplate>
                    </asp:TemplateField>
                  </Columns>
                

           </asp:GridView>
 	</div>
        
        </div>
        
        <br clear="all" />
        
	</div><!-- centercontent -->
    
    
</div><!--bodywrapper-->

    </form>

</body>
</html>