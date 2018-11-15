using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class uploadassign : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string filename = Request.QueryString["filename"];
        string userid = Request.QueryString["userid"];
        DataClassesDataContext dc = new DataClassesDataContext();
        
        string taskid = Request.QueryString["taskid"];
        var re = from x in dc.assignment select x;
        var teamre=from x in dc.student where x.studentID.ToString()==userid select x;
        int count = 0;
        var assignre = from x in dc.assignment where x.taskid.ToString() == taskid && x.teamID == teamre.First().teamID select x;

        foreach (assignment n in re)
        {
            if (n.assignID > count)
                count = n.assignID;
        }
        count++;
        assignment assign = new assignment
        {
            assignID=count,
            teamID=teamre.First().teamID,
            assignName=filename,
            uploadTime=DateTime.Now,
            taskid=Convert.ToInt32( taskid),
           
        };
        foreach(assignment n in assignre)
        dc.assignment.DeleteOnSubmit(n);
        dc.assignment.InsertOnSubmit(assign);
        dc.SubmitChanges();
    }
}