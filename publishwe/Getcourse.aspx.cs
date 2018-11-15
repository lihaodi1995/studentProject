using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Windows;

public partial class Getcourse : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        DataClassesDataContext dc = new DataClassesDataContext();
        var result = from x in dc.course select x;
        foreach (course x in result)
        {
            Response.Write(x.courseID + ",");
            Response.Write(x.courseName + ",");
            Response.Write(x.courseTime + ",");
            Response.Write(x.weekNmuber + ",");
            Response.Write(x.coursePlace + ",");
            Response.Write(x.credit + ",");
            Response.Write(x.notice + "\n");
        }
       
        Response.End();
    }
}