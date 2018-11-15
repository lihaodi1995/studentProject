using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class getGradeOfAllStudent : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student select x;
        string response = "<table><thead><th>学号</th><th>姓名</th><th>团队ID</th><th>所在团队成绩</th><th>个人成绩</th></thead><tbody>";
        foreach(var student in stu)
        {
            if (student.teamID != 0)
            {
                response += "<tr>";
                var team = from x in dc.team where x.teamID == student.teamID select x;
                int personalScore = Convert.ToInt32(team.First().teamScore * student.ContributionRate);
                response += "<td>" + student.studentID.ToString() + "</td><td>" + student.name + "</td><td>" + student.teamID.ToString() + "</td><td>" + team.First().teamScore.ToString() + "</td><td>" + personalScore.ToString() + "</td>";
                response += "</tr>";
            }
            else if(student.teamID != 0&&student.rejectedByLeader==false&&student.rejectedByTeacher==false)
            {
                response += "<tr>";                
                response += "<td>" + student.studentID.ToString() + "</td><td>" + student.name + "</td><td>0</td><td>0</td><td>0</td>";
                response += "</tr>";
            }
        }
        response += "</tbody></table>";
        Response.Write(response);
        Response.End();
    }
}