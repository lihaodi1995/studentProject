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
    public partial class studentWorkDetails : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            string id = Request.QueryString["thwid"];
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string strSql = "select *  from thomework where thwid='" + id + "'";
            MySqlCommand cmd = new MySqlCommand(strSql, con);
            DataSet ds = new DataSet();
            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
            da.Fill(ds, "table1");
            try
            {
                thwtitle.Text = ds.Tables["table1"].Rows[0]["thwtitle"].ToString();
                thwst.Text = ds.Tables["table1"].Rows[0]["thwst"].ToString();
                thwed.Text = ds.Tables["table1"].Rows[0]["thwed"].ToString();
                tcommand.Text = ds.Tables["table1"].Rows[0]["tcommand"].ToString();
            }
            catch
            {
                thwtitle.Text = "尚未录入数据";
                thwst.Text = "尚未录入数据";
                thwed.Text = "尚未录入数据";
                tcommand.Text = "尚未录入数据";
            }
            con.Close();
        }

        //protected void Upload1Button_Click(object sender, EventArgs e)
        //{
        //    DateTime dt = System.DateTime.Now;
        //    string time1 = thwst.Text;
        //    string time2 = thwed.Text;
        //    DateTime bgTime = Convert.ToDateTime(time1);
        //    DateTime endTime = Convert.ToDateTime(time2);
        //    if (DateTime.Compare(dt, bgTime) > 0 && DateTime.Compare(dt, endTime) < 0)
        //    {
        //        string id = Request.QueryString["thwid"];
        //        try
        //        {
        //            MySqlConnection con = db.CreateConnection();
        //            con.Open();
        //            string strSql = "insert into shomework (teamid,thwid) select " +
        //                "(select teamid from student where userid = " + Session["username"] + ")," + id +
        //                " from dual where not exists (select * from shomework where teamid = " +
        //                "(select teamid from student where userid = " + Session["username"] + ") and thwid = " + id + ")" +
        //                ";update shomework set shwtxt = " + shwtxt.Text + " where teamid = " +
        //                "(select teamid from student where userid = " + Session["username"] + ") and thwid = " + id;
        //            MySqlCommand cmd = new MySqlCommand(strSql, con);
        //            DataSet ds = new DataSet();
        //            MySqlDataAdapter da = new MySqlDataAdapter(strSql, con);
        //            cmd.ExecuteNonQuery();
        //            con.Close();
        //            Response.Write("<script>alert('上传作业成功')</script>");
        //        }
        //        catch
        //        {
        //            Response.Write("<script>alert('TAT   出现了未知的错误！')</script>");
        //        }
        //    }
        //    else
        //    {
        //        Response.Write("<script>alert('现在不能提交')</script>");
        //    }
        //}
        protected void Upload2Button_Click(object sender, EventArgs e)
        {
            DateTime dt = System.DateTime.Now;
            string time1 = thwst.Text;
            string time2 = thwed.Text;
            DateTime bgTime = Convert.ToDateTime(time1);
            DateTime endTime = Convert.ToDateTime(time2);
            if (DateTime.Compare(dt, bgTime) > 0 && DateTime.Compare(dt, endTime) < 0)
            {
                string id = Request.QueryString["thwid"];
                //try
                {
                    string filename = MyUpload.FileName;
                    string filepaths = Server.MapPath(("\\\\upfiles\\\\") + filename);
                    string filepath = filepaths.ToString().Replace("\\", "\\\\");
                    MyUpload.SaveAs(filepath);
                    MySqlConnection con = db.CreateConnection();
                    con.Open();
                    string sql1 = "select times from shomework where thwid='" + id + "' and teamid=(select teamid from student where userid = " + Session["username"] + ")";
                    string sql2 = "select thwtimes from thomework where thwid='" + id + "'";
                    MySqlCommand cmd1 = new MySqlCommand(sql1, con);
                    MySqlCommand cmd2 = new MySqlCommand(sql2, con);
                    string thwtimes = "";
                    MySqlDataReader reader1 = cmd2.ExecuteReader();
                    if (reader1.Read())
                    {
                        thwtimes = reader1[0].ToString();
                    }
                    reader1.Close();
                    reader1 = cmd1.ExecuteReader();

                    string strSql = "";
                    if (reader1.Read())
                    {
                        //Response.Write("<script>alert('"+ reader1[0].ToString() + "')</script>");
                        string sumPart = reader1[0].ToString();
                        if (sumPart == thwtimes)
                        {
                            Response.Write("<script>alert('上传达到次数上限')</script>");
                        }
                        else
                        {
                            strSql = "insert into shomework (teamid,thwid) select " +
                       "(select teamid from student where userid = " + Session["username"] + ")," + id +
                       " from dual where not exists (select * from shomework where teamid = " +
                       "(select teamid from student where userid = " + Session["username"] + ") and thwid = " + id + ")" +
                       ";update shomework set  shwtxt ='" + shwtxt.Text + "',times=times+1,shwname = '" + filename + "' , shwaddress = '" + filepath + "' where teamid = " +
                       "(select teamid from student where userid = " + Session["username"] + ") and thwid = " + id;
                            reader1.Close();
                            MySqlCommand cmd = new MySqlCommand(strSql, con);
                            cmd.ExecuteNonQuery();
                            con.Close();
                            Response.Write("<script>alert('更新作业成功')</script>");
                        }
                    }
                    else
                    {
                        strSql = "insert into shomework (teamid,thwid) select " +
                   "(select teamid from student where userid = " + Session["username"] + ")," + id +
                   " from dual where not exists (select * from shomework where teamid = " +
                   "(select teamid from student where userid = " + Session["username"] + ") and thwid = " + id + ")" +
                   ";update shomework set  shwtxt ='" + shwtxt.Text + "',times=1,shwname = '" + filename + "' , shwaddress = '" + filepath + "' where teamid = " +
                   "(select teamid from student where userid = " + Session["username"] + ") and thwid = " + id;
                        reader1.Close();
                        MySqlCommand cmd = new MySqlCommand(strSql, con);
                        cmd.ExecuteNonQuery();
                        con.Close();
                        Response.Write("<script>alert('上传作业成功')</script>");
                    }
                }
                //catch
                //{
                //    Response.Write("<script>alert('TAT   出现了未知的错误！')</script>");
                //}
            }
            else
            {
                Response.Write("<script>alert('现在不能提交！')</script>");
            }

        }
    }
}