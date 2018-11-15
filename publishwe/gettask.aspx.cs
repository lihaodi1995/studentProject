using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class gettask : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        DataClassesDataContext dc = new DataClassesDataContext();
        var result = from x in dc.task select x;
        var fault = 0;
        var userid = Request.QueryString["userid"];
        var teamid = from x in dc.student where x.studentID.ToString() == userid select x.teamID;
        var assi = from x in dc.assignment where x.teamID.ToString() == teamid.First().ToString() select x;
        foreach (task x in result)
        {
            fault = 0;
            foreach(assignment k in assi)
            {
                if(k.taskid==x.taskid)
                {
                    fault = 1;
                }
            }
            string da = x.endtime.ToString();
            string ds = x.starttime.ToString();
            var d = da.Split(' ');
            var s = ds.Split(' ');
            Response.Write(x.taskid + ",");
            Response.Write(x.taskname + ",");
            if(fault==0)
            {
                Response.Write( "否,");
            }
            else
            {
                Response.Write("是,");
            }
            
            Response.Write(s[0] + ",");
            Response.Write(x.taskrate + ",");
            Response.Write(x.tasksname + ",");
            Response.Write(d[0] + "\n");
        }

        Response.End();
    }
}