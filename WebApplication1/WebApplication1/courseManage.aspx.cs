using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.OleDb;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace WebApplication1
{
    public partial class courseManage : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!Page.IsPostBack)
            {
                MySqlConnection con = db.CreateConnection();
                con.Open();
                string strSql = "select* from class where year="+ DateTime.Now.Year.ToString();
                MySqlCommand cmd = new MySqlCommand(strSql, con);
                DataSet ds = new DataSet();
                MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
                MySqlDataReader dr = cmd.ExecuteReader();
                if (dr.Read())
                {
                    classNameTb.Text = dr["classname"].ToString();
                    classPointTb.Text = dr["point"].ToString();
                    classTimeTb.Text = dr["classtime"].ToString();
                    classPlaceTb.Text = dr["classplace"].ToString();
                    classTeacherTb.Text = dr["teachername"].ToString();
                }
                con.Close();
            }
        }
        protected void logout()
        {
            Session.Remove("username");
            Session.Remove("password");
            Response.Redirect("WebForm1.aspx");
        }

        protected void uploadButton_Click(object sender, EventArgs e)
        {
            MySqlConnection con = db.CreateConnection();

            if (fileUpload.HasFile)
            {
                string IsXls = System.IO.Path.GetExtension(fileUpload.FileName).ToString().ToLower();//System.IO.Path.GetExtension获得文件的扩展名
                Response.Write("<script>alert(" + IsXls + ")</script>");
                if (IsXls != ".xlsx" && IsXls != ".xls")
                {
                    Response.Write("<script>alert('只可以选择Excel文件')</script>");
                    return;
                }
                con.Open();
                string filename = fileUpload.FileName;
                string savePaths = Server.MapPath(("\\\\upfiles\\\\") + filename);//Server.MapPath 获得虚拟服务器相对路径
                string savePath = savePaths.ToString().Replace("\\", "\\\\");
                fileUpload.SaveAs(savePath);                        //SaveAs 将上传的文件内容保存在服务器上
                string sql1 = "select* from source where type=1";
                MySqlDataAdapter msda = new MySqlDataAdapter(sql1, con);
                DataSet ds1 = new DataSet();
                msda.Fill(ds1);
                if (ds1.Tables[0].Rows.Count == 0)
                {
                    string sql = "insert source(sourcename,address,type) values('" + filename + "','" + savePath + "','1')";
                    MySqlCommand cmd = new MySqlCommand(sql, con);
                    cmd.ExecuteNonQuery();
                    con.Close();
                }
                else
                {
                    string sql = "update source set sourcename='"+filename+"',address='"+ savePath+"'where type=1";
                    MySqlCommand cmd = new MySqlCommand(sql, con);
                    cmd.ExecuteNonQuery();
                    con.Close();
                }
                DataSet ds = new DataSet();
                ds = ExcelSqlConnection(savePath);           //调用自定义方法
                try
                {
                    int rowsnum = ds.Tables[0].Rows.Count;
                    if (rowsnum == 0)
                    {
                        Response.Write("<script>alert('Excel表为空表,无数据!')</script>");   //当Excel表为空时,对用户进行提示
                    }
                    else
                    {
                        DataRow[] dr = ds.Tables[0].Select();            //定义一个DataRow数组
                        for (int i = 0; i < dr.Length; i++)
                        {

                            string id = dr[i][0].ToString();
                            string password = dr[i][1].ToString();
                            string type = dr[i][2].ToString();
                            string sex = dr[i][3].ToString();
                            string name = dr[i][4].ToString();
                            //Response.Write("<script>alert('导入内容:" + ex.Message + "')</script>");
                            con.Open();
                            try
                            {
                                string comstr1 = "insert into user(userid,password,type) values('" + id + "','" + password + "','" + type + "')";
                                MySqlCommand cmd1 = new MySqlCommand(comstr1, con);
                                cmd1.ExecuteNonQuery();
                                string comstr2= "insert into student(userid,sex,name) values('" + id + "','" + sex + "','" + name + "')";
                                MySqlCommand cmd2 = new MySqlCommand(comstr2, con);
                                cmd2.ExecuteNonQuery();
                                con.Close();
                            }
                            catch
                            {
                                string comstr3 = "update user set password ='" + password + "',type = '" + type + "' where userid='" + id + "'";
                                MySqlCommand cmd3 = new MySqlCommand(comstr3, con);
                                cmd3.ExecuteNonQuery();
                                string comstr4 = "update student set sex ='" + sex + "',name = '" + name + "' where userid='" + id + "'";
                                MySqlCommand cmd4 = new MySqlCommand(comstr4, con);
                                cmd4.ExecuteNonQuery();
                                con.Close();
                            }
                        }
                        Response.Write("<script>alert('用户表导入成功!');</script>");
                    }
                }
                catch
                {
                    Response.Write("<script>alert('用户表导入失败，请检查表格式!');</script>");
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


        protected void classSaveButton_Click(object sender, EventArgs e)
        {
            string year = DateTime.Now.Year.ToString();
            MySqlConnection con = db.CreateConnection();
            string str1 = "select* from class where year=2017";  //判断是否存在教学大纲
            con.Open();
            MySqlDataAdapter msda = new MySqlDataAdapter(str1, con);
            DataSet ds1 = new DataSet();
            msda.Fill(ds1);
            if (ds1.Tables[0].Rows.Count == 0)
            {
                string strSql = " insert into class set classname='" + classNameTb.Text + "', point=" + classPointTb.Text + ", classtime=" + classTimeTb.Text + ", classplace='" + classPlaceTb.Text + "',teachername='" + classTeacherTb.Text + "', year = " + year;
                MySqlCommand cmd = new MySqlCommand(strSql, con);
                DataSet ds = new DataSet();
                MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
                cmd.ExecuteNonQuery();
                con.Close();
            }
            else
            {
                string strSql = " update class set classname='" + classNameTb.Text + "', point=" + classPointTb.Text + ", classtime=" + classTimeTb.Text + ", classplace='" + classPlaceTb.Text + "',teachername='" + classTeacherTb.Text + "'where year = " + year;
                MySqlCommand cmd = new MySqlCommand(strSql, con);
                DataSet ds = new DataSet();
                MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
                cmd.ExecuteNonQuery();
                con.Close();
            }

        }
    }
}