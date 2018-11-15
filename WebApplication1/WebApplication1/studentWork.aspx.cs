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
    public partial class studentWork : System.Web.UI.Page
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
        protected void GridViewBind()
        {
            MySqlConnection con = db.CreateConnection();
            string sql = "select thwid,thwtitle,thwst,thwed, thwtimes from thomework";
            con.Open();
            MySqlDataAdapter adapter = new MySqlDataAdapter(sql, con);
            DataSet ds = new DataSet();
            adapter.Fill(ds);
            if (ds.Tables[0].Rows.Count > 0)
            {

                GridView1.DataSource = ds;
                GridView1.DataBind();

            }
            con.Close();
        }
    }
}