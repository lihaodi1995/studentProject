using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using MySql.Data.MySqlClient;
using System.Data;
using System.Collections;

namespace WebApplication1
{
    public partial class teacherTeam : System.Web.UI.Page
    {
        private string teamid;
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                GridViewBind();      //调用绑定数据信息函数
                GridView2Bind();
                setStudentSource();
                setIDSource();
            }
        }
        public void GridViewBind()
        {


            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();
            string sql = "select team.teamid,team.teamname,student.name,team.teammem from student join team on team.teamid = student.teamid where student.userid = team.leadid";
            MySqlDataAdapter adsa = new MySqlDataAdapter(sql, sqlcon);

            DataSet ds = new DataSet();

            adsa.Fill(ds);

            if (ds.Tables[0].Rows.Count >= 0)
            {

                GridView1.DataSource = ds;

                GridView1.DataBind();

            }
            sqlcon.Close();

        }
        public void GridView2Bind()
        {

            MySqlConnection sqlcon = db.CreateConnection();

            sqlcon.Open();
            string sql = "select teamname,teamrequest.leadid,GROUP_CONCAT(name separator ',') as member,name " +
                "from student,teamrequest where student.leadid = teamrequest.leadid group by leadid";

            MySqlDataAdapter adsa = new MySqlDataAdapter(sql, sqlcon);

            DataSet ds = new DataSet();

            adsa.Fill(ds);

            if (ds.Tables[0].Rows.Count >= 0)
            {

                GridView2.DataSource = ds;

                GridView2.DataBind();
            }
            sqlcon.Close();
        }

        protected void requestSolve(object sender, GridViewCommandEventArgs e)
        {
            int index = Convert.ToInt32(e.CommandArgument.ToString());
            string leadid = this.GridView2.Rows[index].Cells[0].Text;
            string teamname = this.GridView2.Rows[index].Cells[2].Text;
            MySqlConnection con = db.CreateConnection();
            if (e.CommandName == "accept")
            {
                con.Open();
                string memNumSql = "select count(userid) as memNum from student where leadid ='" + leadid + "'";//计算团队人数
                MySqlCommand cmd2 = new MySqlCommand(memNumSql, con);
                MySqlDataReader reader = cmd2.ExecuteReader();
                string memNum = null;
                if (reader.Read())
                {
                    memNum = reader[0].ToString();
                }
                reader.Close();
                string sql = "replace team(leadid,teamname,teammem) values('" + leadid + "','" + teamname + "'," + memNum + ")"; //往团队表中加数据             
                MySqlCommand cmd = new MySqlCommand(sql, con);
                cmd.ExecuteNonQuery();
                string sql2 = "select teamid from team where leadid ='" + leadid + "'";//查找团队id
                MySqlCommand cmd3 = new MySqlCommand(sql2, con);
                MySqlDataReader read = cmd3.ExecuteReader();
                string teamid = null;
                if (read.Read())
                    teamid = read[0].ToString();
                read.Close();
                string sql4 = "update student set teamid = " + teamid + ",teamprocess = 1 where leadid ='" + leadid + "'"; //学生表中插入团队id
                MySqlCommand cmd4 = new MySqlCommand(sql4, con);
                cmd4.ExecuteNonQuery();
                string sql5 = "delete from teamrequest where leadid ='" + leadid + "'";//删除团队申请表中的数据
                MySqlCommand cmd5 = new MySqlCommand(sql5, con);
                cmd5.ExecuteNonQuery();
                con.Close();
                Response.Write("<script>alert('已批准团队组建')</script>");

            }
            else if (e.CommandName == "reject")
            {
                con.Open();

                string sql2 = "update student set leadid = null where leadid = '" + leadid + "'";
                MySqlCommand cmd2 = new MySqlCommand(sql2, con);
                cmd2.ExecuteNonQuery();
                string sql = "delete from teamrequest where leadid ='" + leadid + "'";
                MySqlCommand cmd = new MySqlCommand(sql, con);
                cmd.ExecuteNonQuery();
                con.Close();
                Response.Write("<script>alert('已驳回团队组建请求')</script>");
            }
            GridViewBind();
            GridView2Bind();
        }

        protected void addNewMember(object sender, EventArgs e)
        {
            string username = droplist.SelectedValue;
            string teamid = droplistTeamid.SelectedValue;
            string leadid = null;
            string sql2 = "select leadid from team where teamid = " + teamid;

            MySqlConnection con = db.CreateConnection();
            con.Open();

            MySqlCommand cmd2 = new MySqlCommand(sql2, con);
            MySqlDataReader read = cmd2.ExecuteReader();
            if (read.Read())
                leadid = read[0].ToString();
            read.Close();
            string sql = "update student set teamid =" + teamid + " ,leadid = '" + leadid + "',teamprocess = 1 where name ='" + username + "'";
            MySqlCommand cmd = new MySqlCommand(sql, con);

            cmd.ExecuteNonQuery();
            string sql3 = "update team set teammem = teammem + 1 where teamid =" + teamid;
            MySqlCommand cmd3 = new MySqlCommand(sql3, con);
            cmd3.ExecuteNonQuery();

            con.Close();
            setIDSource();
            setStudentSource();
            GridViewBind();
            Response.Write("<script>alert('已成功添加队员')</script>");
        }
        protected void setStudentSource()
        {
            ArrayList listSource = new ArrayList();
            ArrayList listID = new ArrayList();
            string sql = "select name from student where leadid is null";
            MySqlConnection con = db.CreateConnection();
            con.Open();
            MySqlCommand cmd = new MySqlCommand(sql, con);
            MySqlDataReader reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                listSource.Add(reader[0].ToString());
            }
            reader.Close();
            droplist.DataSource = listSource;
            droplist.DataBind();
            con.Close();
        }
        protected void setIDSource()
        {
            ArrayList listID = new ArrayList();
            MySqlConnection con = db.CreateConnection();
            con.Open();
            string sql2 = "select teamid from team";
            MySqlCommand cmd2 = new MySqlCommand(sql2, con);
            MySqlDataReader reader2 = cmd2.ExecuteReader();
            while (reader2.Read())
            {
                listID.Add(reader2[0].ToString());
            }
            reader2.Close();
            droplistTeamid.DataSource = listID;
            droplistTeamid.DataBind();
            con.Close();
        }
    }
}