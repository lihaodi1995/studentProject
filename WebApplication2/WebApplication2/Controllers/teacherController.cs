using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Web;
using System.Web.Mvc;
using WebApplication2.Models;


namespace WebApplication2.Controllers
{
    public class teacherController : Controller
    {
        private database1Entities db = new database1Entities();
        private string str;
        // GET: teachers
        public ActionResult Index()
        {
            return View("Teacher_first");
        }

        public ActionResult LogOut()
        {
            return RedirectToAction("Login", "User");
        }

        public ActionResult teacher() { return View(); }
        public ActionResult Teacher_addHomework() { return View(); }
        public ActionResult Teacher_checkTeam() { return View(); }
        public ActionResult Teacher_classresource() { return View(); }
        public ActionResult Teacher_classresourcelist() { return View(); }
        public ActionResult Teacher_getresource() { return View(); }
        public ActionResult Teacher_getresource0() { return View(); }
        public ActionResult Teacher_HomeworkCtrl() { return View(); }
        public ActionResult Teacher_homeworkdafen() { return View(); }
        public ActionResult Teacher_setClassMessage() { return View(); }
        public ActionResult Teacher_studentTeamCtrl() { return View(); }



        public ActionResult Teacher_chatOL()
        {
            getscore();
            List<student> list1 = db.student.ToList();
            return View(list1);
        }



        public void getscore()
        {
            List<student> stu = db.student.ToList();
            List<score> sc = db.score.ToList();
            List<submission> sub = db.submission.ToList();
            List<assignment> ass = db.assignment.ToList();
            List<team> team1 = db.team.ToList();
            double allpro = 0;
            foreach (assignment assign in ass)
            {
                allpro += assign.proportion.Value;
            }
            foreach (student s in stu)
            {
                double tid = 0, tsize = 0;
                double afinal = 0;
                double sfinal = 0;
                double a = 0;
                if (s.score != null)
                { a = s.score.Value; }
                if (s.team_id == null) { s.ratio = 0; }
                else
                {
                    tid = s.team_id.Value;
                    double[] aratio = new double[100];
                    double[] sratio = new double[100];
                    int i = 0, j = 0;
                    foreach (team ttt in team1)
                    {
                        if (ttt.team_id == tid)
                            tsize = ttt.teamsize.Value;
                    }
                    foreach (student s1 in stu)
                    {
                        if (s1.team_id == tid)
                        {
                            if (s1.score == null) { aratio[i] = 0; }
                            else
                                aratio[i] = s1.score.Value;
                            i++;
                        }
                    }
                    foreach (submission ss in sub)
                    {
                        if (ss.team_id == tid)
                        {
                            if (ss.score == null) { sratio[i] = 0; }
                            else
                                sratio[j] = ss.score.Value;
                            foreach (assignment assi in ass)
                            {
                                if (assi.assignment_id == ss.assignment)
                                    sratio[j] = sratio[j] * assi.proportion.Value;
                            }
                            j++;
                        }
                    }
                    for (int k = 0; k < i; k++)
                    {
                        afinal += aratio[k];
                    }
                    for (int k = 0; k < j; k++)
                    {
                        sfinal += sratio[k];
                    }
                    if (afinal == 0) { s.ratio = 0; }
                    else
                    {
                        double hh = tsize * sfinal / allpro;
                        double hhh = a / afinal;
                        double final = hh * hhh;
                        string s121323 = Math.Ceiling(final).ToString();
                        s.ratio = int.Parse(s121323);
                        if (s.ratio > 100)
                            s.ratio = 100;
                    }

                }
                db.Entry(s).State = EntityState.Modified;
                db.SaveChanges();
            }
        }

        public ActionResult Teacher_checkJoin()
        {
            string s = Session["教师选择查看申请加入团队编号"].ToString();
            int id = int.Parse(s);
            int teamid = (id + 2) / 3;
            int leaderid = 0;
            List<student> stu = db.student.ToList();
            List<team> t = db.team.ToList();
            foreach (team tt in t)
            {
                if (tt.team_id == teamid)
                    leaderid = tt.leader_id.Value;
            }
            List<student> stlist = new List<student>();
            foreach (student st in stu)
            {
                if (st.student_id == leaderid)
                    stlist.Add(st);
            }
            foreach (student st in stu)
            {
                if (st.team_id == teamid && st.student_id != leaderid)
                    stlist.Add(st);
            }
            return View(stlist);
        }

        [HttpPost]
        public ActionResult Teacher_homeworkdafen(int mark)
        {
            string cid = Session["教师选择查看布置的作业"].ToString();
            string tid = Session["教师选择团队作业打分"].ToString();
            int assid = int.Parse(cid);
            int teamid = int.Parse(tid);
            List<submission> sc = db.submission.ToList();
            foreach (submission s in sc)
            {
                if (s.assignment == assid && s.team_id == teamid)
                {
                    s.score = mark;
                    db.Entry(s).State = EntityState.Modified;
                    db.SaveChanges();
                }
            }
            return RedirectToAction("Teacher_homeworkchakan", "teacher");
        }

        public ActionResult Teacher_checkNewTeam()
        {
            List<team> team1 = (from team2 in db.team where team2.status == 0 select team2).ToList();
            if (team1.Count == 0)
            {
                return ShowAlertAndHref("没有待审核的团队", "Teacher_studentTeamCtrl");
            }
            List<studentteam> st = new List<studentteam>();
            List<student> stu = db.student.ToList();
            foreach (team t in team1)
            {
                studentteam studentteam1 = new studentteam();
                studentteam1.teamname = t.team_name;
                foreach (student s in stu)
                {
                    if (s.student_id == t.leader_id)
                        studentteam1.leadername = s.student_name;
                }
                studentteam1.teamid = t.team_id * 3;
                studentteam1.teamid2 = t.team_id * 3 - 1;
                studentteam1.teamid3 = t.team_id * 3 - 2;
                studentteam1.teamcount = t.teamsize.Value;
                studentteam1.status = t.status.Value;
                st.Add(studentteam1);
            }
            return View(st);
        }

        public ActionResult Teacher_detailMessage()
        {
            string s = Session["教师选择查看团队编号"].ToString();
            int teamid = int.Parse(s);
            int leaderid = 0;
            List<student> stu = db.student.ToList();
            List<team> t = db.team.ToList();
            foreach (team tt in t)
            {
                if (tt.team_id == teamid)
                    leaderid = tt.leader_id.Value;
            }
            List<student> stlist = new List<student>();
            foreach (student st in stu)
            {
                if (st.student_id == leaderid)
                    stlist.Add(st);
            }
            foreach (student st in stu)
            {
                if (st.team_id == teamid && st.student_id != leaderid)
                    stlist.Add(st);
            }
            return View(stlist);
        }

        public ActionResult setclassprogramme()
        {
            return View();
        }

        [HttpPost]
        public ActionResult setclassprogramme(string yourworks, HttpPostedFileBase file)
        {
            course c = db.course.Find(9);

            c.outline = yourworks;

            db.Entry(c).State = EntityState.Modified;
            db.SaveChanges();

            return RedirectToAction("classprogramme", "teacher");
        }

        public ActionResult Teacher_setClassRequire()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Teacher_setClassRequire(string yourworks, int max)
        {
            course c = db.course.Find(9);
            c.requirement = yourworks;
            c.maxsize = max;

            db.Entry(c).State = EntityState.Modified;
            db.SaveChanges();

            return RedirectToAction("classrequire", "teacher");
        }


        public ActionResult classprogramme()
        {
            List<course> list1 = db.course.ToList();
            course course1 = list1[0];
            ViewData["课程大纲"] = course1.outline;
            return View();
        }

        public ActionResult Teacher_homeworkCheck()
        {
            List<assignment> listass = db.assignment.ToList();
            List<ass> ass1 = new List<ass>();
            foreach (assignment a in listass)
            {
                ass a1 = new ass();
                a1.assname = a.assignment_name;
                a1.assid = a.assignment_id * 2 - 1;
                a1.assid2 = a.assignment_id * 2;
                ass1.Add(a1);
            }
            return View(ass1);
        }

        [HttpPost]
        public ActionResult Teacher_homeworkCheck(string alterbutton)
        {
            int buttonid = int.Parse(alterbutton);
            int assid = 0;
            bool flag = true;
            if (buttonid % 2 == 0)
            {
                assid = buttonid / 2;
            }
            else
            {
                assid = (buttonid + 1) / 2;
                flag = false;
            }
            List<assignment> ass = db.assignment.ToList();
            if (flag == false)
            {
                foreach (assignment a in ass)
                {
                    if (a.assignment_id == assid)
                    {
                        db.assignment.Remove(a);
                        db.SaveChanges();
                        break;
                    }
                }
                return RedirectToAction("Teacher_homeworkCheck", "teacher");
            }
            Session["教师查看作业id"] = assid.ToString();
            return RedirectToAction("Teacher_checksingle", "teacher");
        }

        public ActionResult Teacher_checksingle()
        {
            if (Session["教师删除或查看作业"].ToString() == "删除")
                return RedirectToAction("Teacher_homeworkCheck", "teacher");
            string id = Session["教师查看作业id"].ToString();
            List<assignment> ass = db.assignment.ToList();
            foreach (assignment a in ass)
            {
                if (a.assignment_id.ToString() == id)
                {
                    ViewData["作业内容"] = a.requirement;
                    Session["作业要求"] = a.requirement;
                    ViewData["提交时间"] = a.deadline;
                    ViewData["作业占比"] = a.proportion;
                }
            }
            return View();

        }

        public ActionResult Teacher_homeworkpinggu()
        {
            List<assignment> list2 = db.assignment.ToList();
            return View(list2);
        }

        public ActionResult Teacher_homeworkchakan()
        {
            string ss = Session["教师选择查看布置的作业"].ToString();
            int id = int.Parse(ss);
            List<submission> sub = db.submission.ToList();
            List<submission> teamsub = new List<submission>();
            foreach (submission a in sub)
            {
                if (a.assignment == id)
                {
                    submission s = new submission();
                    s.team_id = a.team_id;
                    if (a.score == null)
                        s.score = 0;
                    else
                    { s.score = a.score; }
                    teamsub.Add(s);
                }
            }
            return View(teamsub);
        }

        public ActionResult ShowAlertAndHref(string msg, string actionName, object[] obj = null)
        {
            var script = String.Format("<script>alert('{0}');location.href='{1}'</script>", msg, Url.Action(actionName, obj));
            return Content(script, "text/html");
        }

        public ActionResult Teacher_browseMessage()
        {
            List<team> team1 = (from team2 in db.team where team2.status == 1 select team2).ToList();
            if (team1.Count == 0)
            {
                return ShowAlertAndHref("没有已通过的团队", "Teacher_studentTeamCtrl");
            }
            List<studentteam> st = new List<studentteam>();
            List<student> stu = db.student.ToList();
            foreach (team t in team1)
            {
                studentteam studentteam1 = new studentteam();
                studentteam1.teamname = t.team_name;
                foreach (student s in stu)
                {
                    if (s.student_id == t.leader_id)
                        studentteam1.leadername = s.student_name;
                }
                studentteam1.teamcount = t.teamsize.Value;
                studentteam1.teamid = t.team_id;
                st.Add(studentteam1);
            }
            return View(st);
        }

        [HttpPost]
        public ActionResult Teacher_addHomework(string name, string yourworks, DateTime time, int score)
        {
            if (time < DateTime.Now)
            {
                return ShowAlertAndHref("时间已过", "Teacher_addHomework");
            }
            List<assignment> ass1 = db.assignment.ToList();
            foreach (assignment a in ass1)
            {
                if (a.assignment_name == name)
                    return ShowAlertAndHref("已有该作业名称", "Teacher_addHomework");
            }
            assignment ass = new assignment();
            ass.assignment_name = name;
            ass.requirement = yourworks;
            ass.deadline = time;
            ass.proportion = score;
            db.assignment.Add(ass);
            db.SaveChanges();
            return ShowAlertAndHref("添加成功", "Teacher_homeworkCheck");
        }

        public ActionResult Teacher_changeHomework()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Teacher_changeHomework(string yourworks, DateTime time, int score)
        {
            if (time < DateTime.Now)
            {
                return ShowAlertAndHref("时间已过", "Teacher_changeHomework");
            }
            int a = 0;
            List<assignment> listass = db.assignment.ToList();
            foreach (assignment ass in listass)
            {
                if (ass.requirement == Session["作业要求"].ToString())
                    a = ass.assignment_id;
            }
            assignment assig = db.assignment.Find(a);
            assig.requirement = yourworks;
            assig.deadline = time;
            assig.proportion = score;

            db.Entry(assig).State = EntityState.Modified;
            db.SaveChanges();
            return ShowAlertAndHref("修改成功", "Teacher_homeworkCheck");

        }


        public ActionResult classrequire()
        {
            List<course> list2 = db.course.ToList();
            List<teacher> list3 = db.teacher.ToList();
            List<teachercourse> list4 = new List<teachercourse>();
            foreach (course course1 in list2)
            {
                teachercourse tc = new teachercourse();
                tc.courseid = course1.course_id;
                tc.location = course1.location;
                tc.term = course1.term_id.Value;
                tc.coursetime = course1.time;
                tc.coursename = course1.course_name;
                tc.credit = course1.credit.Value;
                tc.info = course1.requirement;
                foreach (teacher teacher1 in list3)
                {
                    if (teacher1.teacher_id == course1.teacher_id)
                        tc.teachername = teacher1.teacher_name;
                }
                list4.Add(tc);
            }
            return View(list4);
        }

        //上传课程资源
        public string uploadResources(HttpPostedFileBase file)
        {
            var severPath = this.Server.MapPath("~/ClassResources/");
            Directory.CreateDirectory(severPath);
            var savePath = Path.Combine(severPath, file.FileName);
            string result = "{}";
            try
            {
                file.SaveAs(savePath);
            }
            catch (Exception e)
            {
                result = "{\"error\":\"在服务器端发生错误请联系管理员\"}";
            }
            finally
            {
                //System.IO.File.Delete(savePath);
            }
            return result;
        }
        //显示课程资源
        public string getClassResources(string folderPath)
        {
            string[] resultFile;
            var severPath = this.Server.MapPath("~/ClassResources/");

            Directory.CreateDirectory(severPath);
            try
            {
                resultFile = Directory.GetFiles(severPath);
                //resultDirectories = Directory.GetDirectories(severPath);
            }
            catch (Exception e)
            {
                return "error";
            }
            TeacherResource resource = new TeacherResource();
            resource.files = resultFile;
            //resource.directories = resultDirectories;
            return Newtonsoft.Json.JsonConvert.SerializeObject(resource);
        }

        public class TeacherResource
        {
            public string[] files { get; set; }
            public string[] directories { get; set; }
        }
        //上传课程大纲
        public string uploadProgram(HttpPostedFileBase file)
        {
            var severPath = this.Server.MapPath("~/ClassProgram/");
            Directory.CreateDirectory(severPath);
            var savePath = Path.Combine(severPath, file.FileName);
            string result = "{}";
            try
            {
                file.SaveAs(savePath);
            }
            catch (Exception e)
            {
                result = "{\"error\":\"在服务器端发生错误请联系管理员\"}";
            }
            finally
            {
                //System.IO.File.Delete(savePath);
            }
            return result;
        }
        //显示课程大纲
        public string getClassProgram(string folderPath)
        {
            string[] resultFile;
            var severPath = this.Server.MapPath("~/ClassProgram/");

            Directory.CreateDirectory(severPath);
            try
            {
                resultFile = Directory.GetFiles(severPath);
                //resultDirectories = Directory.GetDirectories(severPath);
            }
            catch (Exception e)
            {
                return "error";
            }
            TeacherResource resource = new TeacherResource();
            resource.files = resultFile;
            //resource.directories = resultDirectories;
            return Newtonsoft.Json.JsonConvert.SerializeObject(resource);
        }
        //删除课程资源
        public string deleteClassResource(string filename)
        {
            var severPath = this.Server.MapPath("~/ClassResources/");
            var filepath = severPath + filename;
            System.IO.File.Delete(filepath);
            string result = "1"; 
            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }
        //下载学生作业
        public string getHomework(string folderPath)
        {
            string[] resultFile;
            var severPath = this.Server.MapPath("~/Homework/");

            Directory.CreateDirectory(severPath);
            try
            {
                resultFile = Directory.GetFiles(severPath);
                //resultDirectories = Directory.GetDirectories(severPath);
            }
            catch (Exception e)
            {
                return "error";
            }
            TeacherResource resource = new TeacherResource();
            resource.files = resultFile;
            Session["curHomework"] = resultFile;
            //resource.directories = resultDirectories;
            return Newtonsoft.Json.JsonConvert.SerializeObject(resource);
        }

        public string SubFn(string Tid)
        {
            string fname="";
            List<assignment> ass = db.assignment.ToList();
            foreach(assignment as1 in ass)
            {
                if (as1.assignment_id == int.Parse(Session["教师选择查看布置的作业"].ToString()))
                {
                    fname = as1.assignment_name;
                    break;
                }
            }
            string[] resultFile;
            var severPath = this.Server.MapPath("~/Homework/");

            Directory.CreateDirectory(severPath);
            try
            {
                resultFile = Directory.GetFiles(severPath);
                //resultDirectories = Directory.GetDirectories(severPath);
            }
            catch (Exception e)
            {
                return "error";
            }
            
            int l = resultFile.Length;
            string[] sf = { "", "", "", "", "" };
            for (int i=0;i<l;i++)
            {
                List<submission> subl = db.submission.ToList();
                string[] ts = Regex.Split(resultFile[i],"Homework\\\\");
                string path="";
                foreach (submission s in subl)
                {
                    if(s.team_id==int.Parse(Tid)&&fname==db.assignment.Find(s.assignment).assignment_name)
                    {
                        path = s.sub_path;
                        break;
                    }
                }
                string[] tts = Regex.Split(path,"Homework");
                if (tts[tts.Length - 1] == "\\" + ts[ts.Length - 1])
                {
                    sf[0] = resultFile[i];
                    break;
                }
            }
            TeacherResource resource = new TeacherResource();
            resource.files = sf;
            //Session["curHomework"] = sf;
            return Newtonsoft.Json.JsonConvert.SerializeObject(resource);
        }


        public string TT(String id) //修改作业
        {
            var result = id;
            Teacher_homeworkCheck(id);
            int a = int.Parse(id);
            if (a % 2 == 1)
            { Session["教师删除或查看作业"] = "删除"; }
            else
            { Session["教师删除或查看作业"] = "查看"; }

            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }

        public string TT1(string id) //打分
        {
            var result = id;
            Session["教师选择查看布置的作业"] = id;
            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }

        public string TT2(string id)
        {
            var result = id;
            Session["教师选择查看团队编号"] = id;
            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }

        public string TT3(string id)
        {
            int tid = int.Parse(id);
            if (tid % 3 == 0)//通过
            {
                int teamid = tid / 3;
                List<team> t = db.team.ToList();
                foreach (team tt in t)
                {
                    if (tt.team_id == teamid)
                    {
                        tt.status = 1;
                        db.Entry(tt).State = EntityState.Modified;
                        db.SaveChanges();
                    }
                }
            }
            else if (tid % 3 == 2)//未通过
            {
                int teamid = (tid + 1) / 3;
                List<team> t = db.team.ToList();
                foreach (team tt in t)
                {
                    if (tt.team_id == teamid)
                    {
                        db.team.Remove(tt);
                        db.SaveChanges();
                    }
                }
            }
            var result = id;
            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }
        public string TT4(string id)
        {
            var result = id;
            Session["教师选择查看申请加入团队编号"] = id;
            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }
        public string TT5(string id)
        {
            var result = id;
            Session["教师选择团队作业打分"] = id;
            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }
        public ActionResult test()
        {
            return View();
        }
    }

}