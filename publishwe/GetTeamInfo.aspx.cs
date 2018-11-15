using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class GetTeamInfo : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string teamID = Request.QueryString["teamID"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var team = from x in dc.team where x.teamID == Convert.ToInt32(teamID) select x;
        string nameList = team.First().teamMember;
        string teamName = team.First().teamName;
        string position = "";
        string leaderid = team.First().teamleaderID.ToString();
        string str = "";

        string[] strarr = nameList.Split(',');
        foreach (var aMember in strarr)
        {
            if (aMember != "")
            {
                var stu = from x in dc.student where x.name == aMember select x;
                if (stu.First().studentID.ToString() == leaderid)
                    position = "TeamLeader";
                else
                    position = "NormalMember";
                str += "<tr>";
                str += "<td>" + stu.First().studentID.ToString() + "</td>";
                str += "<td>" + stu.First().name + "</td>";
                str += "<td>" + stu.First().gender + "</td>";
                str += "<td>" + position + "</td>";
                str += "</tr>";
            }

        }
        Response.Write(str);
    }
}