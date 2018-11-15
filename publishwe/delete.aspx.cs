using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.IO;
public partial class delete : System.Web.UI.Page
{
    public void DownLoad(string FName)
    {
        string path = FName;
        System.IO.FileInfo file = new System.IO.FileInfo(path);
        HttpResponse response = HttpContext.Current.Response;
        if (file.Exists)
        {
            Response.Write("upload/" + file.Name + ",");

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
        
        
        var re = re1.Split(',');
        for (int i = 0; i < re.Length; i++)
        {
            if (Convert.ToInt32(re[i]) != 0)

            {
                DataClassesDataContext dc = new DataClassesDataContext();
                var res = from x in dc.sources where x.sourcesID.ToString() == re[i] select x;
                
                string FileName = res.First().sourcesName;

                string filePath = Server.MapPath("~/upload/" + FileName);
                File.Delete(filePath);
                dc.sources.DeleteOnSubmit(res.First());
                dc.SubmitChanges();
                
            }
        }
        Response.Write("<script>window.location='资源管理_教师.htm' </script>");
        Response.End();
        
    }
}