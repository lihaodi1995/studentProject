using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class ContributeIndex : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        string contributeIndex = Request.QueryString["ContributeIndex"];
        string stuID = Request.QueryString["stuId"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var stu = from x in dc.student where x.studentID.ToString() == stuID select x;
        stu.First().ContributionRate = Convert.ToDouble(contributeIndex);
        dc.SubmitChanges();

    }
}