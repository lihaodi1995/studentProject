package com.example.demo.utils;

import com.example.demo.exception.BusinessException;
import org.apache.log4j.Logger;
import org.springframework.http.MediaType;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import static com.example.demo.exception.ExceptionInfo.FORMAT_ERROR;

/**
 * @Author : 叶明林
 * @Description: 文件类型检查
 * @Date created at 2018/5/31 12:15
 **/
public abstract class FileFormatFilter {
    private Logger logger = Logger.getLogger(FileFormatFilter.class);

    //文件头与文件格式的映射
    private final Map<String,String> headerToTypeMap=new HashMap<>();

    //文件类型与媒体类型的映射
    private final Map<String,MediaType> postfixToMediaTypeMap = new HashMap<>();

    //接受上传的格式列表
    private final List<String> acceptType;

    protected FileFormatFilter()
    {
        this.initHeaderToTypeMap();

        this.initPostfixToMediaTypeMap();

        this.acceptType=generateAcceptType();
    }

    private void initHeaderToTypeMap()
    {
        // 图片
        headerToTypeMap.put("FFD8FFE0", "jpg");
        headerToTypeMap.put("FFD8FF", "jpg");
        headerToTypeMap.put("89504E47", "png");
        headerToTypeMap.put("47494638", "gif");
        headerToTypeMap.put("49492A00", "tif");
        headerToTypeMap.put("424D", "bmp");
        //文本
        headerToTypeMap.put("3C3F786D6C", "xml");
        headerToTypeMap.put("68746D6C3E", "html");
        headerToTypeMap.put("D0CF11E0", "doc");
        headerToTypeMap.put("255044462D312E", "pdf");
        headerToTypeMap.put("504B0304", "docx");
        headerToTypeMap.put("52617221", "rar");
        //headerToTypeMap.put("75736167", "txt");           txt无固定文件头
        //音频
        headerToTypeMap.put("57415645", "wav");
        headerToTypeMap.put("41564920", "avi");
    }

    private void initPostfixToMediaTypeMap()
    {
        postfixToMediaTypeMap.put("jpg",MediaType.IMAGE_JPEG );
        postfixToMediaTypeMap.put("png",MediaType.IMAGE_PNG);
        postfixToMediaTypeMap.put("gif", MediaType.IMAGE_GIF);
        postfixToMediaTypeMap.put("tif", MediaType.parseMediaType("application/x-tif"));
        postfixToMediaTypeMap.put("bmp",MediaType.parseMediaType("application/x-bmp") );
        //文本
        postfixToMediaTypeMap.put("xml", MediaType.APPLICATION_XML);
        postfixToMediaTypeMap.put("html",MediaType.TEXT_HTML );
        postfixToMediaTypeMap.put("doc",MediaType.parseMediaType("application/msword") );
        postfixToMediaTypeMap.put("pdf",MediaType.APPLICATION_PDF );
        postfixToMediaTypeMap.put("docx",MediaType.parseMediaType("application/vnd.openxmlformats-officedocument.wordprocessingml.document") );
        postfixToMediaTypeMap.put("rar",MediaType.parseMediaType("application/x-rar") );
        //postfixToMediaTypeMap.put("txt",MediaType.TEXT_HTML );
        postfixToMediaTypeMap.put("xls",MediaType.parseMediaType("application/x-xls"));
        //音频
        postfixToMediaTypeMap.put("wav",MediaType.parseMediaType("audio/x-wav") );
        postfixToMediaTypeMap.put("avi",MediaType.parseMediaType("video/x-msvideo") );
    }

    /**
     * @return 支持的文件格式
     */
    abstract protected List<String> generateAcceptType();

    public boolean isPostfixSupported(MultipartFile file)throws IOException
    {
        return this.acceptType.contains(this.getPostfixOfFile(file));
    }

    public boolean isPostfixSupported(String postfix)
    {
        return this.acceptType.contains(postfix);
    }

    private String getFileHeader(MultipartFile file)throws IOException
    {
        String value;
        try(InputStream is=file.getInputStream())
        {
            value = this.calculateFileHeader(is);
        }
        return value;
    }

    /**
     * @param inputStream 文件流
     * @return 文件头
     * @throws IOException 文件读取错误
     */
    private String calculateFileHeader(InputStream inputStream)throws IOException
    {
        byte[] b = new byte[4];
        int byteLength=inputStream.read(b, 0, b.length);
        String ans = byteLength == 0 ? null :bytesToHexString(b);
        this.logger.info("文件头: "+ ans);
        return ans;
    }

    private String bytesToHexString(byte[] src)
    {
        StringBuilder builder = new StringBuilder();
        if (src == null || src.length <= 0)
            return null;
        String hv;
        for (byte aSrc : src)
        {
            hv = Integer.toHexString(aSrc & 0xFF).toUpperCase();
            if (hv.length() < 2)
                builder.append(0);
            builder.append(hv);
        }
        return builder.toString();
    }


    /**
     * @param file 需要检查类型的文件
     * @return 文件的后缀
     * @throws IOException 文件读取错误
     */
    public String getPostfixOfFile(MultipartFile file)throws IOException
    {
        String fileHeader=this.getFileHeader(file);
        String postFix = this.postfixMatch(fileHeader);
        if(postFix == null)
            throw new BusinessException(FORMAT_ERROR);
        return postFix;
    }

    /**
     * 获取文件需要支持的传输类型
     * @param file 文件
     * @return 传输类型
     */
    public MediaType getMediaType(File file)throws IOException
    {
        if(file == null||!file.exists())
            return MediaType.APPLICATION_OCTET_STREAM;

        InputStream inputStream = new FileInputStream(file);
        String fileHeader = this.calculateFileHeader(inputStream);

        String postfix = this.postfixMatch(fileHeader);

        return postfixToMediaTypeMap.get(postfix);
    }

    private String postfixMatch(String fileHeader)
    {
        if(fileHeader == null|| fileHeader.isEmpty())
            return null;
        Set<String> keys = this.headerToTypeMap.keySet();
        for(String key:keys)
            if(key.startsWith(fileHeader)||fileHeader.startsWith(key))
                return this.headerToTypeMap.get(key);
        return null;
    }
}
