using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class addNewMember : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string teamID = Request.QueryString["teamID"];
        string stuID = Request.QueryString["stuId"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var student = from x in dc.student where x.studentID.ToString() == stuID select x;
        var team = from x in dc.team where x.teamID.ToString() == teamID select x;
        student.First().teamID = Convert.ToInt32(teamID);
        student.First().rejectedByLeader = false;
        student.First().rejectedByTeacher = false;
        team.First().teamMember += student.First().name + ",";
        team.First().quantity++;
        if(student.First().gender=="female")
        team.First().femaleNumber++;
        dc.SubmitChanges();
        
           

    }
}