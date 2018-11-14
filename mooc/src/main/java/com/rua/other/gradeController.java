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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;
import java.sql.*;
import java.sql.SQLException;
import java.text.SimpleDateFormat;

import model.Absence;
import model.Application;
import model.Grade;
import model.Group;
import model.GroupMember;
import model.GroupMemberId;
import model.HibernateUtil;
import model.User;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;


@Controller
public class gradeController {
	
	@RequestMapping(value="/getGradeG",method=RequestMethod.GET)
	public @ResponseBody String getGrade(){
		Session session=HibernateUtil.openSession();
		JSONArray array=new JSONArray();
		try{
			session.beginTransaction();
			List<Grade> grade=session.createQuery("from Grade").list();
			for(int i=0;i<grade.size();i++){
			JSONObject tmp=new JSONObject();
			int id=grade.get(i).getId();
			tmp.put("ID", id);
			tmp.put("name", ((Group)session.createQuery("from Group where id="+id).list().get(0)).getName());
			tmp.put("grade", grade.get(i).getMark());
			array.add(tmp);
			}
		}catch(Exception e){
			e.printStackTrace();
			session.close();
			return array.toString();
		}finally{
			session.close();
		}
		return array.toString();
	}
	
	@RequestMapping(value="/postGradeG",method=RequestMethod.POST)
	public @ResponseBody String postGrade(@RequestParam("ID") String ID,@RequestParam("grade") String grade){
		Session session=HibernateUtil.openSession();
		JSONObject res=new JSONObject();
		//JSONObject req=JSONObject.fromObject(request);
		//System.out.print(req.toString());
		System.out.print("ssssssssssssssssssssssssssssssssssss");
		try{
			session.beginTransaction();
			//for(int i=0;i<req.size();i++){
			//JSONObject tmp=req;
			//session.createQuery("update Grade set mark="+tmp.get("grade")+"where id="+tmp.get("ID"));
			session.createQuery("update Grade set mark="+grade+"where id="+ID).executeUpdate();
			session.getTransaction().commit();
			
			//}
		}catch(Exception e){
			e.printStackTrace();
			session.close();
			res.put("status", 1);
			return res.toString();
		}finally{
			session.close();
		}
		res.put("status", 0);
		return res.toString();
	}
	
	@RequestMapping(value="/getAbsent",method=RequestMethod.GET, produces={"text/html;charset=UTF-8;","application/json;"})
	public @ResponseBody String getAbsence(){
		Session session=HibernateUtil.openSession();
		JSONArray res=new JSONArray();
		try{
			session.beginTransaction();
			List<Absence> absence=session.createQuery("from Absence").list();
			for(int i=0;i<absence.size();i++){
				JSONObject tmp=new JSONObject();
				tmp.put("stuID",absence.get(i).getId().getId());
				tmp.put("stuName",absence.get(i).getStuName());
				List<Group> g=session.createQuery("from Group where id="+absence.get(i).getGroupId()).list();
				tmp.put("stuTeam",g.get(0).getName());
				
				SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
				tmp.put("date",formatter.format(absence.get(i).getId().getDate()));
				res.add(tmp);

			}
		}catch(Exception e){
			e.printStackTrace();
			session.close();
			return res.toString();
		}finally{
			session.close();
		}
		return res.toString();
	}
	
	

}
