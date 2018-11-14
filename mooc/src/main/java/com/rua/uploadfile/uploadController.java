package com.rua.uploadfile;

import java.awt.List;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

@Controller
public class uploadController {
	@RequestMapping(value="/upload")
	public String login(Model model)
	{
		return "upload";
	}
	
	//file upload
	@RequestMapping(value="/uploadfile",method = RequestMethod.POST)
	public String annotate(HttpServletRequest request,@RequestParam MultipartFile file, Model model) throws IOException
	{
	
		
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
		
		
		File wfile=new File("/home/doc/"+fileName); 
		
		File fileParent = wfile.getParentFile();
		if (!fileParent.exists()) {
			fileParent.mkdirs();
		}
		
		file.transferTo(wfile);
		
		
		System.out.println(request.getContextPath());
		
		return null;
	}
	
	//single file download
	@RequestMapping("download")    
    public ResponseEntity<byte[]> download() throws IOException {    
        String path="E:/workspace/mooc/doc/haha.txt";  
        File file=new File(path);  
        HttpHeaders headers = new HttpHeaders();    
        String fileName=new String("haha.txt".getBytes("UTF-8"),"iso-8859-1");//为了解决中文名称乱码问题  
        headers.setContentDispositionFormData("attachment", fileName);   
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);   
        return new ResponseEntity<byte[]>(FileUtils.readFileToByteArray(file),    
                                          headers, HttpStatus.CREATED);    
    }    
    
    @RequestMapping("zipdownload")   
    public void downloadZipFile(HttpServletResponse response) throws IOException {

        response.setContentType(MediaType.APPLICATION_OCTET_STREAM.toString());
        response.setHeader("Content-Disposition","attachment; filename=\"images.zip\"");

        String[] fileNames = {"1.jpg","2.jpg","3.jpg"};
        ZipOutputStream zipOutputStream = new ZipOutputStream(response.getOutputStream());

        for(String fileName : fileNames) {
            ZipEntry zipEntry = new ZipEntry(fileName);
            zipOutputStream.putNextEntry(zipEntry);
            FileInputStream inputStream = new FileInputStream("E:/workspace/mooc/doc/"+fileName);
            IOUtils.copy(inputStream,zipOutputStream);
            inputStream.close();
        }

        zipOutputStream.closeEntry();
        zipOutputStream.close();
    }
	
}
