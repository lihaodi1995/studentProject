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
    
    public partial class assignment
    {
        public int assignment_id { get; set; }
        public Nullable<int> course_id { get; set; }
        public Nullable<System.DateTime> starttime { get; set; }
        public Nullable<System.DateTime> deadline { get; set; }
        public string requirement { get; set; }
        public Nullable<int> sub_max_times { get; set; }
        public Nullable<int> proportion { get; set; }
        public string assignment_name { get; set; }
    }
}
