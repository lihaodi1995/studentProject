using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Geteveryassignment : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
       
        DataClassesDataContext dc = new DataClassesDataContext();
        var userid = Request.QueryString["taskid"];
        var team = from x in dc.assignment where x.taskid.ToString() == userid select x;


        foreach (assignment x in team)
        {
            var taskre = from y in dc.task where y.taskid.ToString() == userid select y;
            var teamre = from y in dc.team where y.teamID == x.teamID select y;
            string da = x.uploadTime.ToString();
            var d = da.Split(' ');
            
            Response.Write(teamre.First().teamName + ",");
            Response.Write(x.assignName + ",");
            Response.Write(x.teamEveryScore + ",");
            Response.Write(x.assignID + ",");
            Response.Write(d[0] + "\n");
            
        }

        Response.End();
    }
}