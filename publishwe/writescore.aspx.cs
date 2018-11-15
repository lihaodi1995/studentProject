using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class writescore : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        var teamname = Request.QueryString["teamname"];
        var score = Request.QueryString["score"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var teamre = teamname.Split(',');
        var scorere = score.Split(',');
        for(var i=0;i<teamre.Length;i++)
        {
            if(teamre[i]!="")
            {
                var re = from x in dc.assignment where x.assignID.ToString() == teamre[i] select x;
                re.First().teamEveryScore = Convert.ToInt32(scorere[i]);
                string teamID = re.First().teamID.ToString();
                var team = from x in dc.team where x.teamID.ToString() == teamID select x;
                var assignment = from x in dc.assignment where x.teamID.ToString() == teamID select x;
                
                int theScore=0;
               
                foreach(var y in assignment)
                {
                
                    var task = from x in dc.task where x.taskid == y.taskid select x;
                    if (task.First().taskrate != null)
                    {
                        theScore = theScore + Convert.ToInt32(y.teamEveryScore * task.First().taskrate);
                    }
                }
                team.First().teamScore = Convert.ToInt32(theScore);
                dc.SubmitChanges();
            }
        }
        Response.End();
    }
}