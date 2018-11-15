using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Data.Entity;
using MvcApplication5.Models;
using System.IO;
using System.Reflection;

namespace MvcApplication5.Controllers
{
    public class studentController : Controller
    {
        // GET: student
        private database2Entities db = new database2Entities();
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
        
        public ActionResult Student_changehomework() { return View(); }
        public ActionResult Student_checkTeam() { return View(); }
        public ActionResult Student_class() { return View(); }
        public ActionResult Student_classdata() { return View(); }
        public ActionResult Student_classchange() { return View(); }
        public ActionResult Student_classdel() { return View(); }
        public ActionResult Student_classhomework() { return View(); }
        public ActionResult Student_classsub() { return View(); }
        
        public ActionResult Student_evateam() { return View(); }
        
        public ActionResult Student_team() { return View(); }
        public ActionResult submitHomework() { return View(); }
        public ActionResult support() { return View(); }

                                        public ActionResult Student_myteam() 
                                        { 
                                            List<student> stulist=db.student.ToList();

                                            List<member> mem = new List<member>();

                                            int tid=0;

                                            foreach(student s in stulist)
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
                                                        return View("Student_team");
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
                                                    ViewData["审核情况"]="未提交";
                                                    break;
                                                case 0:
                                                    ViewData["审核情况"]="待审核";
                                                    break;
                                                case 1:
                                                    ViewData["审核情况"]="已通过";
                                                    break;
                                                default:
                                                    break;
                                            }  

                                            foreach (student s in stulist)
                                            {
                                                if (s.team_id == tid)
                                                {
                                                    member m=new member();
                                                    m.memberid = s.student_id;
                                                    m.membername = s.student_name;
                                                    m.membertel = s.tel;
                                                    mem.Add(m);
                                                }
                                            }
                                            return View(mem); 
                                        }

                                        public ActionResult Student_allteam() 
                                        {
                                            List<team> tlist = db.team.ToList();
                                            List<teamlist> tlist1 = new List<teamlist>();
                                            List<student> dlidt=db.student.ToList();

                                            foreach(student s in dlidt)
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
                                                teamlist tl=new teamlist();
                                                if (t.status == -1)
                                                {
                                                    tl.teamname = t.team_name;
                                                    tl.leadername = db.student.Find(t.leader_id).student_name;
                                                    tl.size = t.size.Value;
                                                    tlist1.Add(tl);
                                                }
                                            }
                                            return View(tlist1); 
                                        }

                                        public ActionResult Student_createteam() { return View(); }

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
                                            t.size = 1;
                                            t.status = -1;
                                            t.team_name = team1;
                                            db.team.Add(t);
                                            db.SaveChanges();
                                            

                                            return View("Student_team"); 
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

        public ActionResult Uploadhomework(HttpPostedFileBase input1)
        {


            var fileName = Path.GetFileName(input1.FileName);
            var filePath = Path.Combine(Request.MapPath("~/Homework"), fileName);



            input1.SaveAs(filePath);

            return RedirectToAction("ToHomeworkForTeam", "student");
        }*/
    }
}