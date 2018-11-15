using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Getifteam : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string teamStatus = "", stuStatus = "", stuType = "";
        DataClassesDataContext dc = new DataClassesDataContext();
        string sid=Request.QueryString["studentID"];        
        var stu = from x in dc.student where x.studentID.ToString() == sid select x;
        
        if (stu.First().teamID == 0 && stu.First().rejectedByLeader == true)
            stuStatus = "rejectedByLeader";
        else if (stu.First().teamID == 0 && stu.First().rejectedByTeacher == true)
            stuStatus = "rejectedByTeacher";
        else if (stu.First().teamID == 0 && stu.First().rejectedByLeader == false && stu.First().rejectedByTeacher == false)
            stuStatus = "noTeamed";
        else if (stu.First().teamID !=0)
        {
            stuStatus = "enteredTeam";
            var team = from x in dc.team where x.teamID == stu.First().teamID select x;
            if (team.First().teamleaderID == Convert.ToInt32(sid))
                stuType = "teamLeader";
            else
                stuType = "normalStu";
            if (team.First().ifOrganized == false)
                teamStatus = "waitingOrganized";
            else if (team.First().ifOrganized == true && team.First().ifChecked == false)
                teamStatus = "waitingChecked";
            else if (team.First().ifOrganized == true && team.First().ifChecked == true && team.First().ifAccepted == false)
                teamStatus = "rejectedByTeacher";
            else if (team.First().ifOrganized == true && team.First().ifChecked == true && team.First().ifAccepted == true)
                teamStatus = "completed";           
        }
        Response.Write(stuStatus +","+teamStatus+","+stuType);
        Response.End();
    }
}