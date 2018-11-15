using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MySql.Data.MySqlClient;

namespace WebApplication1
{
    public class db
    {
        public db()
        {
            //  
            //TODO: 在此处添加构造函数逻辑  
            //  
        }
        public static MySqlConnection CreateConnection()
        {
            string str = "Server=127.0.0.1;User ID=root;Password=paopao;Database=oeap;CharSet=gbk;";
            MySqlConnection con = new MySqlConnection(str);//实例化链接
            return con;
        }
    }
}