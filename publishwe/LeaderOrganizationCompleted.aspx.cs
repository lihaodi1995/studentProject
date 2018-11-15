using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class LeaderOrganizationCompleted : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string studentID = Request.QueryString["userid"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.studentID == Convert.ToInt32(studentID) select x;
        string teamID = stu.First().teamID.ToString();
        var team = from x in dc.team where x.teamID == Convert.ToInt32(teamID) select x;
        team.First().ifOrganized = true;
        dc.SubmitChanges();

    }
}