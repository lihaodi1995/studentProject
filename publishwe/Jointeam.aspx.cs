using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Jointeam : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        DataClassesDataContext dc = new DataClassesDataContext();
        var teamid = Request.QueryString["teamid"];
        var studentID = Request.QueryString["stuid"];
        var studentre = from x in dc.student where x.studentID.ToString() == studentID select x;
        var teamre = from x in dc.team where x.teamID.ToString() == teamid select x;
        studentre.First().teamID = Convert.ToInt32(teamid);
        studentre.First().rejectedByLeader = false;
        studentre.First().rejectedByTeacher = false;
        teamre.First().checkingList += studentre.First().name + ",";

        dc.SubmitChanges();
        
        Response.End();

    }
}