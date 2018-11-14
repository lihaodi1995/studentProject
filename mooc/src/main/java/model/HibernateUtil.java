package model;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;


public class HibernateUtil {
		public static SessionFactory factory; 
		static { 
	        try {    
	            factory = new Configuration().configure()  
	  
	                    .buildSessionFactory();  
	  
	        } catch (Exception e) {  
	  
	            e.printStackTrace();  
	  
	        }  
	  
	    }  
		 //生成session  
	    public static Session openSession(){  
	        Session session=factory.openSession();  
	        return session;  
	  
	    }  
	    //关闭session  
	    public static void closeSession(Session session){  
	        if(session != null){  
	            session.close();  
	        }  
	    }  
}
