using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class checkPassed : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string teamID = Request.QueryString["teamID"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var team = from x in dc.team where x.teamID == Convert.ToInt32(teamID) select x;
        var ateam = dc.team.Single(p => p.teamID == Convert.ToInt32(teamID));
        ateam.ifChecked = true;
        ateam.ifAccepted = true;
        dc.SubmitChanges();
    }
}