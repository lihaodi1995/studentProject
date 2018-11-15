using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Getassignment : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        DataClassesDataContext dc = new DataClassesDataContext();
        var taskid=Request.QueryString["taskid"];
        var userid = Request.QueryString["userid"];
        var teamid = from x in dc.student where x.studentID.ToString() == userid select x.teamID;
        var result = from x in dc.task where x.taskid.ToString() == taskid select x;
        Response.Write(result.First().taskdetail + "\n");
        var assire = from x in dc.assignment where x.taskid.ToString() == taskid&&x.teamID==teamid.First() select x;
        foreach (assignment x in assire)
        {
            string da = x.uploadTime.ToString();
            var d = da.Split(' ');
            Response.Write(x.assignID + ",");
            Response.Write(x.assignName + ",");
            Response.Write(d[0] + "\n");
        }

        Response.End();
    }
}