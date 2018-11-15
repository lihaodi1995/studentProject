using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Teacher_Grade : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        
        DataClassesDataContext dc = new DataClassesDataContext();

        var team = from x in dc.team where x.ifOrganized==true&&x.ifChecked==true&&x.ifAccepted==true select x;
        string response = ""; 
        foreach (var t in team)
        {
            response += "<tr>";
            response += "<td>" + t.teamID.ToString() + "</td><td>" + t.teamName + "</td><td>" + t.teamScore.ToString() + "</td>" + "<td><a id=\"btn\" onClick=\"javascript: stuGrade(" + t.teamID + "); \" >点击查看成员成绩</a> </td>";
            response += "</tr>";
        }
        Response.Write(response);


        Response.End();
    }
}