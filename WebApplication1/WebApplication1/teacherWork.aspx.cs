using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace WebApplication1
{
    public partial class teacherWork : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)

            {

                GridViewBind();      //调用绑定数据信息函数
                GridViewBind1();

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

            MySqlDataAdapter adsa = new MySqlDataAdapter("select  thwtitle ,tcommand,thwst ,thwed  from thomework", sqlcon);

            DataSet ds = new DataSet();

            adsa.Fill(ds);

            if (ds.Tables[0].Rows.Count >= 0)

            {

                GridView1.DataSource = ds;

                GridView1.DataBind();

            }

            sqlcon.Close();

        }
        public void GridViewBind1()

        {


            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            MySqlDataAdapter adsa = new MySqlDataAdapter("select  thwtitle  from thomework", sqlcon);

            DataSet ds = new DataSet();

            adsa.Fill(ds);

            if (ds.Tables[0].Rows.Count >= 0)

            {

                GridView2.DataSource = ds;

                GridView2.DataBind();

            }

            sqlcon.Close();

        }

        //protected void newHomeworkButton_Click(object sender, EventArgs e)
        //{
        //    Response.Redirect("teacherNewWork.aspx");
        //}

        private void shuaxin()

        {

            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            MySqlDataAdapter da = new MySqlDataAdapter(@"select * from thomework", sqlcon);

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

        protected void GridView1_RowDeleting(object sender, GridViewDeleteEventArgs e)
        {
            string sqlstr = "delete from thomework where thwtitle='" + GridView1.DataKeys[e.RowIndex].Value.ToString() + "'";
            MySqlConnection sqlcon = db.CreateConnection();
            MySqlCommand sqlcom = new MySqlCommand(sqlstr, sqlcon);
            sqlcon.Open();
            sqlcom.ExecuteNonQuery();
            sqlcon.Close();
            this.shuaxin();
        }

        protected void GridView1_RowUpdating(object sender, GridViewUpdateEventArgs e)
        {
            MySqlConnection sqlcon = db.CreateConnection();
            string sqlstr = "update thomework set tcommand='"
               
                + ((TextBox)(GridView1.Rows[e.RowIndex].Cells[1].Controls[0])).Text.ToString().Trim() + "',thwst='"
                + ((TextBox)(GridView1.Rows[e.RowIndex].Cells[2].Controls[0])).Text.ToString().Trim() + "',thwed='"
                + ((TextBox)(GridView1.Rows[e.RowIndex].Cells[3].Controls[0])).Text.ToString().Trim() + "' where thwtitle='"
                + GridView1.DataKeys[e.RowIndex].Value.ToString() + "'";
            MySqlCommand sqlcom = new MySqlCommand(sqlstr, sqlcon);
            sqlcon.Open();
            sqlcom.ExecuteNonQuery();
            sqlcon.Close();
            GridView1.EditIndex = -1;
            this.shuaxin();
        }

        protected void newHomeworkButton_Click(object sender, EventArgs e)
        {
            Response.Redirect("teacherNewWork.aspx");
        }
    }
}