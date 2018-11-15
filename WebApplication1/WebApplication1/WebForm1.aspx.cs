using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using MySql.Data.MySqlClient;
using System.Data;

namespace WebApplication1
{
    public partial class WebForm1 : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            {

                int judge = 0;

                judge = Convert.ToInt32(Request["value"]);

                if (!IsPostBack)
                {






                    //if (judge == 1)
                    //{

                    //    Response.Write("<script>alert('该用户已经登录！')</script>");
                    //}
                }

            }
        }
        
        protected void LoginButton_Click(object sender, EventArgs e)
        {
            Application.Lock();//锁定Application对象

            int num;     //在线人数

            string name; //登录用户

            string zs_name;  //已在线的用户名

            string[] user; //在线用户的数组

            num = int.Parse(Application["userNum"].ToString());
            if ((tb1.Text == "") || (pw1.Text == ""))
            {
                loginLabel.Text = "用户名与密码不能为空!";

            }
            else
            {
                MySqlConnection con = db.CreateConnection();
                con.Open();
                string strSql = "select *  from user where userid='" + tb1.Text + "'";
                MySqlCommand cmd = new MySqlCommand(strSql, con);
                DataSet ds = new DataSet();
                MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
                da.Fill(ds, "mytable");
                try
                {
                    if (pw1.Text == ds.Tables[0].Rows[0].ItemArray[1].ToString().Trim())
                    {

                        string username = tb1.Text;
                        string password = pw1.Text;
                        Session["username"] = username;
                        Session["password"] = password;
                        loginLabel.Text = "登录成功,欢迎你!";
                        if (ds.Tables[0].Rows[0].ItemArray[2].ToString().Trim() == "1")
                        {
                            Response.Redirect("termManage.aspx");
                        }
                        else if (ds.Tables[0].Rows[0].ItemArray[2].ToString().Trim() == "2")
                        {
                            name = tb1.Text.Trim();

                            zs_name = Application["user"].ToString();

                            user = zs_name.Split(',');

                            //for (int i = 0; i <= num - 1; i++)

                            //{

                            //    if (name == user[i].Trim())

                            //    {

                            //        int judge = 1;

                            //        Response.Redirect("WebForm1.aspx?value=" + judge);

                            //    }

                            //}

                            if (num == 0)

                                Application["user"] = name.ToString();

                            else

                                Application["user"] = Application["user"] + "," + name.ToString();

                            num += 1;

                            Application["userNum"] = num;

                            Session["teacherName"] = tb1.Text.Trim();

                            Application.UnLock();

                            Response.Redirect("teacher.aspx");
                        }




                        else if (ds.Tables[0].Rows[0].ItemArray[2].ToString().Trim() == "3")
                        {
                            name = tb1.Text.Trim();

                            zs_name = Application["user"].ToString();

                            user = zs_name.Split(',');

                            //for (int i = 0; i <= num - 1; i++)

                            //{

                            //    if (name == user[i].Trim())

                            //    {

                            //        int judge = 1;

                            //        Response.Redirect("WebForm1.aspx?value=" + judge);

                            //    }

                            //}

                            if (num == 0)

                                Application["user"] = name.ToString();

                            else

                                Application["user"] = Application["user"] + "," + name.ToString();

                            num += 1;

                            Application["userNum"] = num;

                            Session["userName"] = tb1.Text.Trim();

                            Application.UnLock();

                            Response.Redirect("studentCourse.aspx");

                        }


                        else
                        {
                            loginLabel.Text = "用户名或者密码错误!";
                        }
                    }
                }
                catch
                {
                    loginLabel.Text = "Sorry!你输入的用户名不存在!";

                }
                con.Close();
            }
        }
    }
}