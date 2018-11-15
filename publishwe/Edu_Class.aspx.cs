using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Edu_Class : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        DataClassesDataContext dc = new DataClassesDataContext();

        var course = from x in dc.course where x.courseID == 1 select x;
        if (course.Count() > 0)
        {
            string teacherid = course.First().teacherID.ToString();
            var teacher = from x in dc.teacher where x.teacherID.ToString() == teacherid select x;

            string response = "<tr>";
            response += "<td>" + course.First().courseName + "</td><td>" + course.First().credit.ToString() + "</td><td>" + course.First().courseTime + "</td><td>" + course.First().weekNmuber.ToString() + "</td><td>" + course.First().coursePlace + "</td><td>" + teacher.First().name + "</td>";
            response += "</tr>";

            Response.Write(response);
            Response.End();
        }
    }
}