using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace WebApplication1
{
    public partial class logout : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            Application.Lock();

            string userName = Application["user"].ToString();

            Application["user"] = userName.Replace(Session["userName"].ToString(), "");

            Application.UnLock();

            Response.Write("<script>window.opener=null;window.close();</script>");
            Response.Redirect("WebForm1.aspx");
        }
    }
}