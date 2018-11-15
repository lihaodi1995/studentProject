using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class getStuInfoOfTeamNow : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string userid = Request.QueryString["userid"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.studentID.ToString() == userid select x;
        string teamId = stu.First().teamID.ToString();
        var team = from y in dc.team where y.teamID.ToString() == teamId select y;

            string namelist = Convert.ToString(team.First().teamMember);
        if (namelist != null)
        {
            string[] strarr = namelist.Split(',');
            string response = "";
            foreach (var name in strarr)
            {
                if (name != "")
                {
                    var studentInList = from x in dc.student where x.name == name select x;
                    string studentID = studentInList.First().studentID.ToString();
                    string studentGender = studentInList.First().gender;
                    string position;
                    if (studentID == team.First().teamleaderID.ToString())
                        position = "TeamLeader";
                    else
                        position = "TeamMember";
                    response += "<tr><td>" + studentID + "</td><td>" + name + "</td><td>" + position + "</td><td>" + studentGender + "</td></tr>";
                }
            }
            Response.Write(response);
        }
    }
}