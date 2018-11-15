using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Publishwork : System.Web.UI.Page
{
    string uploadFolder = "~/task";
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        string filename = Request.QueryString["filename"];
        string workName = Request.QueryString["workName"];
        DataClassesDataContext dc = new DataClassesDataContext();
        string workDetail = Request.QueryString["workDetail"];
        string workStartTime = Request.QueryString["workStartTime"];
        string workEndTime = Request.QueryString["workEndTime"]; 
        string sendTime = Request.QueryString["sendTime"];
        string proportion = Request.QueryString["proportion"];
        var re = from x in dc.task select x;
        int count = 0;
        foreach(task n in re)
        {
            if (n.taskid > count)
                count = n.taskid;
        }
        count++;
        task atask= new task{
            taskid=count,
            taskdetail=workDetail,
            starttime=Convert.ToDateTime( workStartTime),
            endtime=Convert.ToDateTime( workEndTime),
            taskrate=Convert.ToDouble(proportion),
            taskname=workName,
            tasksname=filename,
            taskquantity=Convert.ToInt32( sendTime)
        };
        dc.task.InsertOnSubmit(atask);
        dc.SubmitChanges();
        HttpFileCollection File = Context.Request.Files;
        if (File.Count == 0)
        {
            Response.Write("<script>alert('没有文件');</script>");
        }
        else
        {
            


            string path = Server.MapPath(uploadFolder);

            HttpPostedFile file = File[0];
            if (file != null && file.ContentLength > 0)
            {
                string fileName = file.FileName;//获取文件名



                string savePath = path + "/" + file.FileName;


                file.SaveAs(savePath);

               





            }



        }
        Response.End();

        
    }
   
 
}