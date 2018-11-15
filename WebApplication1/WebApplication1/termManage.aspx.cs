using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using MySql.Data.MySqlClient;
using System.Data;

namespace WebApplication1
{
    public partial class termManage : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!Page.IsPostBack)
            {
                MySqlConnection con = db.CreateConnection();
                con.Open();
                string strSql = "select* from term limit 0,1";
                MySqlCommand cmd = new MySqlCommand(strSql, con);
                DataSet ds = new DataSet();
                MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
                MySqlDataReader dr = cmd.ExecuteReader();
                if (dr.Read())
                {
                    yearTb.Text = dr["year"].ToString();
                    termStartTb.Text = dr["bgtime"].ToString();
                    termEndTb.Text = dr["edtime"].ToString();
                    termWeekTb.Text = dr["week"].ToString();
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
        protected void startTermButton_Click(object sender, EventArgs e)
        {
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql = "delete from term; insert into term set year="+ yearTb.Text +", bgtime="+termStartTb.Text+", edtime="+termEndTb.Text+", week="+termWeekTb.Text;
            MySqlCommand cmd = new MySqlCommand(strSql, con);
            DataSet ds = new DataSet();
            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
            cmd.ExecuteNonQuery();
            con.Close();
            
        }

        protected void endTermButton_Click(object sender, EventArgs e)
        {
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql = "delete from term";
            MySqlCommand cmd = new MySqlCommand(strSql, con);
            DataSet ds = new DataSet();
            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
            cmd.ExecuteNonQuery();
            con.Close();
            Response.Write("<script>alert('学期结束!')</script>");
        }
    }
}