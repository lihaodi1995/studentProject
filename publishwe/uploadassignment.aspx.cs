using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class uploadassignment : System.Web.UI.Page
{
    string uploadFolder = "~/assignment";
    protected void Page_Load(object sender, EventArgs e)
    {
        HttpFileCollection File = Context.Request.Files;
        if (File.Count == 0)
        {
            Response.Write("<script>alert('没有文件');</script>");
        }
        else
        {
            DataClassesDataContext dc = new DataClassesDataContext();
            var re = from x in dc.sources select x;


            string path = Server.MapPath(uploadFolder);

            HttpPostedFile file = File[0];
            if (file != null && file.ContentLength > 0)
            {
                string fileName = file.FileName;//获取文件名



                string savePath = path + "/" + file.FileName;



                file.SaveAs(savePath);
               
                Response.Write("<script>self.location='作业信息_学生.htm' </script>");
                Response.End();





            }



        }
    }
}