﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;

public partial class getCheckingNameListForLeader : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string userid = Request.QueryString["userid"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.studentID.ToString() == userid select x;
        string teamId = stu.First().teamID.ToString();
        var team = from y in dc.team where y.teamID.ToString() == teamId select y;
        string namelist = team.First().checkingList;
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

                    response += "<tr><td>" + studentID + "</td><td>" + name + "</td><td>" + studentGender + "</td>" + "<td> <a type=\"button\" onClick=\"javascript: checkpassed(" + teamId + "," + studentID + ");\">是</a> <a type =\"button\" onClick=\"javascript: checkrejected(" + teamId + "," + studentID + ");\">否</a></td></tr>";

                }
            }
            Response.Write(response);
        }
    }
}