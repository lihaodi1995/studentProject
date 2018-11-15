using System;
using System.Data;
using System.Configuration;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;
using System.IO;
using System.Linq;

public partial class download : System.Web.UI.Page
{
    public void DownLoad(string FName)
    {
        string path = FName;
        System.IO.FileInfo file = new System.IO.FileInfo(path);
        HttpResponse response = HttpContext.Current.Response;
        if (file.Exists)
        {
            Response.Write("upload/" + file.Name+",");
           
        }
        else
        {
            Response.Write("This file does not exist.");
            Response.End();
        }

    }
    protected void Page_Load(object sender, EventArgs e)
    {
        var re1 = Request.QueryString["sourceid"];
        DataClassesDataContext dc = new DataClassesDataContext();
        var re = re1.Split(',');
        for (int i = 0; i < re.Length; i++)
        {
            if (Convert.ToInt32(re[i]) != 0)
            {
                var res = from x in dc.sources where x.sourcesID.ToString() == re[i] select x;
                string FileName = res.First().sourcesName;

                string filePath = Server.MapPath("~/upload/" + FileName);

                DownLoad(filePath);
            }
        }
        Response.End();
        /*
        Response.ContentType = "application/x-zip-compressed";
        
        //使用UTF-8对文件名进行编码  
        Response.AppendHeader("Content-Disposition", "attachment;filename=\"" + HttpUtility.UrlEncode(FileName, System.Text.Encoding.UTF8) + "\"");
        Response.ContentType = "application/octet-stream";
        Response.AddHeader("Content-Disposition", "attachment;filename=" + FileName);
        string filename = Server.MapPath("~/upload/"+FileName);
        Response.TransmitFile(filePath);
        Response.End();
         * */
    }
    public string GetContentType(string fileExt)
    {
        string ContentType;
        switch (fileExt)
        {
            case ".asf":
                ContentType = "video/x-ms-asf"; break;
            case ".avi":
                ContentType = "video/avi"; break;
            case ".doc":
                ContentType = "application/msword"; break;
            case ".zip":
                ContentType = "application/zip"; break;
            case ".xls":
                ContentType = "application/vnd.ms-excel"; break;
            case ".gif":
                ContentType = "image/gif"; break;
            case ".jpg":
                ContentType = "image/jpeg"; break;
            case ".jpeg":
                ContentType = "image/jpeg"; break;
            case ".wav":
                ContentType = "audio/wav"; break;
            case ".mp3":
                ContentType = "audio/mpeg3"; break;
            case ".mpg":
                ContentType = "video/mpeg"; break;
            case ".mepg":
                ContentType = "video/mpeg"; break;
            case ".rtf":
                ContentType = "application/rtf"; break;
            case ".html":
                ContentType = "text/html"; break;
            case ".htm":
                ContentType = "text/html"; break;
            case ".txt":
                ContentType = "text/plain"; break;
            default:
                ContentType = "application/octet-stream";
                break;
        }
        return ContentType;
    }  
}