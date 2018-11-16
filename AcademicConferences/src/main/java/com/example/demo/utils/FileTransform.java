package com.example.demo.utils;

import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import org.apache.log4j.Logger;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

public class FileTransform {
    private static final Logger logger=Logger.getLogger(FileTransform.class);
    /**
    * @param base base64字符串
    * @return MutipartFile类型
    */
    public static MultipartFile Base64ToMultipartFile(String base){
        try{
            Base64.Decoder decoder=Base64.getDecoder();
            byte[] bytes=new byte[0];
            String[] str=base.split(",");
            if(str.length!=2){
                return null;
            }
            bytes= decoder.decode(str[1]);
            BASE64MultipartFile transfer=new BASE64MultipartFile(str[0],bytes);
            return transfer;
        }
        catch(Exception e){
            logger.warn(e.getMessage());
            throw new BusinessException(ExceptionInfo.PARAMS_ILLEGAL);
        }
    }

    /**
     * @param file MutipartFile类型
     * @return base64字符串
     */
    public static String MultipartFileToBase64(MultipartFile file){
        Base64.Encoder encoder = Base64.getEncoder();
        byte[] bytes=new byte[0];
        try {
            bytes=file.getBytes();
        } catch (IOException e) {
            throw new BusinessException(ExceptionInfo.FILE_READ_ERROR);
        }
        String str=encoder.encodeToString(bytes);
        str=((BASE64MultipartFile)file).getHeader()+";base64,"+str;
        return str;
    }

    /**
     * @param files MutipartFile类型列表
     * @return base64字符串列表
     */
    public static List<String> MultipartFileToBase64(List<MultipartFile> files){
        if(files==null) return null;
        List<String> list=new ArrayList<>();
        for(MultipartFile file:files){
            list.add(MultipartFileToBase64(file));
        }
        return list;
    }

    /**
     * @param bases base64字符串列表
     * @return MutipartFile类型列表
     */
    public static List<MultipartFile> Base64ToMultipartFile(List<String> bases){
        if(bases==null) throw new BusinessException(ExceptionInfo.UPLOAD_EMPTY_FILE);
        List<MultipartFile> list=new ArrayList<>();
        for(String base:bases){
            list.add(Base64ToMultipartFile(base));
        }
        return list;
    }
}
