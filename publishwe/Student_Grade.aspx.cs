using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Student_Grade : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {


        Response.Clear();
        string student_id = Request.QueryString["student_id"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.studentID.ToString() == student_id select x;
        string teamID = stu.First().teamID.ToString();
        double conbtribute = Convert.ToDouble(stu.First().ContributionRate);
        var team = from x in dc.team where x.teamID.ToString() == teamID select x;
        string response;
        if (team.Count() != 0)
        {
            int teamGrade = Convert.ToInt32(team.First().teamScore);
            int stuGrade = Convert.ToInt32(teamGrade * conbtribute);
             response = "<tr>";
            response += "<td>" + stu.First().studentID.ToString() + "</td><td>" + stu.First().name + "</td><td>" + conbtribute.ToString() + "</td><td>" + stuGrade.ToString() + "</td>";
            response += "</tr>";

        }
        else
        {
            response = "<tr>";
            response += "<td>" + stu.First().studentID.ToString() + "</td><td>" + stu.First().name + "</td><td>0</td><td>0</td>";
            response += "</tr>";
        }
        Response.Write(response);
        Response.End();
    }
}