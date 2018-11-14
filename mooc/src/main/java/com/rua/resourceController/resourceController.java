package com.rua.resourceController;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.io.FileUtils;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.Query;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import model.HibernateUtil;
import model.Upload;
import model.User;
import net.sf.json.JSONObject;





@Controller
public class resourceController {
	int resourceid = 3;
	String basePath = "/home/";
	
	@RequestMapping(value = "/resource")
	public String resource(ModelMap model)
	{
		return "resource";
	}
	
	@RequestMapping(value = "/tcresource")
	public String tcresource(ModelMap model)
	{
		return "tc-src";
	}
	
	@RequestMapping(value = "/downloadResourceRequest", method = RequestMethod.GET)
	public void downloadResourceRequest(ModelMap model, HttpServletRequest request,
			HttpServletResponse response) throws IOException
	{
		String str = request.getParameter("files");
		System.out.println(str);
		ZipCompressor zc = new ZipCompressor(basePath+"doc/zip/resource.zip");   
		ArrayList<String> list = new ArrayList();
		str = str.substring(0, str.length()-1);
		String[] strList = str.split(",");
		for(int i = 0;i<strList.length;i++)
			System.out.println(strList[i]);
		for(int i = 0;i<strList.length;i++)
		{
			String s = "resource/"+strList[i];
			list.add(s);
		}
			
		
		zc.list = list;
        zc.compress(basePath+"doc/resource");
        
       
	}
	
	
	@RequestMapping(value = "/downloadResource", method = RequestMethod.GET)
	public ResponseEntity<byte[]> downloadResource(ModelMap model, HttpServletRequest request,
			HttpServletResponse response) throws IOException
	{
		String path=basePath+"doc/zip/resource.zip";  
        File file=new File(path);  
        HttpHeaders headers = new HttpHeaders();    
        String fileName=new String("resource.zip".getBytes("UTF-8"),"iso-8859-1");//为了解决中文名称乱码问题  
        headers.setContentDispositionFormData("attachment", fileName);   
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);   
        return new ResponseEntity<byte[]>(FileUtils.readFileToByteArray(file),    
                                          headers, HttpStatus.CREATED);    
	}
	
	
	public void insertByHibernate(String fileName, String title, int id, String strdate, String hw) {
		// 读取配置文件
		Configuration cfg = new Configuration().configure();

		

		Session session = null;
		try {
			session = HibernateUtil.factory.openSession();
			// 开启事务
			session.beginTransaction();

//			Annotation annotation = new Annotation();
//			annotation.setPos(jo.getString("pos"));
//			annotation.setContent(jo.getString("content"));
//			annotation.setType(jo.getString("type"));
//			annotation.setFilename(jo.getString("filename"));
//			annotation.setUsername(username);
//			session.save(annotation);

			Upload upload = new Upload();
			upload.setPath(fileName);
			upload.setTs(strdate);
			upload.setTitle(title);
			upload.setTeacherId(id);
			upload.setNum(hw);
			session.save(upload);
			// 提交事务
			session.getTransaction().commit();
			
			

		} catch (Exception e) {
			e.printStackTrace();
			// 回滚事务
			session.getTransaction().rollback();
		} finally {
			if (session != null) {
				if (session.isOpen()) {
					// 关闭session
					session.close();
//					HibernateUtil.factory.close();
				}
			}
		}
	}
	
	
	public void insertByJDBC(String fileName, String title, int id, String strdate, String hw) throws ClassNotFoundException, SQLException
	{
		resourceid++;
		Class.forName("com.mysql.jdbc.Driver");
        
        String url="jdbc:mysql://localhost:3306/rua?characterEncoding=UTF-8";    //JDBC的URL    
        java.sql.Connection conn;
        conn = DriverManager.getConnection(url, "root", "");

        java.sql.Statement stmt = conn.createStatement(); //创建Statement对象
//        System.out.println("成功连接到数据库！");

        String sql = "insert into upload values"+"("+"\""+resourceid+"\","+"\""+title+"\",\""+hw+"\",\""+id+"\",\""+strdate+"\",\""+fileName+"\")";    //要执行的SQL
        System.out.println(sql);
        stmt.executeUpdate(sql);//创建数据对象
        System.out.println("****************************************");
            stmt.close();
            conn.close();
      

	}
	
	public static User searchByHibernate(String un){
		
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
	
	@RequestMapping("/api/tc-up-src")
	public String uploadHWtuozhuai(ModelMap model,@RequestParam("header") String title,@RequestParam("content") String content, @RequestParam("file") MultipartFile[] files, HttpServletRequest request,
			HttpServletResponse response) throws IOException, ClassNotFoundException, SQLException 
	{
		String username = request.getSession().getAttribute("sessionusername").toString();
		User user = searchByHibernate(username);
		
		for(int i = 0;i<files.length;i++)
		{
			MultipartFile file = files[i];

			//content : 组号

			
			System.out.println(username+" "+title+" "+content);
			//读取上传的文件内容
			InputStream is = file.getInputStream();
			
			BufferedReader in = new BufferedReader(new InputStreamReader(is, "utf-8"));
			   StringBuffer buffer = new StringBuffer();
			   String line = "";
			   while ((line = in.readLine()) != null){
			     buffer.append(line);
			   }
			System.out.println(buffer.toString());
			
			String fileName =  file.getOriginalFilename();
			System.out.println(fileName);
			
			//content现在是文字说明，以前是第几次作业
			//title是资源标题，现在按照title区分资源
			File wfile=new File(basePath+"doc/resource/"+title+"/"+fileName); 
			
			File fileParent = wfile.getParentFile();
			if (!fileParent.exists()) {
				fileParent.mkdirs();
			}
			
			file.transferTo(wfile);
			
			
			
			Date date= new Date();//创建一个时间对象，获取到当前的时间
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置时间显示格式
			String strdate = sdf.format(date);
			
//			insertByHibernate(fileName, title, user.getId(), strdate, content);
			insertByJDBC(fileName, title, user.getId(), strdate, content);
		}
		return "tc-src";
	}
	
	@RequestMapping(value = "/uploadSRC", method = RequestMethod.POST)
	public String uploadSRC(ModelMap model,@RequestParam("title") String title,@RequestParam("content") String content, @RequestParam("file") MultipartFile[] files, HttpServletRequest request,
			HttpServletResponse response) throws IOException, ClassNotFoundException, SQLException
	{
		
		String username = request.getSession().getAttribute("sessionusername").toString();
		User user = searchByHibernate(username);
		
		for(int i = 0;i<files.length;i++)
		{
			MultipartFile file = files[i];

			//content : 组号

			
			System.out.println(username+" "+title+" "+content);
			//读取上传的文件内容
			InputStream is = file.getInputStream();
			
			BufferedReader in = new BufferedReader(new InputStreamReader(is, "utf-8"));
			   StringBuffer buffer = new StringBuffer();
			   String line = "";
			   while ((line = in.readLine()) != null){
			     buffer.append(line);
			   }
			System.out.println(buffer.toString());
			
			String fileName =  file.getOriginalFilename();
			System.out.println(fileName);
			
			//content现在是文字说明，以前是第几次作业
			//title是资源标题，现在按照title区分资源
			File wfile=new File(basePath+"doc/resource/"+title+"/"+fileName); 
			
			File fileParent = wfile.getParentFile();
			if (!fileParent.exists()) {
				fileParent.mkdirs();
			}
			
			file.transferTo(wfile);
			
			
			
			Date date= new Date();//创建一个时间对象，获取到当前的时间
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置时间显示格式
			String strdate = sdf.format(date);
			
//			insertByHibernate(fileName, title, user.getId(), strdate, content);
			insertByJDBC(fileName, title, user.getId(), strdate, content);
		}
		return "tc-src";
	}
	
public static void deleteByHibernate(String hw){
		
		Session session = null;
		try{
			session = HibernateUtil.factory.openSession();
			session.beginTransaction();
			
			String hql = "delete Upload where title = :t";
			Query query  = session.createQuery(hql); 
			query.setParameter("t", hw);
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
	@RequestMapping(value = "/deleteSRC", method = RequestMethod.POST)
	public String deleteSRC(@RequestBody String str, Model model)
	{
		str = str.substring(0, str.length()-1);
		String[] strs = str.split(",");
		for(int i = 0;i<strs.length;i++)
		{
			System.out.println(strs[i]);
			deleteByHibernate(strs[i]);
			delAllFile(basePath+"doc/resource/"+strs[i]);
		}
			
		
		
		return "tc-src";
	}
	
}