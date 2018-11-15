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
    public partial class studentCreateteamNew : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)

            {

                GridViewBind();      //调用绑定数据信息函数
                GridViewBind1();

            }
        }
        public void GridViewBind()

        {


            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            String str = "select  name ,studentid,case when sex=1 then'男'else  '女' end as sex from student where leadid = (select leadid from student where userid='" + Session["username"] + "')and teamprocess = 2";

            MySqlDataAdapter adsa = new MySqlDataAdapter(str, sqlcon);

            DataSet ds = new DataSet();

            adsa.Fill(ds);


            if (ds.Tables[0].Rows.Count > 0)

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

            String str = "select  name ,studentid,case when sex=1 then'男'else  '女' end as sex from student where leadid = (select leadid from student where userid='" + Session["username"] + "')and teamprocess = 3";

            MySqlDataAdapter adsa = new MySqlDataAdapter(str, sqlcon);

            DataSet ds = new DataSet();

            adsa.Fill(ds);


            if (ds.Tables[0].Rows.Count > 0)

            {

                GridView2.DataSource = ds;

                GridView2.DataBind();


            }

            sqlcon.Close();

        }
        private void shuaxin()

        {

            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();

            MySqlDataAdapter da1 = new MySqlDataAdapter(@"select  name ,studentid,case when sex=1 then'男'else  '女' end as sex from student where leadid = (select leadid from student where userid='" + Session["username"] + "')and teamprocess = 3", sqlcon);
            MySqlDataAdapter da = new MySqlDataAdapter(@"select  name ,studentid,case when sex=1 then'男'else  '女' end as sex from student where leadid = (select leadid from student where userid='" + Session["username"] + "')and teamprocess = 2", sqlcon);
            DataSet ds1 = new DataSet();
            DataSet ds = new DataSet();
            da1.Fill(ds1);
            da.Fill(ds);
            if (ds.Tables[0].Rows.Count >= 0)

            {

                GridView1.DataSource = ds;

                GridView1.DataBind();

            }
            if (ds1.Tables[0].Rows.Count >= 0)

            {

                GridView2.DataSource = ds1;

                GridView2.DataBind();

            }

            sqlcon.Close();
        }
        protected void GridView1_RowCommand(object sender, GridViewCommandEventArgs e)
        {
            string studentid = e.CommandArgument.ToString();
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql = "select leadid from student where userid='" + Session["username"] + "'";
            MySqlCommand cmd = new MySqlCommand(strSql, con);
            DataSet ds = new DataSet();
            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
            MySqlDataReader dr = cmd.ExecuteReader();
            dr.Read();
            if (e.CommandName == "deny")
            {
                if (Session["username"].ToString() == dr["leadid"].ToString())
                {
                    string sqlstr = "update student set leadid=null where studentid='" + studentid + "';update student set teamprocess=null where studentid='" + studentid + "'";
                    MySqlConnection sqlcon = db.CreateConnection();
                    MySqlCommand sqlcom = new MySqlCommand(sqlstr, sqlcon);
                    sqlcon.Open();
                    sqlcom.ExecuteNonQuery();
                    sqlcon.Close();
                    this.shuaxin();
                }
                else
                {
                    Response.Write("<script>alert('很抱歉您没有权限执行此操作')</script>");
                }
            }
            else if (e.CommandName == "access")
            {
                if (Session["username"].ToString() == dr["leadid"].ToString())
                {
                    string sqlstr = "update student set teamprocess=2 where studentid='" + studentid + "'";
                    MySqlConnection sqlcon = db.CreateConnection();
                    MySqlCommand sqlcom = new MySqlCommand(sqlstr, sqlcon);
                    sqlcon.Open();
                    sqlcom.ExecuteNonQuery();
                    sqlcon.Close();
                    this.shuaxin();
                }
                else
                {
                    Response.Write("<script>alert('很抱歉您没有权限执行此操作')</script>");
                }
            }
        }


        protected void CreateTeam_Click(object sender, EventArgs e)
        {
            if (teamname.Text == "")
            {
                Response.Write("<script>alert('请输入团队名称')</script>");
            }
            else
            {
                try
                {

                    string newTeamName = teamname.Text;
                    MySqlConnection con = db.CreateConnection();
                    con.Open();
                    string strSql = "select leadid from student where userid='" + Session["username"] + "'";
                    MySqlCommand cmd1 = new MySqlCommand(strSql, con);
                    MySqlDataReader dr1 = cmd1.ExecuteReader();
                    dr1.Read();
                    if (dr1["leadid"] != DBNull.Value)
                    {
                        Response.Write("<script>alert('您已创建或加入过团队')</script>");
                    }
                    else
                    {
                        MySqlConnection con1 = db.CreateConnection();
                        con1.Open();
                        string str = "insert into teamrequest  values('" + Session["username"] + "','" + newTeamName + "');update student set leadid='" + Session["username"] + "'where userid='" + Session["username"] + "';update student set teamprocess=2 where userid='" + Session["username"] + "'";
                        MySqlCommand cmd = new MySqlCommand(str, con1);
                        DataSet ds = new DataSet();
                        MySqlDataAdapter da = new MySqlDataAdapter(str, con1);
                        cmd.ExecuteNonQuery();
                        con1.Close();
                        Response.Write("<script>alert('创建团队成功')</script>");
                        this.shuaxin();
                    }

                }
                catch
                {
                    Response.Write("<script>alert('创建团队失败')</script>");
                }
            }
        }
    }
}