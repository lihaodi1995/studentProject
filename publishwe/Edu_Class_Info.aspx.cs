using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.IO;

public partial class Edu_Class_Info : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();

        string className = Request.QueryString["className"];
        string classCredit = Request.QueryString["classCredit"];
        string startDate = Request.QueryString["startDate"];
        string weekNumber = Request.QueryString["lastTime"];
        string classSite = Request.QueryString["classSite"];
        string teacher = Request.QueryString["teacher"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var course = from x in dc.course where x.courseID == 1 select x;
        var teac = from x in dc.teacher where x.name == teacher select x;
        if (teac.Count() == 0)
            Response.Write("222");
        else
        {
            course.First().courseName = className;
            course.First().credit = Convert.ToInt32(classCredit);
            course.First().courseTime = Convert.ToDateTime(startDate);
            course.First().weekNmuber = Convert.ToInt32(weekNumber);
            course.First().coursePlace = classSite;
            course.First().teacherID = teac.First().teacherID;
            dc.SubmitChanges();
            Response.Write("111");
        }
        Response.End();
    }
}


