package com.rua.usercontroller;

import java.util.ArrayList;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.hibernate.Session;
import org.hibernate.query.Query;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import model.GroupMember;
import model.HibernateUtil;
import model.User;
import net.sf.json.JSONObject;

@Controller
public class loginController {
	@RequestMapping(value="/login")
	public String login(Model model)
	{
		return "login";
	}
	
	
	@RequestMapping(value="/team-stu")
	public String team_stu(Model model)
	{
		return "team-stu";
	}
	
	
	@RequestMapping(value="/indexStudent")
	public String indexStudent(Model model)
	{
		return "indexStudent";
	}
	
	@RequestMapping(value="/indexTeacher")
	public String indexTeacher(Model model)
	{
		return "indexTc";
	}
	
	public User searchUserById(String Id)
	{
		
		User user  = null;
		Session session = null;
		List<User> results = new ArrayList<User>();
		try{
			session = HibernateUtil.factory.openSession();
			session.beginTransaction();
			String hql = "from User where Id = \'"+Id+"\'";
			Query query = session.createQuery(hql);

			results = query.list();

			
		}catch(Exception e)
		{
			e.printStackTrace();
			session.getTransaction().rollback();
		}finally{
			HibernateUtil.closeSession(session);
		/*if(session!=null){
			if(session.isOpen()){
				session.close();
			}
		}*/
		}
		if(results.size()==0)
			return null;
		return results.get(0);
	}
	
	@RequestMapping(value = "/loginCheck", method = RequestMethod.POST)
	public @ResponseBody String loginCheck( ModelMap model, HttpServletRequest request,
				HttpServletResponse response) {

		
		String Id = request.getParameter("Id");
		String password = request.getParameter("password");
		
		System.out.println(Id);
		User user = new User();
		user = searchUserById(Id);
		if(user == null)
			return "no";
		
		System.out.println(user.getPassword());
		
		byte cha = user.getCharacter();
		
		if(!password.equals(user.getPassword()))
		{
			return "wrong";
		}
		request.getSession().setAttribute("sessionuserid", Id);
		request.getSession().setAttribute("sessionusername", user.getName());
		if(cha == 1)//����
		{
			return "jiaowu";
		}
		else if(cha == 2)//laoshi
		{
			return "teacher";
		}
		else if(cha == 3)//xuesheng
		{
			request.getSession().setAttribute("sessiongroupid", searchGroupMByHibernate(user.getId()));
			return "student";
		}
		else
			return null;
	}
	public static int searchGroupMByHibernate(int userid){
		
		Session session = null;
		List<GroupMember> results = new ArrayList<GroupMember>();
		try{
			session = HibernateUtil.factory.openSession();
			session.beginTransaction();
			
			String hql = "FROM GroupMember gm WHERE gm.id.memberId = "+userid;
			Query query = session.createQuery(hql);
			results = query.list();
			
			session.getTransaction().commit();
			
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
		}finally{
			HibernateUtil.closeSession(session);
		}
//		HibernateUtil.factory.close();
		if(results.size()==0) return 0;
		return results.get(0).getId().getGroupId();
	}
	@RequestMapping(value="/logout")
	public String logout(Model model, HttpServletRequest request,
			HttpServletResponse response)
	{
		request.getSession().setAttribute("sessionusername", null);
		return "login";
	}
}
