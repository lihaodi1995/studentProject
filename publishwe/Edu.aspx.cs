using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class Edu : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        Response.Clear();

        DataClassesDataContext dc = new DataClassesDataContext();
        var semester = from x in dc.semester where x.id == 1 select x;
        if (semester.Count()>0)
        {
            string response = "<tr>";
            response += "<td>" + semester.First().startTime + "</td><td>" + semester.First().endTime + "</td><td>" + semester.First().weekNumber.ToString() + "</td>";
            response += "</tr>";
            Response.Write(response);
            Response.End();
        }
    }
}