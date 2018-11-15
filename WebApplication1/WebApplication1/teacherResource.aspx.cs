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
    public partial class teacherResource : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)

            {

                GridViewBind();      //调用绑定数据信息函数

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

            MySqlDataAdapter adsa = new MySqlDataAdapter("select sourceid,sourcename from source where type =2 or type=3 or type=4", sqlcon);

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

            MySqlDataAdapter da = new MySqlDataAdapter(@"select * from source  where type =2 or type=3 or type=4", sqlcon);

            DataSet ds = new DataSet();

            da.Fill(ds);

            if (ds.Tables[0].Rows.Count >= 0)

            {

                GridView1.DataSource = ds;

                GridView1.DataBind();

            }

            sqlcon.Close();

        }
        protected void resourceBtn_Click(object sender, EventArgs e)
        {
            string type = resourceType.SelectedValue;
            string typeid = null;
            switch (type)
            {
                case "课件":
                    typeid = "2";
                    break;
                case "文档":
                    typeid = "3";
                    break;
                case "视频":
                    typeid = "4";
                    break;
            }
            //if (resourceUpload.HasFile)
            // {
            string filename = resourceUpload.FileName;
            string filepaths = Server.MapPath(("\\\\upfiles\\\\") + filename);
            Response.Write("<script>alert('" + filepaths + "');</script>");
            string filepath = filepaths.ToString().Replace("\\", "\\\\");
            resourceUpload.SaveAs(filepath);
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string sql = "insert source(sourcename,address,type) values('" + filename + "','" + filepath + "'," + typeid + ")";
            MySqlCommand cmd = new MySqlCommand(sql, con);
            cmd.ExecuteNonQuery();
            con.Close();
            //   }
            this.shuaxin();
        }
        protected void GridView1_RowDeleting(object sender, GridViewDeleteEventArgs e)
        {
            string id = GridView1.DataKeys[e.RowIndex].Value.ToString();
            string sqlstr = "delete from source where sourceid ='" + id+"'";
            string sqlstr2 = "select address from source where sourceid = '" + id+"'";

            MySqlConnection sqlcon = db.CreateConnection();
            sqlcon.Open();

            MySqlCommand cmd = new MySqlCommand(sqlstr2, sqlcon);
            MySqlDataReader reader = cmd.ExecuteReader();
            string filepath;
            if (reader.Read())
            {
                filepath = reader[0].ToString();

                try
                {
                    if (File.Exists(filepath))
                        File.Delete(filepath);
                }
                catch { }

            }
            reader.Close();

            MySqlCommand sqlcom = new MySqlCommand(sqlstr, sqlcon);
            sqlcom.ExecuteNonQuery();
            sqlcon.Close();
            this.shuaxin();
            
        }

        protected void GridView1_RowDataBound(object sender, GridViewRowEventArgs e)
        {
            e.Row.Cells[1].Visible = false;
            if (e.Row.RowType == DataControlRowType.DataRow)
            {
                e.Row.Cells[0].Text = (e.Row.RowIndex + 1).ToString();

                ////如果使用了分页控件且希望序号在翻页后不重新计算，使用下面方法  
                //int indexID = (AspNetPager1.CurrentPageIndex - 1) * AspNetPager1.PageSize + e.Row.RowIndex + 1;  
                //e.Row.Cells[0].Text = indexID.ToString();  
            }
        }
    }
}