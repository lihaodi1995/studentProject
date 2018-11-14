package com.rua.other;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.sql.DriverManager;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.ss.usermodel.Cell;
import org.hibernate.SQLQuery;
import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.query.Query;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;
import java.sql.*;
import java.sql.SQLException;

import model.Application;
import model.Grade;
import model.Group;
import model.GroupMember;
import model.GroupMemberId;
import model.HibernateUtil;
import model.Score;
import model.ScoreId;
import model.User;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import net.sf.jxls.reader.ReaderBuilder;
import net.sf.jxls.reader.XLSReader;
import net.sf.jxls.transformer.Workbook;
import net.sf.jxls.transformer.XLSTransformer;

@Controller
public class groupController {
	@RequestMapping(value="/d")
	public void test(){
		//createGroup(1,"ruaruarua");
		//createGroup(2,"fel");
		//submitGroup(2);
		//deleteGroup(3);
		//createGroup(4,"gayll");
		//System.out.println(getMyGroup(4234));
		System.out.println(getTeamScore("60"));
	}
	@RequestMapping(value="/stu-team-create",method=RequestMethod.POST)
	public @ResponseBody String createGroup(String stuID,String teamName,String teamInfo){//int manager_id,String group_name
		Session session= HibernateUtil.factory.openSession();
		JSONObject json=new JSONObject(); 
		String manager_id=stuID;
		//System.out.println(manager_id);
		String group_name=teamName;
		String group_Info=teamInfo;
		//System.out.println(group_name);
		try{
			Transaction ts=session.getTransaction();
			session.beginTransaction();
			Group group=new Group();
			group.setManagerId(Integer.parseInt(manager_id));
			group.setName(group_name);
			group.setStatus((byte)0);
			group.setInfo(group_Info);
			session.save(group);
			session.getTransaction().commit();
			session.beginTransaction();
			GroupMember gm=new GroupMember();
			GroupMemberId a=new GroupMemberId();
			Group g=((Group)session.createQuery("from Group where managerId="+stuID).list().get(0));
			a.setGroupId(g.getId());
			a.setMemberId(g.getManagerId());
			gm.setId(a);
			session.save(gm);
			
			session.getTransaction().commit();
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
			json.put("status", 0);
			return json.toString();
			}
		finally{
			session.close();
		}
		json.put("status", 1);
		return json.toString();
		
	}
	
	@RequestMapping(value="stu-team-manage-submit",method=RequestMethod.POST)
	public @ResponseBody String submitGroup(String stuID){//int group_id
		Session session= HibernateUtil.factory.openSession();
		JSONObject json=new JSONObject();
		try{
			session.beginTransaction();
			Query query=session.createQuery("update Group set status=2 where managerId="+stuID);
			query.executeUpdate();
			session.getTransaction().commit();
			System.out.println(stuID);
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
			json.put("status",1);
			session.close();
			return json.toString();
		}
		finally{
			session.close();
		}
		json.put("status",0);
		return json.toString();
	}
	
	
	@RequestMapping(value="/tc-delG",method=RequestMethod.POST)
	public @ResponseBody String deleteGroup(@RequestParam("name") String name){//int group_id
		Session session= HibernateUtil.factory.openSession();
		//System.out.println(request);
		JSONObject json=new JSONObject(); 
		//String name=JSONObject.fromObject(request).get("name").toString();
		//System.out.println(JSONObject.fromObject(request));
		//String group_id=request.getParameter("group_id");
		//String name=request.getParameter("name");
		try{
			Transaction ts=session.getTransaction();
			session.beginTransaction();
			Query query=session.createQuery("delete from Group where name=\'"+name+"\'");
			query.executeUpdate();
			session.getTransaction().commit();
			
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
			json.put("status", 0);
			return json.toString();
			}
		finally{
			session.close();
		}
		json.put("status", 1);
		return json.toString();
	}
	
	
	@RequestMapping(value="/tc-manageG",method=RequestMethod.POST)
	public @ResponseBody String checkGroup(String name,String status){//int group_id,byte status
		Session session= HibernateUtil.factory.openSession();
		
		System.out.println(status);
		//JSONObject json=JSONObject.fromObject(request);
		JSONObject resp=new JSONObject(); 
		//String name=json.get("name").toString();
		//String status=json.get("status").toString();
		//System.out.println(JSONObject.fromObject(request));name
		name=name.substring(name.length()/2);
		try{
			session.beginTransaction();
			Query query=session.createQuery("update Group set status="+status+" where name=\'"+name+"\'"),
					sec=session.createQuery("from Group where name=\'"+name+"\'");
			int id=((Group)(sec.list().get(0))).getId();
			query.executeUpdate();
			session.getTransaction().commit();
			if(status.equals("0")){
				System.out.println(status);
				session.beginTransaction();
				Query query1=session.createQuery("delete from Group where name=\'"+name+"\'");
				Query query2=session.createQuery("delete from GroupMember a where a.id.groupId="+id);
				Query query3=session.createQuery("delete from Application where groupId="+id);
				query1.executeUpdate();
				query2.executeUpdate();
				query3.executeUpdate();
				session.getTransaction().commit();
			}
			
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
			resp.put("status", 1);
			return resp.toString();
			}
		finally{
			session.close();
		}
		resp.put("status", 0);
		return resp.toString();
	}
	
	@RequestMapping(value="/tc-getAcc",method=RequestMethod.GET, produces={"text/html;charset=UTF-8;","application/json;"})
	@ResponseBody
	public String getAcc(HttpServletRequest request,HttpServletResponse response) throws UnsupportedEncodingException{//int group_id,byte status
		JSONObject json=new JSONObject();
		Session session= HibernateUtil.factory.openSession();
		List<Group> group=new ArrayList<Group>();
		int count;
		try{
			Transaction ts=session.getTransaction();
			session.beginTransaction();
			Query query=session.createQuery("from Group where status=1");
			group=query.list();count=group.size();
			json.put("count", count);
			JSONArray array=new JSONArray();
			for(int i=0;i<count;i++){
				JSONObject tmp=new JSONObject();
				tmp.put("name", group.get(i).getName());
				Query query1=session.createQuery("from User where id="+group.get(i).getManagerId());
				List<User> user=query1.list();
				tmp.put("leader", user.get(0).getName());
				String member="",gmember="";
				Query query2=session.createQuery("from GroupMember a where a.id.groupId="+group.get(i).getId());
				List<GroupMember> gMember=query2.list();
				for(int j=0;j<gMember.size();j++){
					List<User> rua=session.createQuery("from User where Id="+gMember.get(j).getId().getMemberId()).list();
					if(rua.get(0).getGender()==(byte)0) gmember+=(rua.get(0).getName()+" ");
					else member+=(rua.get(0).getName()+" ");
				}
				tmp.put("member", member.toString());
				tmp.put("gmember", gmember.toString());
				array.add(tmp);
			}
			json.put("team", array);
		}catch(Exception e){e.printStackTrace();session.getTransaction().rollback();return null;}
		finally{
			session.close();
		}
		System.out.println(json.toString());
		response.setCharacterEncoding("utf-8");
		return json.toString();
		
	}
	
	@RequestMapping(value="/tc-getG",method=RequestMethod.GET, produces={"text/html;charset=UTF-8;","application/json;"})
	@ResponseBody
	public String getGroup(HttpServletRequest request,HttpServletResponse response){//int group_id,byte status
		JSONObject json=new JSONObject();
		Session session= HibernateUtil.factory.openSession();
		List<Group> group=new ArrayList<Group>();
		int count;
		try{
			Transaction ts=session.getTransaction();
			session.beginTransaction();
			Query query=session.createQuery("from Group where status=2");
			group=query.list();count=group.size();
			json.put("count", count);
			JSONArray array=new JSONArray();
			for(int i=0;i<count;i++){
				JSONObject tmp=new JSONObject();
				tmp.put("name", group.get(i).getName());
				Query query1=session.createQuery("from User where id="+group.get(i).getManagerId());
				List<User> user=query1.list();
				tmp.put("leader", user.get(0).getName());
				String member="",gmember="";
				Query query2=session.createQuery("from GroupMember a where a.id.groupId="+group.get(i).getId());
				List<GroupMember> gMember=query2.list();
				for(int j=0;j<gMember.size();j++){
					List<User> rua=session.createQuery("from User where Id="+gMember.get(j).getId().getMemberId()).list();
					if(rua.get(0).getGender()==(byte)0) gmember+=(rua.get(0).getName()+" ");
					else member+=(rua.get(0).getName()+" ");
				}
				tmp.put("member", member.toString());
				tmp.put("gmember", gmember.toString());
				array.add(tmp);
			}
			json.put("team", array);
		}catch(Exception e){e.printStackTrace();session.getTransaction().rollback();return null;}
		finally{
			session.close();
		}
		System.out.println(json.toString());
		response.setCharacterEncoding("utf-8");
		return json.toString();
		
	}

	@RequestMapping(value="/stu-team-info",method=RequestMethod.GET, produces={"text/html;charset=UTF-8;","application/json;"})
	@ResponseBody
	public String getMyGroup(int stuID){//int group_id,byte status
		JSONObject json=new JSONObject();
		Session session= HibernateUtil.factory.openSession();
		//int stuid=Integer.parseInt(request.getParameter("stuId"));
		List<GroupMember> gM=new ArrayList<GroupMember>();
		List<Group> group=new ArrayList<Group>();
		int count;
		try{
			Transaction ts=session.getTransaction();
			session.beginTransaction();
			Query query=session.createQuery("from GroupMember a where a.id.memberId="+stuID);
			gM=query.list();
			int gId=gM.get(0).getId().getGroupId();
			Query query1=session.createQuery("from Group where id="+gId);
			group=query1.list();Group g=group.get(0);
			json.put("teamName",g.getName());
			json.put("teamInfo", g.getInfo());
			JSONArray s=new JSONArray();
			gM=session.createQuery("from GroupMember a where a.id.groupId="+gId).list();
			json.put("memCounter", gM.size());
			for(int i=0;i<gM.size();i++){
				List<User> user=session.createQuery("from User where Id="+gM.get(i).getId().getMemberId()).list();
				JSONObject tmp=new JSONObject();
				tmp.put("memStuID", user.get(0).getId());
				tmp.put("name", user.get(0).getName());
				s.add(tmp);
			}
			JSONObject f=new JSONObject();
			f.put("arr", s);
			json.put("memList", f);
			List<Score> sc=session.createQuery("from Score a where a.id.checkedId="+stuID).list();
			double sum=0;
			for(int i=0;i<sc.size();i++){
				sum+=sc.get(i).getScore();
			}
			json.put("Score", sc.size()==0?0:sum/(double)sc.size());
		}catch(Exception e){e.printStackTrace();session.getTransaction().rollback();return null;}
		finally{
			session.close();
		}
		System.out.println(json.toString());
		return json.toString();
		
	}
	
	@RequestMapping(value="/stu-team-manage",method=RequestMethod.GET, produces={"text/html;charset=UTF-8;","application/json;"})
	@ResponseBody
	public String getLeaderGroup(int stuID){//int group_id,byte status
		JSONObject json=new JSONObject();
		Session session= HibernateUtil.factory.openSession();
		//int stuid=Integer.parseInt(request.getParameter("stuId"));
		List<GroupMember> gM=new ArrayList<GroupMember>();
		List<Group> group=new ArrayList<Group>();
		int count;
		try{
			Transaction ts=session.getTransaction();
			session.beginTransaction();
			Query query=session.createQuery("from GroupMember a where a.id.memberId="+stuID);
			gM=query.list();
			int gId=gM.get(0).getId().getGroupId();
			Query query1=session.createQuery("from Group where id="+gId);
			group=query1.list();Group g=group.get(0);
			json.put("teamName",g.getName());
			json.put("teamInfo", g.getInfo());
			JSONArray s=new JSONArray(),array=new JSONArray();
			gM=session.createQuery("from GroupMember a where a.id.groupId="+gId).list();
			json.put("memCounter", gM.size());
			for(int i=0;i<gM.size();i++){
				List<User> user=session.createQuery("from User where Id="+gM.get(i).getId().getMemberId()).list();
				JSONObject tmp=new JSONObject();
				tmp.put("memStuID", user.get(0).getId());
				tmp.put("name", user.get(0).getName());
				s.add(tmp);
			}
			JSONObject f=new JSONObject();
			f.put("arr", s);
			json.put("memList", f);
			List<Application> app=session.createQuery("from Application where groupId="+gId+" and status=2").list();
			for(int i=0;i<app.size();i++){
				List<User> user=session.createQuery("from User where Id="+app.get(i).getStudentId()).list();
				JSONObject tmp=new JSONObject();
				tmp.put("appStuID", user.get(0).getId());
				tmp.put("name", user.get(0).getName());
				tmp.put("status", app.get(i).getStatus());
				array.add(tmp);
			}
			JSONObject w=new JSONObject();
			w.put("arr", array);
			json.put("memApp", w);
			json.put("appCounter", app.size());
			List<Score> sc=session.createQuery("from Score a where a.id.checkedId="+stuID).list();
			double sum=0;
			for(int i=0;i<sc.size();i++){
				sum+=sc.get(i).getScore();
			}
			json.put("Score", sc.size()==0?0:sum/(double)sc.size());
		}catch(Exception e){e.printStackTrace();session.getTransaction().rollback();return null;}
		finally{
			session.close();
		}
		System.out.println(json.toString());
		return json.toString();
		
	}
	
	@RequestMapping(value="/stu-team-score-list",method=RequestMethod.GET, produces={"text/html;charset=UTF-8;","application/json;"})
	@ResponseBody public String getTeamScore(String stuID){
		JSONObject json=new JSONObject();
		Session session= HibernateUtil.factory.openSession();
		//int stuid=Integer.parseInt(request.getParameter("stuId"));
		List<GroupMember> gM=new ArrayList<GroupMember>();
		int count;
		try{
			Transaction ts=session.getTransaction();
			session.beginTransaction();
			Query query=session.createQuery("from GroupMember a where a.id.memberId="+stuID);
			gM=query.list();
			int gId=gM.get(0).getId().getGroupId();
			JSONArray s=new JSONArray(),array=new JSONArray();
			gM=session.createQuery("from GroupMember a where a.id.groupId="+gId).list();
			json.put("counter", gM.size());
			for(int i=0;i<gM.size();i++){
				List<User> user=session.createQuery("from User where Id="+gM.get(i).getId().getMemberId()).list();
				JSONObject tmp=new JSONObject();
				//tmp.put("memStuID", user.get(0).getId());
				tmp.put("memID", user.get(0).getId());
				tmp.put("Name", user.get(0).getName());
				List<Score> sc=session.createQuery("from Score a where a.id.checkedId="+user.get(0).getId()).list();
				double sum=0;
				for(int j=0;j<sc.size();j++){
					sum+=sc.get(j).getScore();
				}
				json.put("Score", sc.size()==0?0:sum/(double)sc.size());
				s.add(tmp);
			}
			json.put("Arr", s);
		}catch(Exception e){e.printStackTrace();session.getTransaction().rollback();return null;}
		finally{
			session.close();
		}
		//System.out.println(json.toString());
		return json.toString();
	}
	
	@RequestMapping(value="/stu-team-mem-score",method=RequestMethod.GET)
	@ResponseBody public String setTeamScore(HttpServletRequest request,HttpServletResponse response){
		Session session=HibernateUtil.openSession();
		try{
		//JSONObject json=JSONObject.fromObject(request);
		String id=request.getParameter("stuID");
		//String id=json.get("stuID").toString();
		//	//int id=Integer.parseInt(stuID);
		int count=Integer.parseInt(request.getParameter("count"));
		session.beginTransaction();
		System.out.println(count);
		for(int i=0;i<count;i++){
			
			String mid=request.getParameter("memList["+i+"][memID]"),scr=request.getParameter("memList["+i+"][Score]");
			System.out.println(mid + scr);
			List<Score> sc=session.createQuery("from Score a where a.id.memId="+id+"and a.id.checkedId="+request.getParameter("memlist["+i+"][memID]")).list();
			if(sc.size()==0){
				System.out.println(mid);
				Score score=new Score();
				score.setId(new ScoreId());
				score.getId().setCheckedId(Integer.parseInt(mid));
				score.getId().setMemId(Integer.parseInt(id));
				//score.getId().setMemId(id);
				score.setScore(Double.parseDouble(scr));
				session.save(score);
			}
			else{
				session.createQuery("update Score a set score="+scr+" where a.id.memId="+id+"and a.id.checkedId="+mid);
			}
		}
		session.getTransaction().commit();
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
			return "{status:1}";}
		finally{
			session.close();
		}
		return "{status:0}";
	}
}
