using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json.Converters;
using Newtonsoft.Json;



public partial class ImportInfo : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        DataClassesDataContext dc = new DataClassesDataContext();
        string stuInfo = Request.QueryString["string"];
        JArray jArray = (JArray)JsonConvert.DeserializeObject(stuInfo);//jsonArrayText必须是带[]数组格式字符串
        foreach(var x in jArray)
        {
            if (x != null)
            {
                string str1 = x["学号"].ToString();
                string str2 = x["姓名"].ToString();
                string str3 = x["性别"].ToString();
                string str4 = x["密码"].ToString();
                var newStudent = new student
                {
                    studentID = Convert.ToInt32(str1),
                    name = str2,
                    gender = str3,
                    password = str4,
                    teamID = 0
                };
                int flag = 0;
                var stu = from y in dc.student select y;
                foreach(var z in stu)
                {
                    if (z.studentID.ToString() == str1)
                    {
                        flag = 1;
                        break;
                    }
                }
                if(flag == 1)
                    continue;
                dc.student.InsertOnSubmit(newStudent);
            }

        }
        dc.SubmitChanges();



    }
}