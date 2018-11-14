package com.rua.other;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.io.FileUtils;
import org.hibernate.Session;
import org.hibernate.query.Query;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import model.Course;
import model.HibernateUtil;
import net.sf.json.JSONObject;

@Controller
public class changeClassInfoController {
	
	public static void updateByHibernate(String tp){
		
		Session session = null;
		List<Integer> results = new ArrayList<Integer>();
		try{
			session = HibernateUtil.factory.openSession();
			session.beginTransaction();
			
			String hql = "update Course c set c.tp=:tp where c.id=:ID";
			Query query  = session.createQuery(hql); 
			query.setParameter("tp", tp);
			query.setParameter("ID", 1);
			query.executeUpdate();
			
			session.getTransaction().commit();
			
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
		}finally{
			HibernateUtil.closeSession(session);
		}
		//HibernateUtil.factory.close();
		
		return;
	}
	
	
	
	
	@RequestMapping(value = "/bigAss", method = RequestMethod.POST)
	public void bigAss(@RequestBody String str, ModelMap model, HttpServletRequest request,
			HttpServletResponse response) throws IOException
	{
		JSONObject jo = JSONObject.fromObject(str);
		updateByHibernate(jo.getString("tp"));
		
		System.out.println(jo.getString("tp"));
	}
	
	@RequestMapping(value = "/tc-tm")
	public String tc_tm(ModelMap model)
	{
		return "tc-tm";
	}
	
//	@RequestMapping(value = "/tc-hw")
//	public String tc_hw(ModelMap model)
//	{
//		return "tc-hw";
//	}
	
	@RequestMapping(value = "/tm-stu")
	public String tm_stu(ModelMap model)
	{
		return "tm-stu";
	}
	
	@RequestMapping(value = "/homework-stu")
	public String homework_stu(ModelMap model)
	{
		return "homework-stu";
	}
}
