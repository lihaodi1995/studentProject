using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class _Default : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string courseTime = Request.QueryString["courseTime"];

        string coursePlace = Request.QueryString["coursePlace"];

        DataClassesDataContext dc = new DataClassesDataContext();
        var course = dc.course.Single(p => p.courseID == 1);
        course.courseTime = Convert.ToDateTime(courseTime);
        course.coursePlace = coursePlace;
        dc.SubmitChanges();

        var course1 = from x in dc.course where x.courseID == 1 select x;
       


    }
} 