using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class RejectedByLeader : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        {
            Response.Clear();
            string userid = Request.QueryString["userID"];
            DataClassesDataContext dc = new DataClassesDataContext();            
            var ateam = dc.student.Single(p => p.studentID == Convert.ToInt32(userid));
            ateam.rejectedByLeader = false;
            dc.SubmitChanges();

        }
    }
}