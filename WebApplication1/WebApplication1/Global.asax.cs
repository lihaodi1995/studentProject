using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Security;
using System.Web.SessionState;

namespace WebApplication1
{
    public class Global : System.Web.HttpApplication
    {

        protected void Application_Start(object sender, EventArgs e)
        {
            // 在应用程序启动时运行的代码

            //建立用户列表

            string user = "";//用户列表

            Application["user"] = user;

            Application["userNum"] = 0;

            string chats = "";//聊天记录 

            Application["chats"] = chats;

            //当前的聊天记录数

            Application["current"] = 0;
        }

        protected void Session_Start(object sender, EventArgs e)
        {

        }

        protected void Application_BeginRequest(object sender, EventArgs e)
        {

        }

        protected void Application_AuthenticateRequest(object sender, EventArgs e)
        {

        }

        protected void Application_Error(object sender, EventArgs e)
        {

        }

        protected void Session_End(object sender, EventArgs e)
        {

        }

        protected void Application_End(object sender, EventArgs e)
        {
            // 在应用程序关闭时运行的代码

            Application["user"] = "";

            Application["chats"] = "";
        }
    }
}