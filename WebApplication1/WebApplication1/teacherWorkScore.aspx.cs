using Ionic.Zip;
using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace WebApplication1
{
    public partial class teacherWorkScore : System.Web.UI.Page
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
            string thwTitle = Request.QueryString["thwtitle"];

            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            MySqlDataAdapter adsa = new MySqlDataAdapter("select  teamid,shwname,shwgrade,shwaddress from shomework where thwid in (select thwid from thomework where thwtitle='" + thwTitle + "')", sqlcon);

            DataSet ds = new DataSet();

            adsa.Fill(ds);

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
                //Response.Write("<script>alert('"+filename+"');</script>");
                //string fileName = "下载内容.xlsx";//客户端保存的文件名  
                //string filePath = Server.MapPath("upfiles/工作簿1.xlsx");//路径  

                //FileInfo fileInfo = new FileInfo(filePath);
                //Response.Clear();
                //Response.ClearContent();
                //Response.ClearHeaders();
                //Response.AddHeader("Content-Disposition", "attachment;filename=" + filename);
                //Response.AddHeader("Content-Length", fileInfo.Length.ToString());
                //Response.AddHeader("Content-Transfer-Encoding", "binary");
                //Response.ContentType = "application/octet-stream";
                //Response.ContentEncoding = System.Text.Encoding.GetEncoding("gb2312");
                //Response.WriteFile(fileInfo.FullName);
                //Response.Flush();
                //Response.End();
                download(filename);
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
        private void shuaxin()

        {

            string thwTitle = Request.QueryString["thwtitle"];

            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            MySqlDataAdapter da = new MySqlDataAdapter("select  teamid,shwname,shwgrade,shwaddress from shomework where thwid in (select thwid from thomework where thwtitle='" + thwTitle + "')", sqlcon);

            DataSet ds = new DataSet();

            da.Fill(ds);

            if (ds.Tables[0].Rows.Count >= 0)

            {

                GridView1.DataSource = ds;

                GridView1.DataBind();

            }

            sqlcon.Close();

        }
        protected void GridView1_RowEditing(object sender, GridViewEditEventArgs e)
        {
            GridView1.EditIndex = e.NewEditIndex;

            this.shuaxin();
        }

        protected void GridView1_RowCancelingEdit(object sender, GridViewCancelEditEventArgs e)
        {
            GridView1.EditIndex = -1;
            this.shuaxin();
        }

        protected void GridView1_RowUpdating(object sender, GridViewUpdateEventArgs e)
        {
            MySqlConnection sqlcon = db.CreateConnection();
            string sqlstr = "update shomework set shwgrade='"


                + ((TextBox)(GridView1.Rows[e.RowIndex].Cells[3].Controls[0])).Text.ToString().Trim() + "' where shwname='"
               + GridView1.DataKeys[e.RowIndex].Value.ToString() + "'";
            MySqlCommand sqlcom = new MySqlCommand(sqlstr, sqlcon);
            sqlcon.Open();
            sqlcom.ExecuteNonQuery();
            sqlcon.Close();
            GridView1.EditIndex = -1;
            this.shuaxin();
        }

        protected void PackDown_Click(object sender, EventArgs e)
        {
            Response.Clear();
            Response.ContentType = "application/zip";
            Response.AddHeader("content-disposition", "filename=DotNetZip.zip");
            using (ZipFile zip = new ZipFile(System.Text.Encoding.Default))//解决中文乱码问题  
            {
                foreach (GridViewRow gvr in GridView1.Rows)
                {
                    if (((CheckBox)gvr.Cells[0].Controls[1]).Checked)
                    {
                        Response.Write("<script>alert('"+ gvr.Cells[4].Text+"');</script>"); 
                        zip.AddFile((gvr.Cells[4]).Text, "");
                    }
                }

                zip.Save(Response.OutputStream);
            }

            Response.End();
        }

        protected void GridView1_RowDataBound(object sender, GridViewRowEventArgs e)
        {
            e.Row.Cells[4].Visible = false;
        }
    }
}