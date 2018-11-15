using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Text;


public partial class Handler : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();
        DataClassesDataContext dc = new DataClassesDataContext();
        var course = from x in dc.course where x.courseID == 1 select x;
        
        StringBuilder strBul = new StringBuilder();
       
        strBul.Append("<th>" + course.First ().courseID .ToString()+ "</th>");
        strBul.Append("<th>" + course.First ().courseName +"</th>");
        strBul.Append("<th>" + Convert.ToDateTime(course.First().courseTime).ToString("yyyy-MM-dd") + "</th>");
        strBul.Append("<th>" + course.First().weekNmuber.ToString()+"</th>");
        strBul.Append("<th>" + course.First().coursePlace + "</th>");
        strBul.Append("<th>" + course.First().credit.ToString() + "</th>");
       
        Response.ContentType = "text/html";
        Response.Write(strBul.ToString());
        Response.End();//这句是关键，这是因为没有关闭，所以会输出页面所有的html标签，而不只是xml文件，所以会为空
            
        }
    
}