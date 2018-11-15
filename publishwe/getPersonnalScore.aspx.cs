using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class getPersonnalScore : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string teamID = Request.QueryString["teamID"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var team = from x in dc.team where x.teamID.ToString() == teamID select x;
        string nameList = team.First().teamMember;
        string[] strarr = nameList.Split(',');
        string response = "";
        int teamScore = Convert.ToInt32(team.First().teamScore);
        foreach(var name in strarr)
        {
            if(name!="")
            {
                response += "<tr>";
                var stu = from x in dc.student where x.name == name select x;
                int score = Convert.ToInt32(stu.First().ContributionRate * teamScore);
                response += "<td>" + stu.First().studentID.ToString() + "</td><td>" + stu.First().name + "</td><td>" + score.ToString() + "</td>";
                response += "</tr>";

            }
        }
        Response.Write(response);
        Response.End();
    }
}