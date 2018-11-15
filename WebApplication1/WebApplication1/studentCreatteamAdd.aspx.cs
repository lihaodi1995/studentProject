using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using MySql.Data.MySqlClient;
using System.Data;
using System.Data.OleDb;

namespace WebApplication1
{
    public partial class studentCreatteamAdd : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                GridViewBind();
            }
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql = "select teamname from teamrequest where leadid=" +
                "(select leadid from student where userid='" + Session["username"] + "')";

            MySqlCommand cmd = new MySqlCommand(strSql, con);
            DataSet ds = new DataSet();
            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
            da.Fill(ds, "table1");
            try
            {
               teamname.Text = ds.Tables["table1"].Rows[0]["teamname"].ToString();
            }
            catch
            {
                teamname.Text = "尚未录入数据";
            }
            strSql = "select name from student where userid=" +
                "(select leadid from student where userid='" + Session["username"] + "')";
            cmd = new MySqlCommand(strSql, con);
            da = new MySqlDataAdapter(strSql, con);
            da.Fill(ds, "table1");
            try
            {
                leadname.Text = ds.Tables["table1"].Rows[1]["name"].ToString();
            }
            catch
            {
                leadname.Text = "尚未录入数据";
            }
            strSql = "select leadid from student where userid='" + Session["username"] + "'";
            cmd = new MySqlCommand(strSql, con);
            da = new MySqlDataAdapter(strSql, con);
            da.Fill(ds, "table1");
            try
            {
                leadid.Text = ds.Tables["table1"].Rows[2]["leadid"].ToString();
            }
            catch
            {
                leadid.Text = "尚未录入数据";
            }
            strSql = "select teamprocess from student where userid='" + Session["username"] + "'";
            cmd = new MySqlCommand(strSql, con);
            da = new MySqlDataAdapter(strSql, con);
            da.Fill(ds, "table1");
            try
            {
                string myteamprocess = ds.Tables["table1"].Rows[3]["teamprocess"].ToString();
                if ( myteamprocess == "1")
                {
                    teamprocess.Text = "老师通过";
                }
                else if (myteamprocess == "2")
                {
                    teamprocess.Text = "队长通过";
                }
                else if (myteamprocess == "3")
                {
                    teamprocess.Text = "审核中";
                }
                else
                {
                    teamprocess.Text = "拒绝";
                }
            }
            catch
            {
                teamprocess.Text = "拒绝";
            }
            con.Close();

        }
        public void GridViewBind()
        {
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql =
                "select teamname,teamrequest.leadid,GROUP_CONCAT(name separator ',') as member,name " +
                "from student,teamrequest where (student.leadid = teamrequest.leadid and student.teamprocess=2 ) group by leadid";
            MySqlCommand cmd = new MySqlCommand(strSql, con);
            DataSet ds = new DataSet();
            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
            da.Fill(ds, "table1");
            if (ds.Tables[0].Rows.Count > 0)
            {

                GridView1.DataSource = ds;
                GridView1.DataBind();

            }
            con.Close();
        }
        protected void GridView1_OnRowCommand(object sender, GridViewCommandEventArgs e)
        {
            if (e.CommandName == ("requestClick"))
            {
                MySqlConnection con = db.CreateConnection();
                con.Open();
                string strSql = "select teamprocess from student where userid='" + Session["username"] + "'";
                MySqlCommand cmd = new MySqlCommand(strSql, con);
                DataSet ds = new DataSet();
                MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
                da.Fill(ds, "table1");
                if (ds.Tables["table1"].Rows[0]["teamprocess"].ToString()=="")
                {
                    try
                    {
                        //GridViewRow row = (GridViewRow)((Control)e.CommandSource).Parent.Parent;
                        //string leadid = row.Cells[2].Text;
                        int RowIndex = Convert.ToInt32(e.CommandArgument);
                        DataKey keys = GridView1.DataKeys[RowIndex];
                        string myleadid = keys.Value.ToString();
                        strSql =
                            "update student set leadid = '" + myleadid + "' ,teamprocess = 3 where userid = '" + Session["username"] + "'";
                        cmd = new MySqlCommand(strSql, con);
                        ds = new DataSet();
                        da = new MySqlDataAdapter(strSql, con);
                        cmd.ExecuteNonQuery();
                        con.Close();
                        Response.Write("<script>alert('申请团队成功，请在刷新页面后查看信息,等待审核')</script>");
                    }
                    catch
                    {
                        Response.Write("<script>alert('TAT  出现错误')</script>");
                    }
                }
                else
                {
                    Response.Write("<script>alert('你已经有团队')</script>");
                }
            }
        }

        /*protected void GridView1_RowCreated(object sender, GridViewRowEventArgs e)
        {
            if (e.Row.RowType != DataControlRowType.DataRow) return;

            if (e.Row.FindControl("Button1") != null)
            {
                Button CtlButton = (Button)e.Row.FindControl("Button1");
                CtlButton.Click += new EventHandler(CtlButton_Click);
            }
        }

        private void CtlButton_Click(object sender, EventArgs e)
        {
            Button button = (Button)sender;
            GridViewRow gvr = (GridViewRow)button.Parent.Parent;
            string pk = GridView1.DataKeys[gvr.RowIndex].Value.ToString();
            Response.Write("<script>alert('申请团队成功，请等待审核')</script>");
            //do something


            //objJs.JsAlert(pk);
        }*/
    }
}