using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using MySql.Data.MySqlClient;
using System.Data;
using System.Data.OleDb;
using System.IO;

namespace WebApplication1
{
    public partial class studentCourse : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            year.Text = DateTime.Now.Year.ToString();
            MySqlConnection con = db.CreateConnection();
            con.Open();


            string strSql1 = "select *  from term where year='" + year.Text + "'";
            MySqlCommand cmd1 = new MySqlCommand(strSql1, con);
            DataSet ds1 = new DataSet();
            MySqlDataAdapter da1 = new MySqlDataAdapter(strSql1, con);
            da1.Fill(ds1, "table1");
            try
            {
                bgtime.Text = ds1.Tables["table1"].Rows[0]["bgtime"].ToString();
                edtime.Text = ds1.Tables["table1"].Rows[0]["edtime"].ToString();
            }
            catch
            {
                bgtime.Text = "尚未录入数据";
                edtime.Text = "尚未录入数据";
            }

            string strSql2 = "select *  from class where year='" + year.Text + "'";
            MySqlCommand cmd2 = new MySqlCommand(strSql2, con);
            DataSet ds2 = new DataSet();
            MySqlDataAdapter da2 = new MySqlDataAdapter(strSql2, con);
            da2.Fill(ds2, "table2");
            try
            {
                memup.Text = ds2.Tables["table2"].Rows[0]["memup"].ToString();
                memdn.Text = ds2.Tables["table2"].Rows[0]["memdn"].ToString();
            }
            catch
            {
                memup.Text = "尚未录入数据";
                memdn.Text = "尚未录入数据";
            }

            con.Close();
        }
        protected void logout()
        {
            Session.Remove("username");
            Session.Remove("password");
            Response.Redirect("WebForm1.aspx");
        }
        protected void DownloadButton_Click(object sender, EventArgs e)
        {
            try
            {
                MySqlConnection con = db.CreateConnection();
                con.Open();
                string sql1 = "select * from source where type=5";
                MySqlDataAdapter msda = new MySqlDataAdapter(sql1, con);
                DataSet ds1 = new DataSet();
                msda.Fill(ds1);
                if (ds1.Tables[0].Rows.Count == 0)
                {
                    con.Close();
                    Response.Write("<script>alert('教学大纲尚未上传!');</script>");
                }
                else
                {
                    string fileURL = ds1.Tables[0].Rows[0]["address"].ToString();//文件路径，可用相对路径
                    FileInfo fileInfo = new FileInfo(fileURL);
                    Response.Clear();
                    Response.AddHeader("content-disposition", "attachment;filename=" + Server.UrlEncode(fileInfo.Name.ToString()));//文件名
                    Response.AddHeader("content-length", fileInfo.Length.ToString());//文件大小
                    Response.ContentType = "application/octet-stream";
                    Response.ContentEncoding = System.Text.Encoding.Default;
                    Response.WriteFile(fileURL);
                    con.Close();
                }
            }

            catch
            {
                Response.Write("<script>alert('老师尚未上传大纲')</script>");
            }
        }
    }
}