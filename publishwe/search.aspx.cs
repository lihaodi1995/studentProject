using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class search : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        DataClassesDataContext dc = new DataClassesDataContext();
        var str=Request.QueryString["searchid"];
        var result = from x in dc.sources where x.sourcesName.Contains(str) select x;

        foreach (sources x in result)
        {
            string da = x.uploadTime.ToString();
            var d = da.Split(' ');
            Response.Write(x.sourcesID + ",");
            Response.Write(x.sourcesName + ",");
            Response.Write(d[0] + "\n");
        }

        Response.End();
    }
}