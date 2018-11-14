package com.rua.other;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
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
import model.User;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import net.sf.jxls.reader.ReaderBuilder;
import net.sf.jxls.reader.XLSReader;
import net.sf.jxls.transformer.Workbook;
import net.sf.jxls.transformer.XLSTransformer;

@Controller
public class applicationController {
	
	@RequestMapping(value="/s")
	public void test(){
		//addApplication("1231","252651");
	}
	
	@RequestMapping(value="/stu-team-apply",method=RequestMethod.POST)
	public @ResponseBody String addApplication(String stuID,String teamName){//int student_id,int group_id
		Session session=HibernateUtil.factory.openSession();
		JSONObject resp=new JSONObject();
		//JSONArray array=JSONArray.fromObject(request);
		System.out.println(stuID+" "+teamName);
		try{
		session.beginTransaction();
		List<Group> group=session.createQuery("from Group where name=\'"+teamName+"\'").list();
		int group_id=group.get(0).getId();
		Application app=new Application(Integer.parseInt(stuID),(group_id),(byte)2);
		session.save(app);
		session.getTransaction().commit();
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
			resp.put("status", 1);
			return resp.toString();
		}finally{
			session.close();
		}
		resp.put("status", 0);
		return resp.toString();
	}
	
	@RequestMapping(value="stu-team-status",method=RequestMethod.GET)
	public @ResponseBody String checkStatus(String stuID){
		//System.out.println(request);
		Session session=HibernateUtil.factory.openSession();
		//JSONObject json=JSONObject.fromObject(request);
		JSONObject res=new JSONObject();
	//	String stuname=json.get("stuName").toString();
		System.out.println("stuID"+stuID);
		try{
		session.beginTransaction();
		List<User> user=session.createQuery("from User where ID="+stuID).list();
		int stu=user.get(0).getId();
		List<GroupMember> gm=session.createQuery("from GroupMember a where a.id.memberId="+stu).list();
		if(gm.size()==0){
			res.put("status", 0);
			System.out.println(res);
			return res.toString();
		}
		else{
			List<Group> gp=session.createQuery("from Group where ID="+gm.get(0).getId().getGroupId()).list();
			if(gp.get(0).getManagerId()==stu){
				res.put("status", 1);
			}
			else res.put("status", 2);
			return res.toString();
		}
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
			res.put("status", 4);
			session.close();
			return res.toString();
		}finally{
			session.close();
		}
	}
	
	@RequestMapping(value="stu-team-manage-approval",method=RequestMethod.POST)
	public @ResponseBody String checkApplication(String appStuID,String approve){
		Session session=HibernateUtil.factory.openSession();
		JSONObject resp=new JSONObject();
		String status=approve;
		try{

		session.beginTransaction();
		if(status.equals("0")) {//更新成员表
			Query query1=session.createQuery("from Application where studentId="+appStuID+" and status=2");
			List<Application> app=query1.list();
			GroupMember member=new GroupMember();
			GroupMemberId id=new GroupMemberId();
			id.setGroupId(app.get(0).getGroupId());
			id.setMemberId(app.get(0).getStudentId());
			member.setId(id);
			session.save(member);
			System.out.println("mmmmm"+id);
		}
		session.getTransaction().commit();
		System.out.println(status);
		noteApplication(session,appStuID,status);
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
			session.close();
			resp.put("status", 1);
			return resp.toString();
		}finally{
			session.close();
		}
		resp.put("status",0);
		return resp.toString();
	}
	
	public byte noteApplication(Session session,String student_id,String status){//int student_id
		//String student_id=request.getParameter("student_id");
		Query query=session.createQuery("from Application where studentId="+student_id);
		session.beginTransaction();
		List<Application> app=query.list();
		Query query2=session.createQuery("update Application t set t.status="+status+" where t.studentId="+student_id);
		query2.executeUpdate();
		byte stus=app.get(0).getStatus();
		if(stus==(byte)1){
			Query query1=session.createQuery("delete from Application where studentId="+student_id);
			query1.executeUpdate();
			
			session.getTransaction().commit();
		}
		System.out.println(stus);
		session.getTransaction().commit();
		return app.get(0).getStatus();
		}
		
	@RequestMapping(value="/stu-team-list",method=RequestMethod.GET, produces={"text/html;charset=UTF-8;","application/json;"})
	@ResponseBody
	public String showGroup(){
		JSONObject json=new JSONObject();
		Session session= HibernateUtil.factory.openSession();
		List<Group> group=new ArrayList<Group>();
		int count;
		try{
			session.beginTransaction();
			Query query=session.createQuery("from Group where status=0");
			group=query.list();count=group.size();
			json.put("TeamCounter", count);
			JSONArray array=new JSONArray();
			for(int i=0;i<count;i++){
				JSONObject tmp=new JSONObject();
				tmp.put("teamName", group.get(i).getName());
				tmp.put("teamInfo", group.get(i).getInfo());
				Query query1=session.createQuery("from User where id="+group.get(i).getManagerId());
				List<User> user=query1.list();
				tmp.put("teamCrter", user.get(0).getName());
				
				JSONArray mem=new JSONArray();
				Query query2=session.createQuery("from GroupMember a where a.id.groupId="+group.get(i).getId());
				List<GroupMember> gMember=query2.list();
				tmp.put("teamMemCounter", gMember.size());
				for(int j=0;j<gMember.size();j++){
					List<User> rua=session.createQuery("from User where Id="+gMember.get(j).getId().getMemberId()).list();
					JSONObject tmp2=new JSONObject();
					tmp2.put("name", rua.get(0).getName());
					tmp2.put("stuID", rua.get(0).getId());
					mem.add(tmp2);
				}
				tmp.put("teamMemArr", mem);
				array.add(tmp);
			}
			json.put("TeamListArr", array);
		}catch(Exception e){e.printStackTrace();session.getTransaction().rollback();return null;}
		finally{
			session.close();
		}
		System.out.println(json.toString());
		return json.toString();
		
	}
	

}
