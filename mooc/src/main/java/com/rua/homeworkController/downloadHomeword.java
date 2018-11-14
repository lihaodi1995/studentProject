package com.rua.homeworkController;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.io.FileUtils;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.rua.homeworkController.ZipCompressor;;

@Controller
public class downloadHomeword {
	
	String basePath = "/home/";
	
	@RequestMapping("/homework")
	public String homework(Model model)
	{
		return "homework";
	}
	
	
	@RequestMapping(value = "/downloadHomeworkRequest", method = RequestMethod.GET)
	public void downloadResourceRequest(ModelMap model, HttpServletRequest request,
			HttpServletResponse response) throws IOException
	{
		String taskid = request.getParameter("files");
		System.out.println(taskid);
		ZipCompressor zc = new ZipCompressor(basePath+"doc/ziphw/homework.zip");   
		ArrayList<String> list = new ArrayList();
		taskid = taskid.substring(0, taskid.length()-1);
		String[] strList = taskid.split(",");
		for(int i = 0;i<strList.length;i++)
			System.out.println(strList[i]);
		for(int i = 0;i<strList.length;i++)
		{
			String s = "homework/"+strList[i];
			list.add(s);
		}
			
		
		zc.list = list;
        zc.compress(basePath+"doc/homework");
        
       
	}
	
	
	@RequestMapping(value = "/downloadHomework", method = RequestMethod.GET)
	public ResponseEntity<byte[]> downloadResource(ModelMap model, HttpServletRequest request,
			HttpServletResponse response) throws IOException
	{
		String path=basePath+"doc/ziphw/homework.zip";  
        File file=new File(path);  
        HttpHeaders headers = new HttpHeaders();    
        String fileName=new String("homework.zip".getBytes("UTF-8"),"iso-8859-1");//为了解决中文名称乱码问题  这个homewor.zip是浏览器下载文件的名字
        headers.setContentDispositionFormData("attachment", fileName);   
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);   
        return new ResponseEntity<byte[]>(FileUtils.readFileToByteArray(file),    
                                          headers, HttpStatus.CREATED);    
	}
}
