using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class upload : System.Web.UI.Page
{
    string uploadFolder = "~/upload";
    protected void Page_Load(object sender, EventArgs e)
    {
        HttpFileCollection File = Context.Request.Files;
        if(File.Count==0)
        {
            Response.Write("<script>alert('没有文件');</script>"); 
        }
        else
        {
            DataClassesDataContext dc = new DataClassesDataContext();
            var re = from x in dc.sources select x;
            string id = Application["id"].ToString();
            int count = 0;
            foreach(sources n in re)
            {
                if (n.sourcesID > count)
                    count = n.sourcesID;
            }
            count++;
            string path = Server.MapPath(uploadFolder); 
            
                HttpPostedFile file = File[0];
                if (file != null && file.ContentLength > 0)
                {
                    string fileName = file.FileName;//获取文件名
                    bool ifhave = false;
                    foreach (sources n in re)
                    {
                        if (n.sourcesName == fileName)
                        {
                            ifhave = true;
                        }
                    }
                    if (ifhave == false)
                    {
                        sources asource = new sources
                        {
                            sourcesID = count,
                            sourcesName = fileName,
                            uploadTime = DateTime.Now,
                            teacherID = Convert.ToInt32(id)
                        };
                        dc.sources.InsertOnSubmit(asource);
                        dc.SubmitChanges();
                        string savePath = path + "/" + file.FileName;


                        file.SaveAs(savePath);
                        Response.Write("<script>self.location='资源管理_教师.htm' </script>");
                        Response.End();

                    }
                    else
                    {
                        Response.Write("<script>alert('有重复资源') </script>");
                        Response.Write("<script>self.location='资源管理_教师.htm' </script>");
                        Response.End();
                    }


                }

            
             
        }
        
    }
}