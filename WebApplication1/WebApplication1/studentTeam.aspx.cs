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
    public partial class studentTeam : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                GridViewBind();
            }
            /*MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql;
            for (int i = 0; i < this.GridView1.Rows.Count; i++)
            {
                strSql =
                "select contribute from student where userid = '" + this.GridView1.Rows[i].Cells[1].Text + "'";
                MySqlCommand cmd = new MySqlCommand(strSql, con);
                DataSet ds = new DataSet();
                MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
                da.Fill(ds, "table1");
                TextBox txt = (TextBox)this.GridView1.Rows[i].Cells[0].FindControl("contribute");
                if (txt != null)
                {
                    txt.Text = ds.Tables["table1"].Rows[0]["contribute"].ToString();
                }
            }
            con.Close();*/
        }
        public void GridViewBind()
        {

            MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql =
                "select name,userid,sex " +
                "from student where teamid = (select teamid from student where userid = '" + Session["username"] + "')";
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

        protected void gradeButton_Click(object sender, EventArgs e)
        {

            MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql =
                "select leadid from student where userid = '" + Session["username"] + "'";
            MySqlCommand cmd = new MySqlCommand(strSql, con);
            DataSet ds = new DataSet();
            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
            da.Fill(ds, "table1");
            if (Session["username"].ToString() == ds.Tables["table1"].Rows[0]["leadid"].ToString())
            {
                TextBox txt = (TextBox)this.GridView1.Rows[0].Cells[0].FindControl("contribute");
                try
                {
                    Double[] mygrade = new Double[50];
                    for (int i = 0; i < this.GridView1.Rows.Count; i++)
                    {
                        txt = (TextBox)this.GridView1.Rows[i].Cells[0].FindControl("contribute");
                        if (txt != null)
                        {
                            string str = txt.Text;
                            mygrade[i] = Convert.ToDouble(str);
                        }
                    }
                    Double allgrade = 0;
                    for (int i = 0; i < this.GridView1.Rows.Count; i++)
                    {
                        allgrade += mygrade[i];
                    }
                    if (allgrade / this.GridView1.Rows.Count == 1)
                    {
                        try
                        {
                            for (int i = 0; i < this.GridView1.Rows.Count; i++)
                            {
                                strSql =
                                "update student set contribute =" + mygrade[i] + " where userid = '" + this.GridView1.Rows[i].Cells[1].Text + "'";
                                cmd = new MySqlCommand(strSql, con);
                                cmd.ExecuteNonQuery();
                            }
                            Response.Write("<script>alert('打分成功 请于刷新后查看')</script>");
                        }
                        catch
                        {
                            Response.Write("<script>alert('TAT  出现未知错误')</script>");
                        }
                    }
                    else
                    {
                        Response.Write("<script>alert('请核对数据，确保贡献度平均值为1')</script>");
                    }
                }
                catch
                {
                    Response.Write("<script>alert('录入数据出错')</script>");
                }


            }
            else
            {
                Response.Write("<script>alert('抱歉，你没有权限修改')</script>");
            }

            con.Close();
        }
    }
}