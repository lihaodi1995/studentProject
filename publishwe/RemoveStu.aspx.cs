using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class RemoveStu : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string stuID = Request.QueryString["stuId"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.studentID.ToString() == stuID select x;
        string teamId = stu.First().teamID.ToString();
        string stuName = stu.First().name;
        string gender = stu.First().gender;
        var team = from x in dc.team where x.teamID.ToString() == teamId select x;
        string leaderid = team.First().teamleaderID.ToString();
        if (leaderid == stuID)
            Response.Write("1\n");
        else
        {
            string oldList = team.First().teamMember;
            string newList = "";
            string[] strarr = oldList.Split(',');
            foreach (var name in strarr)
            {
                if (name != "" && name != stuName)
                {
                    newList += name + ",";
                }
            }
            team.First().teamMember = newList;
            team.First().quantity--;
            if (gender == "female")
                team.First().femaleNumber--;
            stu.First().teamID = 0;
            stu.First().rejectedByTeacher = true;
            dc.SubmitChanges();
        }
    }
}