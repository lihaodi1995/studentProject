using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication2.Models
{
    public class teachercourse
    {
        public int courseid { get; set; }
        public string teachername { get; set; }
        public string location { get; set; }
        public string coursetime { get; set; }
        public int credit { get; set; }
        public string info { get; set; }
        public string coursename { get; set; }
        public int term { get; set; }
        public string require { get; set; }
        public int score { get; set; }
    }
}