using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace WebApplication1
{
    public partial class studentChat : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            Application.Lock();

            string[] messages = Application["chats"].ToString().Split(',');//把Application里的聊天记录拿出来,用，号分隔成数组
            contentTextBox.Text = "";

            for (int i = 0; i <= messages.Length - 1; i++)

            {

                contentTextBox.Text += messages[i] + "\n";

            }

            int current = Convert.ToInt32(Application["current"]);

            ArrayList ItemList = new ArrayList();

            string zs_name;       //已在线的用户名

            string[] user;        //在线用户的数组





            int num = Convert.ToInt32(Application["userNum"]);

            zs_name = Application["user"].ToString();

            user = zs_name.Split(',');

            for (int i = (num - 1); i >= 0; i--)

            {

                if (user[i].ToString() != "")

                    ItemList.Add(user[i].ToString());

            }

     

            Application.UnLock();
        }

        protected void Button1_Click(object sender, EventArgs e)
        {
            contentTextBox.Text = "";

            int current = Convert.ToInt32(Application["current"]);

            Application["chats"] = Application["chats"].ToString() + "," + Session["userName"].ToString() + "说：" + messageTextBox.Text.Trim() + "(" + DateTime.Now.ToString() + ")";

            current += 1;

            Application["current"] = current;



            string chats = Application["chats"].ToString();

            string[] chat = chats.Split(',');//定义一个存放消息的数组，用,号分隔开
           
            {

                for (int i = chat.Length - 1; i >= 0; i--)

                {

                    if (current == 0)

                    {

                        contentTextBox.Text = chat[i].ToString();

                    }

                    else

                    {

                        contentTextBox.Text = chat[i].ToString() + "\n" + contentTextBox.Text;

                    }

                }
            }

            Application.UnLock();



            messageTextBox.Text = "";

            messageTextBox.Focus();
        }

        protected void Button2_Click(object sender, EventArgs e)
        {
            Page_Load( sender,  e);
        }
        protected void logout()
        {
            Session.Remove("username");
            Session.Remove("password");
            Application.Lock();

            string userName = Application["user"].ToString();

            Application["user"] = userName.Replace(Session["userName"].ToString(), "");

            Application.UnLock();

            Response.Write("<script>window.opener=null;window.close();</script>");
            Response.Redirect("WebForm1.aspx");
        }
    }
}