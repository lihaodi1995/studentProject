using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class checkRejected : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string teamID = Request.QueryString["teamID"];
        string rejectingReason = Request.QueryString["rejectingReason"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var team = from x in dc.team where x.teamID == Convert.ToInt32(teamID) select x;
        var ateam = dc.team.Single(p => p.teamID == Convert.ToInt32(teamID));
        var stu = from x in dc.student where x.teamID.ToString() == teamID select x;
        
        foreach(var y in stu)
        {
            y.excuseByTeacher = rejectingReason;
        }
       
        ateam.ifChecked = true;
        ateam.rejectingReason = rejectingReason;
        string stdList = team.First().teamMember;
        string[] sArray = stdList.Split(',');
        foreach(var Aname in sArray)
        {
            if (Aname != "")
            {
                var std = from x in dc.student where x.name == Aname select x;
                std.First().rejectedByTeacher = true;
                std.First().teamID = 0;
            }
        }
        dc.SubmitChanges();
    }
}