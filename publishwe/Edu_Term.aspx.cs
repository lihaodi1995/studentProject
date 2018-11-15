using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Edu_term : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();

        string first = Request.QueryString["first"];
        string second = Request.QueryString["second"];
        string third = Request.QueryString["third"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var semester = from x in dc.semester where x.id == 1 select x;
        semester.First().startTime = Convert.ToDateTime(first + " 00:00:00");
        semester.First().endTime = Convert.ToDateTime(second + " 23:59:59");
        semester.First().weekNumber = Convert.ToInt32(third);
        dc.SubmitChanges();
        Response.Write(first);
        Response.End();
    }
}