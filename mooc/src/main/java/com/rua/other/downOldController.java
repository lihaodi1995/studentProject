package com.rua.other;

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
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.rua.homeworkController.ZipCompressor;

@Controller
public class downOldController {
	@RequestMapping(value = "/downOld", method = RequestMethod.GET)
	public ResponseEntity<byte[]> downloadResource(ModelMap model, HttpServletRequest request,
			HttpServletResponse response) throws IOException
	{
		String basePath = "/home/";
		
		String str = request.getParameter("id");
		String fileName = null;
		String path = null;
		if(str.equals("1"))
		{
			path = "doc/old/2016res.zip";
			fileName=new String("2016res.zip");//为了解决中文名称乱码问题  这个homewor.zip是浏览器下载文件的名字s
		}
		else if(str.equals("2"))
		{
			path = "doc/old/2016hw.zip";
			fileName=new String("2016hw.zip");//为了解决中文名称乱码问题  这个homewor.zip是浏览器下载文件的名字
		}
		else if(str.equals("3"))
		{
			path = "doc/old/2015res.zip";
			fileName=new String("2015res.zip");//为了解决中文名称乱码问题  这个homewor.zip是浏览器下载文件的名字
		}
		else if(str.equals("4"))
		{
			path = "doc/old/2015hw.zip";
			fileName=new String("2015hw.zip");//为了解决中文名称乱码问题  这个homewor.zip是浏览器下载文件的名字
		}
//		=basePath+"doc/old/homework.zip";  
        File file=new File(basePath + path);  
        HttpHeaders headers = new HttpHeaders();    
        
        headers.setContentDispositionFormData("attachment", fileName);   
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);   
        return new ResponseEntity<byte[]>(FileUtils.readFileToByteArray(file),    
                                          headers, HttpStatus.CREATED);    
	}
}
