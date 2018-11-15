using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class _Default : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
       

        Response.Clear();

        string userid = Request.QueryString["userid"];
        Application["id"] = userid;
        string password = Request.QueryString["password"];
       
        DataClassesDataContext dc = new DataClassesDataContext();
        int len = userid.Length;     //区分用户类别抓取不同的表信息
        switch (len)
        {
            case 8:
                var student = from x in dc.student where x.studentID.ToString() == userid && x.password == password select x;
                if (student.ToList().Count == 0)
                    Response.Write("");
                else
                Response.Write(student.First().name);

                break;
            case 6:
                var teacher = from x in dc.teacher where x.teacherID.ToString() == userid && x.password == password select x;
                if (teacher.ToList().Count == 0)
                    Response.Write("");
                else
                    Response.Write(teacher.First().name);
                break;
            case 4:
                var administrator = from x in dc.administrator where x.adminID.ToString() == userid && x.password == password select x;
                Response.Write(administrator.First().adminID.ToString());
                if(administrator.ToList().Count==0)
                    Response.Write("");
                else
                    Response.Write(administrator.First().adminID.ToString());
                break;
        }


       

        Response.End();
    }
}