using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;
using System.Collections;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Web.SessionState;
using System.Web.UI.HtmlControls;

public partial class Student_Already_Enter : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        /*DataClassesDataContext dc = new DataClassesDataContext();
        var result = from x in dc.team select x;
        foreach (team x in result)
        {
            Response.Write(x.teamID + ",");
            Response.Write(x.teamName + ",");
            Response.Write(x.teamleaderID + ",");
            Response.Write(x.courseTime + ",");
            Response.Write(x.teamScore + "\n");
        }
      
        Response.End();*/
        var stuID = Request.QueryString["stuID"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var student = from x in dc.student where x.studentID == Convert.ToInt32(stuID) select x;
        var teamID = student.First().teamID;
        var team = from y in dc.team where y.teamID == teamID select y;
        var teamLeaderID = team.First().teamleaderID;
        var teamleader = from x in dc.student where x.studentID == teamLeaderID select x;
        string response = "";
        response += team.First().teamID.ToString()+"\n";
        response += "<tr>";
        response += "<td>" + teamID.ToString() + "</td>";
        response += "<td>" + team.First().teamName + "</td>";
        response += "<td>" + teamleader.First().name + "</td>";
        response += "<td>" + team.First().quantity + "</td>";
        response += "<td><a onClick=\"javascript: enterteam(" + teamID + "); \" >成员名单</a> </td>";
        response += "<td>" + team.First().teamScore + "</td>";
        response += "</tr>";

        Response.Write(response);
        Response.End();
    }
}