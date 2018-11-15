using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class getStuList : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.teamID == 0 select x;
        string str = "";
        foreach (var aMember in stu)
        {

                str += "<tr>";
                str += "<td>" + aMember.studentID.ToString() + "</td>";
                str += "<td>" + aMember.name + "</td>";
                str += "<td>" + aMember.gender + "</td>";
                str += "<td><a id=\"btn\" onClick=\"javascript: addStu(" + aMember.studentID + "); \" >点击添加</a> </td>";
                str += "</tr>";


        }
        Response.Write(str);
    }
}