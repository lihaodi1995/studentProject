using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class getWaitingCheckInformation : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string userid = Request.QueryString["userid"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.studentID.ToString() == userid select x;
        string teamId = stu.First().teamID.ToString();
        var team = from y in dc.team where y.teamID.ToString() == teamId select y;
        var teamleaderid = team.First().teamleaderID;
        var leader = from x in dc.student where x.studentID == teamleaderid select x;

        string response = "";
        response += "<tr><td>"+team.First().teamName+"</td><td>"+leader.First().name+"</td><td>"+team.First().quantity+ "</td><td>"+team.First().femaleNumber+ "</td><td><a id=\"btn\" onClick=\"javascript: showInform(" + teamId + "); \" >点击查看团队名单</a> </td></tr>";
        Response.Write(response);
    }
}