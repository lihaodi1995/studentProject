package com.rua.other;

import java.util.Date;
import java.util.List;
import org.hibernate.Session;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import model.Absence;
import model.AbsenceId;
import model.Attendance;
import model.HibernateUtil;

@Controller
public class attendenceController {
	@RequestMapping(value="/getAb",method=RequestMethod.GET)
	public @ResponseBody String get(){
		try{
			Session session=HibernateUtil.openSession();
			session.getTransaction().begin();
			Attendance att=(Attendance)session.createQuery("from Attendance").list().get(0);
			if(att.getChecked()==-1) return "{status:0}";
			else if(att.getChecked()==1 ||att.getChecked()==0) return "{status:1}";
		}catch(Exception e){
			e.printStackTrace();
			return "{status:-1}";
		}
		return "{status:-1}";
	}
	
	
	@RequestMapping(value="/postAb",method=RequestMethod.GET)
	public @ResponseBody String post(String status){
		try{
			if(status.equals("0")){
				end();
			}else if(status.equals("1")){
				start();
			}
		}catch(Exception e){
			e.printStackTrace();
			return "{status:0}";
		}
		return "{status:1}";
	}
	
	@RequestMapping(value="/startSign",method=RequestMethod.GET)
	public @ResponseBody String start(){
		try{
			Session session=HibernateUtil.openSession();
			session.beginTransaction();
			/*List<User> user=session.createQuery("from User where character=3").list();
			for(int i=0;i<user.size();i++){
				Attendance att=new Attendance();
				att.setId(user.get(i).getId());
				att.setName(user.get(i).getName());
				att.setGroup(((GroupMember)(session.createQuery("from GroupMember a where a.id.memberId="+att.getId()).list().get(0))).getId().getGroupId());
				session.save(att);
				session.getTransaction().commit();
			}*/
			session.createQuery("update Attendance set checked=0").executeUpdate();
			session.getTransaction().commit();
		}catch(Exception e){
			e.printStackTrace();
			return "{status:0}";
		}
		return "{status:1}";
	}
	
	@RequestMapping(value="/endSign",method=RequestMethod.GET)
	public @ResponseBody String end(){
		try{
			Session session=HibernateUtil.openSession();
			session.beginTransaction();
			List<Attendance> att=session.createQuery("from Attendance where checked!=1").list();
			System.out.println("sdsaddsadasa"+att.size());
			for(int i=0;i<att.size();i++){
				Absence ab=new Absence();
				AbsenceId r=new AbsenceId();
				ab.setId(r);
				Date now = new Date(); 
				ab.setId((new AbsenceId()));
				ab.getId().setDate(now);
				ab.setGroupId(att.get(i).getGroup());
				ab.setStuName(att.get(i).getName());
				ab.getId().setId(att.get(i).getId());
				session.saveOrUpdate(ab);
			}
			session.createQuery("update Attendance set checked=-1").executeUpdate();
			session.getTransaction().commit();
		}catch(Exception e){
			e.printStackTrace();
			return "{status:0}";
		}
		return "{status:1}";
	}
	
	@RequestMapping(value="/signIn",method=RequestMethod.GET)
	public @ResponseBody String end(String id){
		try{
			Session session=HibernateUtil.openSession();
			session.beginTransaction();
			Attendance att=(Attendance)session.createQuery("from Attendance").list().get(0);
			if(att.getChecked()==-1) return "{status:0}";
			else {
			session.createQuery("update Attendance set checked=1 where id="+id).executeUpdate();
			session.getTransaction().commit();}
		}catch(Exception e){
			e.printStackTrace();
			return "{status:0}";
		}
		return "{status:1}";
	}
	

}
