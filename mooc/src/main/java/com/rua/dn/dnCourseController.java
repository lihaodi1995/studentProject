package com.rua.dn;

import java.io.UnsupportedEncodingException;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.hibernate.Session;
import org.hibernate.cfg.Configuration;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import model.Course;
import model.HibernateUtil;
import model.Task;
import net.sf.json.JSONObject;

@Controller
public class dnCourseController {
	@RequestMapping("/dncourse")
	public String dn_course(Model model)
	{
		return "dn-course";
	}
	
	public void insertOrUpdateByHibernateTask(String name, String info, String teacher, String place, String score, String people, String start, String end) {
		// 读取配置文件
		Configuration cfg = new Configuration().configure();
		Session session = null;
		try {
			session = HibernateUtil.factory.openSession();
			// 开启事务
			session.beginTransaction();
			
			Course c = new Course();
			c.setId(1);
			c.setName(name);
			c.setPeople(people);
			c.setPlace(place);
			c.setScore(score);
			c.setStartTime(start);
			c.setEndTime(end);
			c.setTeacher(teacher);
			c.setInfo(info);
			session.saveOrUpdate(c);
//			Task t = new Task();
//			t.setTitle(hwtitle);
//			t.setCourseId(1);
//			t.setInfo(hwexplain);
//			t.setWeight(Double.parseDouble(hwweight));
//			session.save(t);

			// 提交事务
			session.getTransaction().commit();
			
		} catch (Exception e) {
			e.printStackTrace();
			session.getTransaction().rollback();
		} finally {
			if (session != null) {
				if (session.isOpen()) {
					session.close();
				}
			}
		}
	}
	
	//var course = {'name': name, 'info': info, 'teacher': teacher, 'place': place, 'score': score, 'people': people, 'start': start, 'end': end,};
	@RequestMapping(value ="/courseInfo", method = RequestMethod.POST)
	public String courseInfo(Model model, @RequestBody String str,HttpServletRequest request,
			HttpServletResponse response) throws UnsupportedEncodingException
	{
		request.setCharacterEncoding("UTF-8");
//		String name = request.getParameter("name");
//		String info = request.getParameter("info");
//		String teacher = request.getParameter("teacher");
//		String place = request.getParameter("place");
//		String score = request.getParameter("score");
//		String people = request.getParameter("people");
//		String start = request.getParameter("start");
//		String end = request.getParameter("end");
		JSONObject jo = JSONObject.fromObject(str);
		System.out.println(request.getParameter("tp"));
		//insertOrUpdateByHibernateTask(String name, String info, String teacher, String place, String score, String people, String start, String end) {
		insertOrUpdateByHibernateTask(jo.getString("name"), jo.getString("info"), jo.getString("teacher"), jo.getString("place"), jo.getString("score"), jo.getString("people"), jo.getString("start"), jo.getString("end"));
		return "dn-course";
	}
}
