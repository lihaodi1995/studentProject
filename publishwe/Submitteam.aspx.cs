using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Submitteam : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        var teamname = Request.QueryString["teamname"];
        var leaderid = Request.QueryString["leaderid"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var re = from x in dc.team select x;
        var leader = from x in dc.student where x.studentID.ToString() == leaderid select x;
        string gender = leader.First().gender;
        int flag;
        if (gender == "female")
            flag = 1;
        else
            flag=0;
        int count = 0;
        foreach (team a in re)
        {
            count++;
        }
        count++;
        leader.First().teamID = count;
        team ateam = new team
        {
           teamID=count,
           teamleaderID=Convert.ToInt32( leaderid),
           quantity=1,
           femaleNumber=flag,
           teamMember=leader.First().name+",",
           teamName=teamname,
           ifOrganized=false,
           ifAccepted=false,
           ifChecked=false,
           

        };
        dc.team.InsertOnSubmit(ateam);
        dc.SubmitChanges();
        Response.Write("<script>alert('创建成功');</script>"); 
        Response.End();
    }
}