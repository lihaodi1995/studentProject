using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using MySql.Data.MySqlClient;
using System.Data;
using Ionic.Zip;

namespace WebApplication1
{
    public partial class studentResource : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                string sql = "select sourceid,sourcename,address,type from source where type=2 or type=3 or type=4";
                GridViewBind(sql);      //调用绑定数据信息函数

            }
        }
        protected void logout()
        {
            Session.Remove("username");
            Session.Remove("password");
            Response.Redirect("WebForm1.aspx");
        }
        public void GridViewBind(string sql)
        {


            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            MySqlDataAdapter adsa = new MySqlDataAdapter(sql, sqlcon);

            DataSet ds = new DataSet();
            adsa.Fill(ds);

            if (ds.Tables[0].Rows.Count > 0)
            {

                GridView1.DataSource = ds;

                GridView1.DataBind();

            }

            sqlcon.Close();
        }
        public void showResource_Click(object sender, EventArgs e)
        {
            string sql = "select sourceid,sourcename,address,type from source where type=2 or type=3 or type=4";
            string type = resourceType.SelectedValue;
            switch (type)
            {
                case "课件":
                    sql = "select sourceid,sourcename,address,type from source where type = 2 ";
                    break;
                case "文档":
                    sql = "select sourceid,sourcename,address,type from source where type = 3";
                    break;
                case "视频":
                    sql = "select sourceid,sourcename,address,type from source where type = 4 ";
                    break;
                default:
                    break;
            }
            GridViewBind(sql);
        }
        protected void CheckBox_Click(object sender, EventArgs e)
        {
            CheckBox checkBox = sender as CheckBox;
            foreach (GridViewRow row in GridView1.Rows)
            {
                if (row.RowType == DataControlRowType.DataRow)
                {
                    (row.Cells[0].FindControl("checkBox2") as CheckBox).Checked = checkBox.Checked;
                }
            }
        }
        //批量下载
        protected void downLoad_Click(object sender, EventArgs e)
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
                        Response.Write("<script>alert('" + gvr.Cells[4].Text + "');</script>");
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