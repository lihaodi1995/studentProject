package com.rua.homeworkController;

import java.util.ArrayList;
import java.util.List;

import org.hibernate.Session;
import org.hibernate.query.Query;

import model.GroupMember;
import model.HibernateUtil;
import model.SubText;
import net.sf.json.JSONObject;

public class hiberTest {
	public static void updateByHibernateHWGrade()
	{
		SubText st = null;
		Session session = null;
		List<SubText> results = new ArrayList<SubText>();
		try{
			session = HibernateUtil.factory.openSession();
			session.beginTransaction();
			String hql = "from SubText where textId =:file";
			Query query = session.createQuery(hql);
//			query.setParameter("gid", 2);
//			query.setParameter("tt", "12");
			query.setParameter("file", "jsp开发笔记.docx");
			results = query.list();			
//			label = (Labels)session.get(Labels.class, results.get(0).getId());
			System.out.println(results.get(0));
			
//			st = results.get(0);
//			st.setGrade(jo.getString("grade"));
//			st.setComment(jo.getString("comment"));
//			session.update(st);
			session.getTransaction().commit();
			
		}catch(Exception e)
		{
			e.printStackTrace();
			session.getTransaction().rollback();
		}finally{
			HibernateUtil.closeSession(session);
			
		}
		
		return;
	}
	public static void main(String []args)
	{
		updateByHibernateHWGrade();
	}

}
