using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;

public partial class getCheckWaitingTeam : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        DataClassesDataContext dc = new DataClassesDataContext();
        var waitingCheckTeam = from x in dc.team where x.ifOrganized == true && x.ifChecked == false && x.ifAccepted == false select x;

        StringBuilder strBul = new StringBuilder();
        foreach (var aTeam in waitingCheckTeam)
        {
            strBul.Append("<tr>");
            strBul.Append("<td height=\"50\">" + aTeam.teamID.ToString() + "</td>");
            strBul.Append("<td height=\"50\">" + aTeam.teamName + "</td>");
            strBul.Append("<td height=\"50\">" + aTeam.teamleaderID.ToString() + "</td>");
            strBul.Append("<td height=\"50\">" + aTeam.quantity.ToString() + "</td>");
            strBul.Append("<td height=\"50\">" + aTeam.femaleNumber.ToString() + "</td>");
            strBul.Append("<td height=\"50\"><a id=\"btn\" onClick=\"javascript: showInform(" + aTeam.teamID.ToString() + "); \" >点击查看团队名单</a> </td>");
            strBul.Append("<td height=\"50\"> <a type=\"button\" onClick=\"javascript: checkpassed(" + aTeam.teamID.ToString() + ");\">通过</a> <a type =\"button\" onClick=\"javascript: checkrejected(" + aTeam.teamID.ToString() + ");\">驳回</a></td>");
            strBul.Append("<td height =\"50\">" +"</td>");

            strBul.Append("</tr>");
        }

        Response.ContentType = "text/html";
        Response.Write(strBul.ToString());
        Response.End();//这句是关键，这是因为没有关闭，所以会输出页面所有的html标签，而不只是xml文件，所以会为空
    }
}