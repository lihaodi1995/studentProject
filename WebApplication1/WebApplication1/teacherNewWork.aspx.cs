using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using MySql.Data.MySqlClient;

namespace WebApplication1
{
    public partial class teacherNewWork : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
        }
        protected void cancleBtn_Click(object sender, EventArgs e)
        {
            Response.Redirect("teacherWork.aspx");
        }
        protected void hwRelease_Click(object sender, EventArgs e)
        {
            string title = hwTitle.Text;
            string bgTime = hwBegintime.Value;
            string endTime = hwEndtime.Value;
            string hwrequire = statustext.InnerText;
            string times = hwTimes.Text;
            string part = hwParts.Text;
            if (title == null)
            {
                Response.Write("<script>alert('请输入标题!')</script>");
                return;
            }
            if (bgTime == null)
            {
                Response.Write("<script>alert('请输入开始时间!')</script>");
                return;
            }
            if (endTime == null)
            {
                Response.Write("<script>alert('请输入结束时间!')</script>");
                return;
            }
            if (hwrequire == null)
            {
                Response.Write("<script>alert('请输入要求!')</script>");
                return;
            }
            if (part == null)
            {
                Response.Write("<script>alert('请输入占分比例!')</script>");
                return;
            }
            if (times == null)
            {
                Response.Write("<script>alert('请输入限交次数!')</script>");
                return;
            }
            MySqlConnection con = db.CreateConnection();
            try
            {
                string sql1 = "select sum(thwpart) as part from thomework";
                con.Open();
                MySqlCommand cmd1 = new MySqlCommand(sql1, con);
                MySqlDataReader reader = cmd1.ExecuteReader();
                while (reader.Read())
                {
                    string sumPart = reader[0].ToString();
                    if (sumPart == "")
                        break;
                    double sum = Convert.ToDouble(sumPart);
                    double left = 1 - sum;

                    double partNow = Convert.ToDouble(part);
                    if (sum + partNow > 1)
                    {
                        Response.Write("<script>alert('总占分比已超过1，请重新输入!剩余占分比为：" + Convert.ToString(left) + "')</script>");
                        return;
                    }
                }
                reader.Close();
                string sql = "insert into thomework (thwtitle,thwst,thwed,tcommand,thwtimes,thwpart) values('" + title + "','" + bgTime + "','" + endTime + "','" + hwrequire + "'," + times + "," + part + ")";
                MySqlCommand cmd = new MySqlCommand(sql, con);
                cmd.ExecuteNonQuery();
                con.Close();
                Response.Redirect("teacherwork.aspx");
            }
            catch
            {
                Response.Write("<script>alert('发布失败!')</script>");
            }
        }
    }
}