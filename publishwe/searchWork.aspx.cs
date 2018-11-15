using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class searchWork : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
       DataClassesDataContext dc = new DataClassesDataContext();
        var str = Request.QueryString["searchid"];
        var result = from x in dc.task where x.taskname.Contains(str) select x;

        foreach (task x in result)
        {
            string da = x.endtime.ToString();
            var d = da.Split(' ');
            Response.Write(x.taskid + ",");
            Response.Write(x.taskname + ",");
            Response.Write(x.endtime + ",");
            Response.Write(d[0] + "\n");
        }

        Response.End();
    }
}