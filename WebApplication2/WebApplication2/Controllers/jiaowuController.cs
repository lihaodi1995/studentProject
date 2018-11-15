using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Text;
using System.Data.Entity;
using System.Web.Mvc;
using WebApplication2.Models;
using Newtonsoft.Json;
using System.IO;
using Microsoft.Office.Interop.Excel;
using System.Web.Security;
using System.Net;
using System.Reflection;

namespace WebApplication2.Controllers
{
    public class jiaowuController : Controller
    {
        private database1Entities db = new database1Entities();

        private string str;

        public ActionResult Tojiaowu()
        {
            return RedirectToAction("jiaowu", "jiaowu");
        }
        public ActionResult LogOut()
        {
            return RedirectToAction("Login", "User");
        }
        public ActionResult ToaddClass()
        {
            return RedirectToAction("addClass", "jiaowu");
        }
        public ActionResult TocheckClass()
        {
            return RedirectToAction("checkClass", "jiaowu");
        }
        public ActionResult Tomanageblog()
        {
            return RedirectToAction("manageblog", "jiaowu");
        }
        public ActionResult Toshezhixueqixinxi()
        {
            return RedirectToAction("shezhixueqixinxi", "jiaowu");
        }
        public ActionResult Totianjiaxueshengxinxi()
        {
            return RedirectToAction("tianjiaxueshengxinxi", "jiaowu");
        }
        public ActionResult Toxueshengminglu()
        {
            return RedirectToAction("xueshengminglu", "jiaowu");
        }
        public ActionResult ToalterClass() { return RedirectToAction("alterClass", "jiaowu"); }
        public ActionResult Toxueqixinxi() { return RedirectToAction("xueqixinxi", "jiaowu"); }

        public ActionResult jiaowu()
        {
            return View();
        }
        public ActionResult alterClass()
        {
            return View();
        }
        public ActionResult addClass()
        {
            return View();
        }
        public ActionResult checkClass()
        {
            
            List<course> list = db.course.ToList();
            List<teacher> list1 = db.teacher.ToList();
            List<teachercourse> list2 = new List<teachercourse>();
            foreach (course c1 in list)
            {
                teachercourse tc = new teachercourse();
                tc.courseid = c1.course_id;
                tc.location = c1.location;
                tc.coursetime = c1.time;
                tc.coursename = c1.course_name;
                tc.credit = c1.credit.Value;
                foreach (teacher teacher1 in list1)
                {
                    if (teacher1.teacher_id == c1.teacher_id)
                        tc.teachername = teacher1.teacher_name;
                }
                list2.Add(tc);
            }
            //ViewBag.value = "ggggggg";

            return View(list2);
        }
        public ActionResult shezhixueqixinxi()
        {
            return View();
        }
        public ActionResult xueshengminglu()
        {
            List<student> stu = db.student.ToList();
            return View(stu);
        }
        public ActionResult manageblog()
        {
            return View();
        }
        public ActionResult xueqixinxi()
        {
            List<term> term1 = db.term.ToList();
            return View(term1);
        }
        public ActionResult tianjiaxueshengxinxi()
        { return View(); }

        public ActionResult ShowAlertAndHref(string msg, string actionName, object[] obj = null)
        {
            var script = String.Format("<script>alert('{0}');location.href='{1}'</script>", msg, Url.Action(actionName, obj));
            return Content(script, "text/html");
        }

        [HttpPost]
        public ActionResult shezhixueqixinxi(string name, DateTime starttime, DateTime endtime)
        {
            List<term> term1 = db.term.ToList();
            string finalValue = Session["教务修改学期信息"].ToString();
            if (finalValue == "添加")
            {
                if (starttime > endtime)
                {
                    return ShowAlertAndHref("起始时间大于终止时间", "shezhixueqixinxi");
                }
                else
                {
                    foreach (term t1 in term1)
                    {
                        if (t1.term_name == name)
                        {
                            return ShowAlertAndHref("已有该学期名称", "shezhixueqixinxi");
                        }
                    }
                    term t = new term();
                    t.term_name = name;
                    t.starttime = starttime;
                    t.endtime = endtime;
                    db.term.Add(t);
                    db.SaveChanges();
                }
            }
            else if (finalValue.Contains("修改"))
            {
                if (starttime > endtime)
                {
                    return ShowAlertAndHref("起始时间大于终止时间", "shezhixueqixinxi");
                }
                string finalValue1 = finalValue.Substring(0, finalValue.Length - 5);//现在的finalValue就是课程名称
                foreach (term t in term1)
                {
                    if (t.term_name == finalValue1)
                    {
                        t.term_name = name;
                        t.starttime = starttime;
                        t.endtime = endtime;
                        db.Entry(t).State = EntityState.Modified;
                        db.SaveChanges();
                        break;
                    }
                }
            }
            return ShowAlertAndHref("提交成功", "xueqixinxi");
            //return RedirectToAction("xueqixinxi", "jiaowu");
        }

        [HttpPost]
        public ActionResult xueqixinxi(string alterbutton)
        {
            if (alterbutton.Contains("添加"))
            {
                string finalValue = alterbutton.Substring(0, alterbutton.Length);
                Session["教务修改学期信息"] = finalValue;
                return RedirectToAction("shezhixueqixinxi", "jiaowu");
            }
            else
            {
                if (alterbutton.Contains("选中了") == false)
                {
                    return RedirectToAction("xueqixinxi", "jiaowu");
                }
                else if (alterbutton.Contains("删除"))
                {
                    string finalValue = alterbutton.Substring(0, alterbutton.Length - 5);//现在的finalValue就是课程名称
                    List<term> teamlist = db.term.ToList();
                    int couid = 0;
                    foreach (term cou in teamlist)
                    {
                        if (cou.term_name == finalValue)
                            couid = cou.term_id;
                    }
                    term cc = db.term.Find(couid);
                    db.term.Remove(cc);
                    db.SaveChanges();
                    return RedirectToAction("xueqixinxi", "jiaowu");
                }
                else
                {
                    string finalValue = alterbutton.Substring(0, alterbutton.Length);
                    Session["教务修改学期信息"] = finalValue;
                    return RedirectToAction("shezhixueqixinxi", "jiaowu");
                }
            }
        }



        [HttpPost]
        public ActionResult checkClass(string alterbutton)
        {
            if (alterbutton.Contains("选中了")==false)
            {
                return RedirectToAction("checkClass", "jiaowu");
            }
            if (alterbutton.Contains("修改"))
            {
                string finalValue = alterbutton.Substring(0, alterbutton.Length - 5);//现在的finalValue就是课程名称
                str = finalValue;
                Session["教务修改课程信息"] = finalValue;
                //Console.WriteLine("alterbutton" + alterbutton);
                return RedirectToAction("alterClass", "jiaowu");
            }
            else if (alterbutton.Contains("删除"))
            {
                string finalValue = alterbutton.Substring(0, alterbutton.Length - 5);//现在的finalValue就是课程名称
                List<course> coulist = db.course.ToList();
                int couid = 0;
                foreach (course cou in coulist)
                {
                    if (cou.course_name == finalValue)
                        couid = cou.course_id;
                }
                course cc = db.course.Find(couid);
                db.course.Remove(cc);
                db.SaveChanges();
                return RedirectToAction("checkClass", "jiaowu");
            }
            return RedirectToAction("alterClass", "jiaowu");
        }

        [HttpPost]
        public ActionResult addClass(string name, string teacher, string location, string time, int credit)
        {
            List<course> ll = db.course.ToList();
            List<teacher> t1 = db.teacher.ToList();
            //Console.WriteLine("132456789");
            int teaid = 0; bool flag = false;
            foreach (teacher tea in t1)
            {
                if (tea.teacher_name == teacher)
                { teaid = tea.teacher_id; flag = true; }
            }
            if (flag == false)
            {
                return ShowAlertAndHref("没有这名老师", "addClass");
            }
            foreach (course cou1 in ll)
            {
                if (cou1.course_name == name)
                    return ShowAlertAndHref("已有该课程名称", "addClass");
            }
            course cou = new course();
            cou.course_name = name;
            cou.teacher_id = teaid;
            cou.time = time;
            cou.credit = credit;
            cou.location = location;
            db.course.Add(cou);
            db.SaveChanges();
            return ShowAlertAndHref("添加成功", "checkClass");
        }

        [HttpPost]
        public ActionResult alterClass(string name, string teacher, string location, string time, int credit)
        {
            List<course> ll = db.course.ToList();
            List<teacher> t1 = db.teacher.ToList();
            //Console.WriteLine("132456789");
            string s = Session["教务修改课程信息"].ToString();
            int teaid = 0; bool flag = false;
            foreach (teacher tea in t1)
            {
                if (tea.teacher_name == teacher)
                { teaid = tea.teacher_id; flag = true; }
            }
            if (flag == false)
            {
                return ShowAlertAndHref("没有这名老师", "alterClass");
            }
            foreach (course cou in ll)
            {
                if (cou.course_name == s)
                {
                    cou.course_name = name;
                    cou.teacher_id = teaid;
                    cou.time = time;
                    cou.credit = credit;
                    cou.location = location;
                    db.Entry(cou).State = EntityState.Modified;
                    db.SaveChanges();
                }
            }
            return ShowAlertAndHref("修改成功", "checkClass");
        }


        public string batchAddStudents(HttpPostedFileBase file)
        {
            var severPath = this.Server.MapPath("/StudentExcel/");
            Directory.CreateDirectory(severPath);
            var savePath = Path.Combine(severPath, file.FileName);
            string result = "{}";
            try
            {
                if (string.Empty.Equals(file.FileName) || ".xlsx" != Path.GetExtension(file.FileName))
                {
                    return "error";
                }

                file.SaveAs(savePath);
                //启动Excel应用程序
                Microsoft.Office.Interop.Excel.Application xls = new Microsoft.Office.Interop.Excel.Application();
                //打开filename表
                _Workbook book = xls.Workbooks.Open(savePath, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value, Missing.Value);

                _Worksheet sheet;//定义sheet变量
                xls.Visible = false;//设置Excel后台运行
                xls.DisplayAlerts = false;//设置不显示确认修改提示

                try
                {
                    sheet = (_Worksheet)book.Worksheets.get_Item(1);//获得第index个sheet，准备读取
                }
                catch (Exception ex)//不存在就退出
                {
                    Console.WriteLine(ex.Message);
                    return null;
                }
                Console.WriteLine(sheet.Name);
                int row = sheet.UsedRange.Rows.Count;//获取不为空的行数
                int col = sheet.UsedRange.Columns.Count;//获取不为空的列数
                // Array value = (Array)sheet.get_Range(sheet.Cells[1, 1], sheet.Cells[row, col]).Cells.Value2;//获得区域数据赋值给Array数组，方便读取\
                string tempId;
                string tempName;
                string tempTel;
                int idcol = -1;
                int idrow = -1;
                int namecol = -1;
                int telcol = -1;
                for (var i = 1; i <= row; i++)
                {
                    for (var j = 1; j <= col; j++)
                    {
                        tempId = ((Range)sheet.Cells[i, j]).Text;
                        if (tempId.Equals("学号"))
                        {
                            idcol = j;
                            idrow = i;
                        }
                        if (tempId.Equals("姓名"))
                        {
                            namecol = j;
                        }
                        if (tempId.Equals("联系方式"))
                        {
                            telcol = j;
                        }
                    }

                    if (idcol >= 0 && idrow >= 0)
                    {
                        break;
                    }
                }


                for (var i = idrow + 1; i <= row; i++)
                {
                    tempId = ((Range)sheet.Cells[i, idcol]).Text;
                    tempName = ((Range)sheet.Cells[i, namecol]).Text;
                    tempTel = ((Range)sheet.Cells[i, telcol]).Text;
                    if (isInt(tempId) && tempName != "")
                    {
                        //student user = new Models.User();
                        student stu1 = new student();
                        stu1.student_id = int.Parse(tempId);
                        stu1.student_name = tempName;
                        stu1.tel = tempTel;
                        //user.setUserType("student");
                        stu1.password = "1";
                        db.student.Add(stu1);
                        db.SaveChanges();

                    }
                    
                }

                



                book.Save();//保存
                book.Close(false, Missing.Value, Missing.Value);//关闭打开的表
                xls.Quit();//Excel程序退出
                //sheet,book,xls设置为null，防止内存泄露
                sheet = null;
                book = null;
                xls = null;
                GC.Collect();//系统回收资源
                //System.IO.File.Delete(savePath);
                result = "{}";
            }
            catch (Exception e)
            {
                result = "{\"error\":\"在服务器端发生错误请联系管理员\" "+e.Message+ "}";
            }
            finally
            {
                //System.IO.File.Delete(savePath);
           }
            return result;
        }
        private bool isInt(string s)
        {
            int i = 0;
            try
            {
                i = int.Parse(s);
            }
            catch (Exception e)
            {
                return false;
            }

            return true;
        }

        public string Test()
        {
            return "";
        }
    }
}