package com.rua.homeworkController;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.hibernate.Session;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.Query;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;


import model.GroupMember;
import model.HibernateUtil;
import model.SubText;
import model.Task;
import model.Upload;
import model.User;
import net.sf.json.JSONObject;

@Controller
public class homeworkController {
	String basePath = "/home/";
	
	@RequestMapping("/publishHW")
	public String publishHW(Model model,HttpServletRequest request,HttpServletResponse response)
	{
		String hwtitle = request.getParameter("title");
		String hwexplain = request.getParameter("explain");
		String hwweight = request.getParameter("weight");
		
		System.out.println(hwtitle+" "+hwexplain+" "+hwweight);
		insertByHibernateTask(hwtitle, hwexplain, hwweight);
		
		return "tc-hw";
	}
	
public static User searchUserByHibernate(String un){
		
		Session session = null;
		List<User> results = new ArrayList<User>();
		try{
			session = HibernateUtil.factory.openSession();
			session.beginTransaction();
			
			String hql = "FROM User u WHERE u.name = \'"+un+"\'";
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
		
		return results.get(0);
	}
	
public static GroupMember searchGroupMByHibernate(int userid){
	
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
//	HibernateUtil.factory.close();
	
	return results.get(0);
}



	@RequestMapping("/uploadHW")
	public String uploadHW(ModelMap model, @RequestParam MultipartFile file, @RequestParam("info") String info, @RequestParam("title") String title, HttpServletRequest request,
			HttpServletResponse response) throws IOException, ClassNotFoundException, SQLException
	{
		System.out.println("infotitle "+info+" "+title);
		String username = request.getSession().getAttribute("sessionusername").toString();
		User user = searchUserByHibernate(username);
		GroupMember gm = searchGroupMByHibernate(user.getId());
		
		
		InputStream is = file.getInputStream();
		
		BufferedReader in = new BufferedReader(new InputStreamReader(is, "utf-8"));
		   StringBuffer buffer = new StringBuffer();
		   String line = "";
		   while ((line = in.readLine()) != null){
		     buffer.append(line);
		   }
//		System.out.println(buffer.toString());
		
		String fileName =  file.getOriginalFilename();
		System.out.println(fileName);
		
		//index 是第几次作业
		//gm.getid是第几组
		//title是作业标题 使用这个来表示第几次作业 index就先不用了
//		File wfile=new File("doc/homework/"+index+"/"+gm.getId().getGroupId()+"/"+fileName); 
		File wfile=new File(basePath+"doc/homework/"+title+"/"+gm.getId().getGroupId()+"/"+fileName); 
		
		
		File fileParent = wfile.getParentFile();
		if (!fileParent.exists()) {
			fileParent.mkdirs();
		}
		
		file.transferTo(wfile);
		
		insertByHibernateSubTask(info, "", gm.getId().getGroupId(), fileName, title);
		
//		User user = searchByHibernate(username);
//		
//		for(int i = 0;i<files.length;i++)
//		{
//			MultipartFile file = files[i];
//
//			//content : 组号
//
//			
//			System.out.println(username+" "+title+" "+content);
//			//读取上传的文件内容
//			InputStream is = file.getInputStream();
//			
//			BufferedReader in = new BufferedReader(new InputStreamReader(is, "utf-8"));
//			   StringBuffer buffer = new StringBuffer();
//			   String line = "";
//			   while ((line = in.readLine()) != null){
//			     buffer.append(line);
//			   }
//			System.out.println(buffer.toString());
//			
//			String fileName =  file.getOriginalFilename();
//			System.out.println(fileName);
//			
//			
//			File wfile=new File("doc/resource/"+content+"/"+fileName); 
//			
//			File fileParent = wfile.getParentFile();
//			if (!fileParent.exists()) {
//				fileParent.mkdirs();
//			}
//			
//			file.transferTo(wfile);
//			
//			
//			
//			Date date= new Date();//创建一个时间对象，获取到当前的时间
//			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置时间显示格式
//			String strdate = sdf.format(date);
//			
////			insertByHibernate(fileName, title, user.getId(), strdate, content);
//			insertByJDBC(fileName, title, user.getId(), strdate, content);
//		}
		return "homework-stu";
	}
	
	
	public void insertByHibernateSubTask(String info, String indextask, int groupid, String fileName, String taskTitle) {
		// 读取配置文件
		Configuration cfg = new Configuration().configure();
		Session session = null;
		try {
			session = HibernateUtil.factory.openSession();
			// 开启事务
			session.beginTransaction();
			
			SubText t = new SubText();
			t.setInfo(info);
//			t.setTaskId(Integer.parseInt(indextask));
			t.setTextId(fileName);
			t.setGroupId(groupid);
			t.setTaskTitle(taskTitle);
			session.save(t);
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
	
	public void insertByHibernateTask(String hwtitle, String hwexplain, String hwweight) {
		// 读取配置文件
		Configuration cfg = new Configuration().configure();
		Session session = null;
		try {
			session = HibernateUtil.factory.openSession();
			// 开启事务
			session.beginTransaction();
			
			Task t = new Task();
			t.setTitle(hwtitle);
			t.setCourseId(1);
			t.setInfo(hwexplain);
			t.setWeight(Double.parseDouble(hwweight));
			session.save(t);

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
	
public static void deleteByHibernate(String hw){
		
		Session session = null;
		try{
			session = HibernateUtil.factory.openSession();
			session.beginTransaction();
			
			String hql = "delete SubText where taskTitle = :num";
			Query query  = session.createQuery(hql); 
			query.setParameter("num", hw);
			query.executeUpdate();
			
			session.getTransaction().commit();
			
//			String hql1 = "delete Task where Title = :num";
//			Query query1  = session.createQuery(hql1); 
//			query1.setParameter("num", hw);
//			query1.executeUpdate();
//			
//			session.getTransaction().commit();
			
		}catch(Exception e){
			e.printStackTrace();
			session.getTransaction().rollback();
		}finally{
			HibernateUtil.closeSession(session);
		}
		//HibernateUtil.factory.close();
		
		return;
	}
public static void deleteByHibernate1(String hw){
	
	Session session = null;
	try{
		session = HibernateUtil.factory.openSession();
		session.beginTransaction();
		
//		String hql = "delete SubText where taskTitle = :num";
//		Query query  = session.createQuery(hql); 
//		query.setParameter("num", hw);
//		query.executeUpdate();
//		
//		session.getTransaction().commit();
		
		String hql1 = "delete Task where Title = :num";
		Query query1  = session.createQuery(hql1); 
		query1.setParameter("num", hw);
		query1.executeUpdate();
		
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
	
public static void delFolder(String folderPath) {
    try {
       delAllFile(folderPath); //删除完里面所有内容
       String filePath = folderPath;
       filePath = filePath.toString();
       java.io.File myFilePath = new java.io.File(filePath);
       myFilePath.delete(); //删除空文件夹
    } catch (Exception e) {
      e.printStackTrace(); 
    }
}

//删除指定文件夹下所有文件
//param path 文件夹完整绝对路径
  public static boolean delAllFile(String path) {
      boolean flag = false;
      File file = new File(path);
      if (!file.exists()) {
        return flag;
      }
      if (!file.isDirectory()) {
        return flag;
      }
      String[] tempList = file.list();
      File temp = null;
      for (int i = 0; i < tempList.length; i++) {
         if (path.endsWith(File.separator)) {
            temp = new File(path + tempList[i]);
         } else {
             temp = new File(path + File.separator + tempList[i]);
         }
         if (temp.isFile()) {
            temp.delete();
         }
         if (temp.isDirectory()) {
            delAllFile(path + "/" + tempList[i]);//先删除文件夹里面的文件
            delFolder(path + "/" + tempList[i]);//再删除空文件夹
            flag = true;
         }
      }
      return flag;
    }
	@RequestMapping(value = "/deleteHW", method = RequestMethod.POST)
	public String deleteHW(@RequestBody String str, Model model)
	{
		str = str.substring(0, str.length()-1);
		String[] strs = str.split(",");
		for(int i = 0;i<strs.length;i++)
		{
			deleteByHibernate(strs[i]);
			deleteByHibernate1(strs[i]);
			delAllFile(basePath+"doc/homework/"+strs[i]);
		}
			
		
		
		return "tc-src";
	}
	

//public void deleteByContent(String content)
//{
//	EntityLabel label = null;
//	Session session = null;
//	List<Integer> results = new ArrayList<Integer>();
//	try{
//		session = HibernateUtil.factory.openSession();
//		session.beginTransaction();
//		String hql = "SELECT id FROM EntityLabel where content = \'"+content+"\'";
//		Query query = session.createQuery(hql);
//		results = query.list();			
////		label = (Labels)session.get(Labels.class, results.get(0).getId());
//		System.out.println(results.get(0));
//		
//		label = new EntityLabel();
//		label.setId(results.get(0));
//		session.delete(label);
//		session.getTransaction().commit();
//		
//	}catch(Exception e)
//	{
//		e.printStackTrace();
//		session.getTransaction().rollback();
//	}finally{
//		HibernateUtil.closeSession(session);
//		
//	}
//	
//	return;
//}
public void updateByHibernateHWGrade(JSONObject jo)
{
	SubText st = null;
	Session session = null;
	List<SubText> results = new ArrayList<SubText>();
	try{
		session = HibernateUtil.factory.openSession();
		session.beginTransaction();
		String hql = "FROM SubText s where s.groupId =:gid and s.taskTitle = :tt and s.textId =:file";
		Query query = session.createQuery(hql);
		query.setParameter("gid", jo.getInt("group"));
		query.setParameter("tt", jo.getString("title"));
		query.setParameter("file", jo.getString("file"));
		results = query.list();			
//		label = (Labels)session.get(Labels.class, results.get(0).getId());
		System.out.println(results.get(0));
		
		st = results.get(0);
		st.setGrade(jo.getString("grade"));
		st.setComment(jo.getString("comment"));
		session.update(st);
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



//var dafen = {'group': group, 'title': pigai, 'file': file, 'grade': ("#hwgrade").val(), 'comment': $("#hwcomment").val()};
	@RequestMapping(value ="/hwgrade", method = RequestMethod.POST)
	public String hwgrade(Model model, @RequestBody String str,HttpServletRequest request,
			HttpServletResponse response) throws UnsupportedEncodingException
	{
		System.out.println(str);
		request.setCharacterEncoding("UTF-8");
		JSONObject jo = JSONObject.fromObject(str);
		updateByHibernateHWGrade(jo);
		
		return "tc-hw";
		
	}
}
