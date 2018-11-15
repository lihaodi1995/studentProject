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
    public partial class teacher : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            MySqlConnection con = db.CreateConnection();
            con.Open();

            string strSql = "select *  from term where year='" + DateTime.Now.Year.ToString() + "'";
            MySqlCommand cmd = new MySqlCommand(strSql, con);
            DataSet ds = new DataSet();
            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
            da.Fill(ds, "table1");
            try
            {
                year.Text = ds.Tables["table1"].Rows[0]["year"].ToString();
                bgtime.Text = ds.Tables["table1"].Rows[0]["bgtime"].ToString();
                edtime.Text = ds.Tables["table1"].Rows[0]["edtime"].ToString();
                week.Text = ds.Tables["table1"].Rows[0]["week"].ToString();
            }
            catch
            {
                year.Text = "尚未录入数据";
                bgtime.Text = "尚未录入数据";
                edtime.Text = "尚未录入数据";
                week.Text = "尚未录入数据";
            }
            con.Close();
        }
        protected void logout()
        {
            Session.Remove("username");
            Session.Remove("password");
            Response.Redirect("WebForm1.aspx");
        }
        protected void SaveButton_Click(object sender, EventArgs e)
        {
            if ((memup.Text == "") || (memdn.Text == ""))
            {
                Response.Write("<script>alert('信息不完整!')</script>");
            }
            else
            {
                MySqlConnection con = db.CreateConnection();
                con.Open();
                string strSql = "update class set memup = " + memup.Text + " , memdn = " + memdn.Text + " where year = " + DateTime.Now.Year.ToString();
                MySqlCommand cmd = new MySqlCommand(strSql, con);
                DataSet ds = new DataSet();
                MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
                cmd.ExecuteNonQuery();
                con.Close();
            }
        }
       

    protected void uploadButton_Click(object sender, EventArgs e)
        {
            MySqlConnection con = db.CreateConnection();
            //if (fileUpload.HasFile)
            {
                string filename = fileUpload.FileName;
                string savePaths = Server.MapPath(("\\\\upfiles\\\\") + filename);//Server.MapPath 获得虚拟服务器相对路径
                string savePath = savePaths.ToString().Replace("\\", "\\\\");
                fileUpload.SaveAs(savePath);                        //SaveAs 将上传的文件内容保存在服务器上
                string sql1 = "select* from source where type=5";  //判断是否存在教学大纲
                con.Open();
                MySqlDataAdapter msda = new MySqlDataAdapter(sql1, con);
                DataSet ds1 = new DataSet();
                msda.Fill(ds1);
                if (ds1.Tables[0].Rows.Count == 0)
                {
                    string sql = "insert source(sourcename,address,type) values('" + filename + "','" + savePath + "','5')";
                    MySqlCommand cmd = new MySqlCommand(sql, con);
                    cmd.ExecuteNonQuery();
                    con.Close();
                    Response.Write("<script>alert('课程大纲上传成功!');</script>");
                }
                else
                {
                    string sql = "update source set sourcename='" + filename + "',address='" + savePath + "'where type=5";
                    MySqlCommand cmd = new MySqlCommand(sql, con);
                    cmd.ExecuteNonQuery();
                    con.Close();
                    Response.Write("<script>alert('课程大纲更新成功!');</script>");
                }
            }



        }
        public static System.Data.DataSet ExcelSqlConnection(string filepath)
        {
            string strCon = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" + filepath + ";Extended Properties='Excel 8.0;HDR=YES;IMEX=1';";
            OleDbConnection ExcelConn = new OleDbConnection(strCon);
            try
            {
                string strCom = string.Format("SELECT * FROM [Sheet1$]");
                ExcelConn.Open();
                OleDbDataAdapter ada = new OleDbDataAdapter(strCom, ExcelConn);
                DataSet ds = new DataSet();
                ada.Fill(ds, "[Sheet1$]");
                ExcelConn.Close();
                return ds;
            }
            catch
            {
                ExcelConn.Close();
                return null;
            }
        }

        protected void downloadstudentBtn_Click(object sender, EventArgs e)
        {
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string sql1 = "select * from source where type=1";
            MySqlDataAdapter msda = new MySqlDataAdapter(sql1, con);
            DataSet ds1 = new DataSet();
            msda.Fill(ds1);
            if (ds1.Tables[0].Rows.Count == 0)
            {
                con.Close();
                Response.Write("<script>alert('学生信息表尚未上传!');</script>");
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
    }
}