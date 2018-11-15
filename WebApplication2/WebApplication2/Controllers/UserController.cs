using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using WebApplication2.Models;

namespace WebApplication2.Controllers
{
    public class UserController : Controller
    {
        private database1Entities db = new database1Entities();
        public ActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Login(string username, string password, int status)
        {
            bool hasuser = false;
            bool hasuserid = false;
            bool hasuserpswd = false;

            List<student> stulist = db.student.ToList();
            List<teacher> tealist = db.teacher.ToList();
            List<jiaowu> jwlist = db.jiaowu.ToList();

            switch (status)
            {
                //student login
                case 1:
                    foreach (student user in stulist)
                    {
                        if (user.student_id.ToString() == username)
                        {
                            if (user.password == password)
                            {
                                hasuser = true;
                                hasuserpswd = true;
                                hasuserid = true;
                                Session["CurUser"] = username;//储存当前用户ID
                                Session["CurUserName"] = user.student_name;
                            }
                            else
                            {
                                hasuserpswd = false;
                                hasuserid = true;
                            }
                        }
                    }
                    if (hasuser)
                    {
                        ViewData["1"] = "Login Success";
                        return RedirectToAction("Index", "student");
                    }
                    else
                    {
                        if (hasuserid == false)
                            ViewData["1"] = "用户名不存在！";
                        else
                            ViewData["1"] = "密码不正确！";
                    }
                    break;
                //teacher login
                case 2:
                    foreach (teacher user in tealist)
                    {
                        if (user.teacher_id.ToString() == username)
                        {
                            if (user.password == password)
                            {
                                hasuser = true;
                                hasuserpswd = true;
                                hasuserid = true;
                                Session["CurUser"] = username;//储存当前用户ID
                                Session["CurUserName"] = user.teacher_name;
                            }
                            else
                            {
                                hasuserpswd = false;
                                hasuserid = true;
                            }
                        }
                    }
                    if (hasuser)
                    {
                        ViewData["1"] = "Login Success";
                        return RedirectToAction("Index", "teacher");
                    }
                    else
                    {
                        if (hasuserid == false)
                            ViewData["1"] = "用户名不存在！";
                        else
                            ViewData["1"] = "密码不正确！";
                    }
                    break;
                //jiaowurenyuan login
                default:
                    foreach (jiaowu user in jwlist)
                    {
                        if (user.jiaowu_id.ToString() == username)
                        {
                            if (user.password == password)
                            {
                                hasuser = true;
                                hasuserpswd = true;
                                hasuserid = true;
                                Session["CurUser"] = username;//储存当前用户ID
                                Session["CurUserName"] = "超级管理员";
                            }
                            else
                            {
                                hasuserpswd = false;
                                hasuserid = true;
                            }
                        }
                    }
                    if (hasuser)
                    {
                        ViewData["1"] = "Login Success";
                        return RedirectToAction("Tojiaowu", "jiaowu");
                    }
                    else
                    {
                        if (hasuserid == false)
                            ViewData["1"] = "用户名不存在！";
                        else
                            ViewData["1"] = "密码不正确！";
                    }
                    break;
            }
            return View();
        }
    }
}