using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class LeaderComment : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string teamID = Request.QueryString["teamID"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var team = from x in dc.team where x.teamID.ToString() == teamID select x;
        string nameList = team.First().teamMember;
        string[] strarr = nameList.Split(',');
        string response = "";
        int log = 1;
        foreach(var name in strarr)
        {
            if (name != "")
            {
                var stu = from x in dc.student where x.name == name select x;
                response += "<tr>";
                response += "<td>" + stu.First().studentID + "</td>";
                response += "<td>" + stu.First().name + "</td>";
                response += "<td><select  id=\"s"+log.ToString()+"\"style=\"color:#000000\"><option value = \"0.6\" style=\"color:#000000\">0.6</option><option value = \"0.8\" style=\"color:#000000\" >0.8</option><option value = \"1.0\" style=\"color:#000000\">1.0 </option><option value = \"1.2\" style=\"color:#000000\" >1.2</option><option value = \"1.4\" style=\"color:#000000\" >1.4</option></select></td>";
                response += "</tr>";
                log++;
            }
        }
        Response.Write(response);

    }
}