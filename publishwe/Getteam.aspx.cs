using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Getteam : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        DataClassesDataContext dc = new DataClassesDataContext();
        var result = from x in dc.team where x.ifOrganized==false select x;
        if (result == null)
            Response.Write("1");
        else
        {
            string response="";
            foreach (team x in result)
            {
                var leader = from y in dc.student where y.studentID == x.teamleaderID select y;
                response += "<tr>";
                response += "<td>" + x.teamName + "</td>";
                response += "<td>" + leader.First().name + "</td>";
                response += "<td>" + x.quantity + "</td>";
                response += "<td>" + x.femaleNumber + "</td>";
                response += "<td><a onClick=\"javascript: enterteam(" + x.teamID+  "); \" >点击加入</a> </td>";
                response += "</tr>";           
            }
            Response.Write(response);
        }

        Response.End();
    }
}