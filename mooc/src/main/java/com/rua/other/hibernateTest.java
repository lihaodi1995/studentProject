package com.rua.other;

import java.util.ArrayList;
import java.util.List;

import org.hibernate.Session;
import org.hibernate.query.Query;

import model.Course;
import model.HibernateUtil;

public class hibernateTest {
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
		HibernateUtil.factory.close();
		
		return;
	}
	public static void main(String[]args)
	{
		updateByHibernate("3223433");
		
	}
}
