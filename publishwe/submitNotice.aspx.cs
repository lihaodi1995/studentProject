using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class submitNotice : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string notice = Request.QueryString["notice"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var course = from x in dc.course where x.courseID == 1 select x;
        course.First().notice = notice;
        dc.SubmitChanges();

    }
}