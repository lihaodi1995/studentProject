using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Data.Entity;
using WebApplication2.Models;
using System.IO;
using System.Reflection;

namespace WebApplication2.Controllers
{
    public class studentController : Controller
    {
        // GET: student
        private database1Entities db = new database1Entities();
        public ActionResult Index()
        {
            return View("mainOfStudent");

        }


        public ActionResult LogOut()
        {
            return RedirectToAction("Login", "User");
        }

        public ActionResult classMessage() { return View(); }
        public ActionResult CommentForTeam() { return View(); }
        public ActionResult HomeworkForTeam() { return View(); }
        public ActionResult MessageForTeam() { return View(); }
        
        public ActionResult Student_changehomework() {
            List<student> stulist = db.student.ToList();
            List<submission> slist = db.submission.ToList();
            List<assiglist> asslist = new List<assiglist>();
            int tid = 0;
            foreach (student s in stulist)
            {
                if (s.student_id.ToString() == Session["CurUser"].ToString())
                {
                    if (s.team_id != null)
                    {
                        tid = s.team_id.Value;
                        break;
                    }
                    else
                    {
                        return RedirectToAction("Student_class", "stident");
                    }
                }
            }
            foreach (submission a in slist)
            {
                if (a.team_id == tid)
                {
                    if (a.score != null)
                    { 
                        assiglist assig = new assiglist();
                        assig.assignname = db.assignment.Find(a.assignment).assignment_name;
                        assig.date = a.sub_time.Value;
                        assig.score = a.score.Value;
                        asslist.Add(assig);
                    }
                    else
                    {
                        assiglist assig = new assiglist();
                        assig.assignname = db.assignment.Find(a.assignment).assignment_name;
                        assig.date = a.sub_time.Value;
                        assig.score = 0;
                        asslist.Add(assig);
                    }

                }
            }
            return View(asslist);
        }

        public ActionResult Student_class() { return View(); }
        public ActionResult Student_classchange() { return View(); }
        public ActionResult Student_classdel() { return View(); }
        public ActionResult Student_classhomework() { return View(); }
        
        
        public ActionResult Student_team() { return View(); }
        public ActionResult submitHomework() { return View(); }
        public ActionResult support() { return View(); }

        public ActionResult Student_checkTeam()
        {

            List<student> stulist = db.student.ToList();

            List<member> mem = new List<member>();

            int tid = 0;

            foreach (student s in stulist)
            {
                if (s.student_id.ToString() == Session["CurUser"].ToString())
                {
                    if (s.team_id != null)
                    {
                        tid = s.team_id.Value;
                        break;
                    }
                    else
                    {
                        return ShowAlertAndHref("你不是团队负责人", "Student_team");
                    }
                }
            }

            List<student> stlist = db.student.ToList();
            int leader = int.Parse(Session["CurUser"].ToString());
            List<studentapply> alist = new List<studentapply>();
            foreach (student s in stlist)
            {

                if (s.apply != null)
                    if (db.team.Find(s.apply).leader_id == leader)
                    {
                        studentapply a = new studentapply();
                        a.student_id = s.student_id;
                        a.studentid = s.student_id * 2;
                        a.studentid2 = s.student_id * 2 - 1;
                        a.student_name = s.student_name;
                        alist.Add(a);
                    }

            }
            return View(alist);
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
                    foreach(team ttt in team1)
                    {
                        if (ttt.team_id == tid)
                            tsize = ttt.teamsize.Value;
                    }
                    foreach (student s1 in stu)
                    {
                        if (s1.team_id == tid)
                        {
                            if(s1.score==null) { aratio[i] = 0; }
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
                        if (allpro != 0)
                        {
                            double hh = tsize * sfinal / allpro;
                            double hhh = a / afinal;
                            double final = hh * hhh;
                            string s121323 = Math.Ceiling(final).ToString();
                            s.ratio = int.Parse(s121323);
                            if (s.ratio > 100)
                                s.ratio = 100;
                        }
                        else
                            s.ratio = 0;
                    }
                    
                }
                db.Entry(s).State = EntityState.Modified;
                db.SaveChanges();
            }
        }

        public ActionResult Student_classdata()
        {
            getscore();
            List<course> clist = db.course.ToList();
            List<teachercourse> tclist = new List<teachercourse>();
            List<student> stu = db.student.ToList();
            int a = 0;
            foreach(student s in stu)
            {
                if (s.student_id == int.Parse(Session["CurUser"].ToString()))
                    { a = s.ratio.Value; }
            }
            foreach (course c in clist)
            {
                teachercourse tc = new teachercourse();
                tc.coursename = c.course_name;
                tc.coursetime = c.time;
                tc.teachername = db.teacher.Find(c.teacher_id).teacher_name;
                tc.location = c.location;
                tc.require = c.requirement;
                tc.score = a;
                tclist.Add(tc);
            }
            return View(tclist);
        }

        public ActionResult Student_myteam()
        {
            List<student> stulist = db.student.ToList();

            List<member> mem = new List<member>();

            int tid = 0;

            foreach (student s in stulist)
            {
                if (s.student_id.ToString() == Session["CurUser"].ToString())
                {
                    if (s.team_id != null)
                    {
                        tid = s.team_id.Value;
                        Session["提交申请"] = s.team_id;
                        break;
                    }
                    else
                    {
                        return ShowAlertAndHref("你还未加入团队", "Student_team");
                    }
                }
            }

            team t = db.team.Find(tid);
            ViewData["团队名称"] = t.team_name;
            ViewData["团队负责人"] = db.student.Find(t.leader_id).student_name;
            ViewData["负责人id"] = t.leader_id;
            switch (t.status)
            {
                case -1:
                    ViewData["审核情况"] = "未提交";
                    break;
                case 0:
                    ViewData["审核情况"] = "待审核";
                    break;
                case 1:
                    ViewData["审核情况"] = "已通过";
                    break;
                default:
                    break;
            }

            foreach (student s in stulist)
            {
                if (s.team_id == tid)
                {
                    member m = new member();
                    m.memberid = s.student_id;
                    m.membername = s.student_name;
                    m.membertel = s.tel;
                    mem.Add(m);
                }
            }

            return View(mem);
        }

        public ActionResult submitteam()
        {
            int tid = int.Parse(Session["提交申请"].ToString());
            team t = db.team.Find(tid);
            t.status = 0;

            db.Entry(t).State = EntityState.Modified;
            db.SaveChanges();

            return RedirectToAction("Student_myteam", "student");
        }

        public ActionResult Student_allteam()
        {
            List<team> tlist = db.team.ToList();
            List<teamlist> tlist1 = new List<teamlist>();
            List<student> dlidt = db.student.ToList();

            foreach (student s in dlidt)
            {
                if (s.student_id.ToString() == Session["CurUser"].ToString())
                {
                    if (s.team_id == null)
                    {
                        ViewData["无团队"] = "无团队";
                        break;
                    }
                    else
                    {
                        ViewData["无团队"] = "有团队";
                        break;
                    }
                }
            }

            foreach (team t in tlist)
            {
                teamlist tl = new teamlist();
                if (t.status == -1)
                {
                    tl.teamname = t.team_name;
                    tl.leadername = db.student.Find(t.leader_id).student_name;
                    tl.size = t.teamsize.Value;
                    tlist1.Add(tl);
                }
            }
            return View(tlist1);

        }

        [HttpPost]
        public ActionResult Student_allteam(string teamchoose)
        {
            if (teamchoose.Contains("申请加入"))
            {
                string finalValue = teamchoose.Substring(0, teamchoose.Length - 4);//现在的finalValue就是团队名字
                int sid = int.Parse(Session["CurUser"].ToString());
                student s = db.student.Find(sid);
                List<team> tlist = db.team.ToList();
                foreach (team t in tlist)
                {
                    if (t.team_name == finalValue)
                    {
                        s.apply = t.team_id;
                        break;
                    }
                }
                db.Entry(s).State = EntityState.Modified;
                db.SaveChanges();
            }
            return RedirectToAction("Student_allteam", "student");
        }

        public ActionResult Student_createteam()
        {
            List<student> dlidt = db.student.ToList();
            bool flag = true;

            foreach (student s in dlidt)
            {
                if (s.student_id.ToString() == Session["CurUser"].ToString())
                {
                    if (s.team_id == null)
                    {
                        flag = true;
                        break;
                    }
                    else
                    {
                        flag = false;
                        break;
                    }
                }
            }
            if (flag)
            {
                return View();
            }
            else
            {
                return ShowAlertAndHref("你拥有一个团队", "Student_team");
            }
        }

        [HttpPost]
        public ActionResult Student_createteam(string team1)
        {


            team t = new team();
            List<student> slist = db.student.ToList();

            foreach (student s in slist)
            {
                if (s.student_id.ToString() == Session["CurUser"].ToString())
                {
                    t.leader_id = s.student_id;
                    break;
                }
            }

            t.teamsize = 1;
            t.status = -1;
            t.team_name = team1;
            db.team.Add(t);
            db.SaveChanges();

            student st = db.student.Find(t.leader_id);
            st.team_id = t.team_id;

            db.Entry(st).State = EntityState.Modified;
            db.SaveChanges();
            return View("Student_team");

        }

        public ActionResult Student_evateam()
        {
            List<student> stulist = db.student.ToList();

            List<member> mem = new List<member>();

            int tid = 0;

            foreach (student s in stulist)
            {
                if (s.student_id.ToString() == Session["CurUser"].ToString())
                {
                    if (s.team_id != null)
                    {
                        tid = s.team_id.Value;
                        break;
                    }
                    else
                    {
                        return ShowAlertAndHref("你不是团队负责人", "Student_team");
                    }
                }
            }

            team t = db.team.Find(tid);

            ViewData["负责人id1"] = t.leader_id;


            foreach (student s in stulist)
            {
                if (s.team_id == tid)
                {
                    member m = new member();
                    m.memberid = s.student_id;
                    m.membername = s.student_name;
                    if (s.score != null)
                    {
                        //ViewData["未评价"] = "已评价";
                        m.score = s.score.Value;
                    }
                    else
                    {
                        m.score = 0;
                        //ViewData["未评价"] = "未评价";
                    }
                    mem.Add(m);
                }
            }
            return View(mem);
        }

        [HttpPost]
        public ActionResult Student_evateam(string evabut)
        {
            if (evabut.Contains("A"))
            {
                string[] result = evabut.Split('A');
                string a = result[0];
                string b = result[1];//现在的finalValue就是团队名字
                int sid = int.Parse(a);
                student s = db.student.Find(sid);
                s.score = int.Parse(b);
                db.Entry(s).State = EntityState.Modified;
                db.SaveChanges();
            }
            return RedirectToAction("Student_evateam", "student");
        }

        public ActionResult Student_classsub()
        {
            List<student> stulist = db.student.ToList();
            List<submission> slist = db.submission.ToList();
            List<assiglist> asslist = new List<assiglist>();

            int tid = 0;

            foreach (student s in stulist)
            {
                if (s.student_id.ToString() == Session["CurUser"].ToString())
                {
                    if (s.team_id != null)
                    {
                        tid = s.team_id.Value;
                        break;
                    }
                    else
                    {
                        return RedirectToAction("Student_class","stident");
                    }
                }
            }

            foreach (submission a in slist)
            {
                if (a.team_id == tid)
                {
                        assiglist assig = new assiglist();
                        assig.assignname = db.assignment.Find(a.assignment).assignment_name;
                        assig.date = a.sub_time.Value;
                        asslist.Add(assig);
                }
            }
            return View(asslist);
        }

        public ActionResult ShowAlertAndHref(string msg, string actionName, object[] obj = null)
        {
            var script = String.Format("<script>alert('{0}');location.href='{1}'</script>", msg, Url.Action(actionName, obj));
            return Content(script, "text/html");
        }

        public string TT(String id) //修改作业
        {
            int leader = int.Parse(Session["CurUser"].ToString());
            List<team> tlist = db.team.ToList();
            int tid = 0;
            foreach (team t in tlist)
            {
                if (t.leader_id == leader)
                {
                    t.teamsize++;
                    tid = t.team_id;
                    db.Entry(t).State = EntityState.Modified;
                    db.SaveChanges();
                }
            }
            var result = id;
            int stuid = int.Parse(id);

            if (stuid % 2 == 0)
            {
                int sid = stuid / 2;
                student s = db.student.Find(sid);
                s.apply = null;
                s.team_id = tid;
                db.Entry(s).State = EntityState.Modified;
                db.SaveChanges();
            }
            else if (stuid % 2 == 1)
            {
                int sid = (stuid + 1) / 2;
                student s = db.student.Find(sid);
                s.apply = null;
                s.team_id = null;
                db.Entry(s).State = EntityState.Modified;
                db.SaveChanges();
            }
            return Newtonsoft.Json.JsonConvert.SerializeObject(result);
        }


        /*public ActionResult classMessage()//课程信息
        {
            List<course> list = db.course.ToList();
            List<teacher> list1 = db.teacher.ToList();
            List<teachercourse> list2 = new List<teachercourse>();
            foreach (course course1 in list)
            {
                teachercourse tc = new teachercourse();
                tc.courseid = course1.course_id;
                tc.location = course1.location;
                tc.coursetime = course1.time;
                tc.coursename = course1.course_name;
                tc.credit = course1.credit.Value;
                tc.info = course1.requirement;
                foreach (teacher teacher1 in list1)
                {
                    if (teacher1.teacher_id == course1.teacher_id)
                        tc.teachername = teacher1.teacher_name;
                }
                list2.Add(tc);
            }
            return View(list2);
        }


        public ActionResult MessageForTeam()//团队信息
        {
            List<student> list3 = db.student.ToList();
            int a = 0, leaderid = 0;
            foreach (student student1 in list3)
            {
                if (student1.student_id.ToString() == Session["CurUser"].ToString())
                    a = student1.team_id.Value;
            }
            List<team> list4 = db.team.ToList();
            List<student> list5 = new List<student>();
            foreach (team team1 in list4)
            {
                if (team1.team_id == a)
                {
                    ViewData["组名"] = team1.team_name;
                    leaderid = team1.leader_id.Value;
                }
            }
            foreach (student student2 in list3)
            {
                if (student2.student_id == leaderid)
                {
                    ViewData["负责人"] = student2.student_name;
                    list5.Add(student2);
                }
            }
            foreach (student student3 in list3)
            {
                if (student3.team_id == a && student3.student_id != leaderid)
                    list5.Add(student3);
            }
            return View(list5);
        }

        public ActionResult HomeworkForTeam()//团队作业
        {
            List<student> list6 = db.student.ToList();
            int a = 0, value = 0;
            List<homework> list9 = new List<homework>();
            foreach (student student1 in list6)
            {
                if (student1.student_id.ToString() == Session["CurUser"].ToString())
                    a = student1.team_id.Value;
            }
            List<submission> list7 = db.submission.ToList();
            List<assignment> list8 = db.assignment.ToList();
            foreach (assignment homework1 in list8)
            {
                if (homework1.starttime < DateTime.Now)
                {
                    homework h = new homework();
                    h.homeworkname = homework1.assignment_name;
                    h.teamid = a;
                    h.value = value;
                    value++;
                    h.checksub = false;
                    h.checktime = true;
                    foreach (submission sub in list7)
                    {
                        if (sub.assignment_id == homework1.assignment_id)
                        {
                            if (sub.team_id == a && sub.subtime != null)
                            {
                                h.checksub = true;
                                h.submittime = sub.subtime.Value;
                            }
                        }
                    }
                    if (h.checksub == false && homework1.deadline < DateTime.Now)
                        h.checktime = false;
                    list9.Add(h);
                }
            }
            return View(list9);
        }
        */
        public string Uploadhomework(HttpPostedFileBase file)
        {
            string curUserId = Session["CurUser"].ToString();
            List<team> team1 = db.team.ToList();
            int teamid=0;
            foreach(team t in team1)
            {
                if (t.leader_id == int.Parse(curUserId))
                    teamid = t.team_id;
            }
            if (teamid != 0)
            {
                var severPath = this.Server.MapPath("~/Homework/");
                Directory.CreateDirectory(severPath);

                string[] stst = file.FileName.Split('.');
                
                string t = Session["homeworkname"].ToString();
                var fileNewName = Session["homeworkname"].ToString() + "BY" + teamid.ToString() + "." + stst[1];
               // file.FileName = fileNewName;
                var savePath = Path.Combine(severPath, fileNewName);
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
                    string s = Session["homeworkname"].ToString();
                    int aid = 0;
                    List<assignment> asss = db.assignment.ToList();
                    foreach (assignment a in asss)
                    {
                        if (a.assignment_name == s)
                            aid = a.assignment_id;
                    }
                    List<submission> subs = db.submission.ToList();
                    bool flag = false;
                    foreach (submission sub in subs)
                    {
                        if (sub.team_id == teamid && sub.assignment == aid)
                        {
                            flag = true;
                            sub.sub_time = DateTime.Now;
                            sub.sub_count = sub.sub_count + 1;
                            sub.sub_path = savePath.ToString();
                            db.Entry(sub).State = EntityState.Modified;
                            db.SaveChanges();
                            break;
                        }
                    }
                    if (flag == false)
                    {
                        submission subb = new submission();
                        subb.team_id = teamid;
                        subb.assignment = aid;
                        subb.sub_time = DateTime.Now;
                        subb.sub_count = subb.sub_count + 1;
                        subb.sub_path = savePath;
                        db.submission.Add(subb);
                        db.SaveChanges();
                    }
                }
                return result;
            }
            else { string result = ""; return result; } 
        }

        public string init(string homeworkName)
        {
            //string t = homeworkName;
            Session["homeworkname"] = homeworkName;
            return Newtonsoft.Json.JsonConvert.SerializeObject(homeworkName);
        }
    }
}