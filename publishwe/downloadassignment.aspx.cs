using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class downloadassignment : System.Web.UI.Page
{
    public void DownLoad(string FName)
    {
        string path = FName;
        System.IO.FileInfo file = new System.IO.FileInfo(path);
        HttpResponse response = HttpContext.Current.Response;
        if (file.Exists)
        {
            Response.Write("assignment/" + file.Name + ",");

        }
        else
        {
            Response.Write("This file does not exist.");
            Response.End();
        }

    }
    protected void Page_Load(object sender, EventArgs e)
    {
        var re1 = Request.QueryString["sourceid"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var re = re1.Split(',');
        for (int i = 0; i < re.Length; i++)
        {
            if (Convert.ToInt32(re[i]) != 0)
            {
                var res = from x in dc.assignment where x.assignID.ToString() == re[i] select x;
                string FileName = res.First().assignName;

                string filePath = Server.MapPath("~/assignment/" + FileName);

                DownLoad(filePath);
            }
        }
        Response.End();
    }
}