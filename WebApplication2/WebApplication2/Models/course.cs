//------------------------------------------------------------------------------
// <auto-generated>
//     此代码已从模板生成。
//
//     手动更改此文件可能导致应用程序出现意外的行为。
//     如果重新生成代码，将覆盖对此文件的手动更改。
// </auto-generated>
//------------------------------------------------------------------------------

namespace WebApplication2.Models
{
    using System;
    using System.Collections.Generic;
    
    public partial class course
    {
        public int course_id { get; set; }
        public Nullable<int> term_id { get; set; }
        public string course_name { get; set; }
        public string location { get; set; }
        public string time { get; set; }
        public Nullable<int> teacher_id { get; set; }
        public Nullable<int> credit { get; set; }
        public string requirement { get; set; }
        public string outline { get; set; }
        public Nullable<int> maxsize { get; set; }
        public Nullable<int> minsize { get; set; }
    }
}