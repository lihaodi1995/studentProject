using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Student_Already_Enter1 : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();

        string member = Request.QueryString["member"];

        string number = Request.QueryString["number"];
        Response.Write("mumber");

        Response.End();
    }
}