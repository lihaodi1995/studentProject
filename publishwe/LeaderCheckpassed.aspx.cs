using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class LeaderCheckpassed : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string teamID = Request.QueryString["teamID"];
        string studentID = Request.QueryString["studentID"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.studentID == Convert.ToInt32(studentID) select x;
        string name = stu.First().name;
        
        var team = from x in dc.team where x.teamID == Convert.ToInt32(teamID) select x;
        string OldcheckingNameList = team.First().checkingList;
        string[] strra = OldcheckingNameList.Split(',');
        string NewcheckingNameList = "";
        foreach (var checkingName in strra)
        {
            if(checkingName!=""&&checkingName!=name)
            {
                NewcheckingNameList += checkingName + ",";
            }
        }
        team.First().checkingList = NewcheckingNameList;
        team.First().teamMember += (name + ",");
        team.First().quantity++;
        if (stu.First().gender == "female")
            team.First().femaleNumber++;
        dc.SubmitChanges();
    }
}