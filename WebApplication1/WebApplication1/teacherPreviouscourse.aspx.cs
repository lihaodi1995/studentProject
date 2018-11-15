using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using MySql.Data.MySqlClient;
using System.Data;
using System.IO;

namespace WebApplication1
{
    public partial class teacherPreviouscourse : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                GridViewBind();
            }
        }
        protected void logout()
        {
            Session.Remove("username");
            Session.Remove("password");
            Response.Redirect("WebForm1.aspx");
        }
        public void GridViewBind()
        {


            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            MySqlDataAdapter adsa = new MySqlDataAdapter("select  year ,classname,classplace,classtime,point from class", sqlcon);

            DataSet ds = new DataSet();

            adsa.Fill(ds);

            if (ds.Tables[0].Rows.Count > 0)
            {

                GridView1.DataSource = ds;

                GridView1.DataBind();

            }

            sqlcon.Close();

        }
        private void shuaxin()
        {

            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            MySqlDataAdapter da = new MySqlDataAdapter(@"select * from class", sqlcon);

            DataSet ds = new DataSet();

            da.Fill(ds);

            if (ds.Tables[0].Rows.Count >= 0)
            {

                GridView1.DataSource = ds;

                GridView1.DataBind();

            }

            sqlcon.Close();

        }

        protected void GridView1_RowCommand(object sender, GridViewCommandEventArgs e)
        {
            if (e.CommandName == "download")
            {
                string filename = e.CommandArgument.ToString();
                string filepath=Server.MapPath(("\\\\upfiles\\\\") + filename + ".zip");
                download(filepath);
            }
        }
        private void download(string fileurl)
        {
            string fileURL = fileurl;//文件路径，可用相对路径
            FileInfo fileInfo = new FileInfo(fileURL);
            Response.Clear();
            Response.AddHeader("content-disposition", "attachment;filename=" + Server.UrlEncode(fileInfo.Name.ToString()));//文件名
            Response.AddHeader("content-length", fileInfo.Length.ToString());//文件大小
            Response.ContentType = "application/octet-stream";
            Response.ContentEncoding = System.Text.Encoding.Default;
            Response.WriteFile(fileURL);
        }
    }
}