package com.example.demo.service.impl;

import com.example.demo.exception.BusinessException;
import com.example.demo.model.entity.AttachmentEntity;
import com.example.demo.service.UploadFileService;
import com.example.demo.utils.FileFormatFilter;
import com.example.demo.component.UploadStrategy;
import org.apache.log4j.Logger;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

import static com.example.demo.exception.ExceptionInfo.*;

/**
 * @Author : 叶明林
 * @Description: 资源上传类，实现资源上传中消息记录等通用操作，
 *                  存储策略交给策略接口决定
 * @Date created at 2018/5/31 12:39
 **/

@Service
public class ResourceUploadService implements UploadFileService{
    private Logger logger = Logger.getLogger(ResourceDownloadServiceImpl.class);
    @Override
    public List<AttachmentEntity> uploadFiles(List<MultipartFile> files, Object object,UploadStrategy uploadStrategy)
    {
        List<AttachmentEntity> result = new LinkedList<>();
        for(MultipartFile file:files)
            result.add(this.uploadFile(file, object,uploadStrategy));
        return result;
    }

    public AttachmentEntity uploadFile(MultipartFile multipartFile, Object object ,UploadStrategy uploadStrategy)
    {
        if(uploadStrategy == null)
            throw new RuntimeException("上传策略为空");

        if(multipartFile == null || multipartFile.isEmpty() || multipartFile.getOriginalFilename().isEmpty())
            throw new BusinessException(UPLOAD_EMPTY_FILE);

        String contentType = multipartFile.getContentType();
        if (!contentType.contains(""))
            throw new BusinessException(UPLOAD_EMPTY_CONTENT_TYPE);

        String filePath = uploadStrategy.getStorePath(object);
        String fileName;
        try
        {
            FileFormatFilter fileFormatFilter = new FileFormatFilter() {
                @Override
                protected List<String> generateAcceptType() {
                    return uploadStrategy.getSupportTypeOfUploadFile();
                }
            };
            fileName = this.saveFile(multipartFile, filePath,fileFormatFilter);
            this.logger.info("上传文件: "+fileName+" (fileName); "+filePath+" (filePath);");
            return new AttachmentEntity(fileName);
        }
        catch (IOException t)
        {
            t.printStackTrace();
            throw new BusinessException(UPLOAD_SAVE_ERROR);
        }
    }


    /**
     * @param multipartFile 要保存的文件
     * @param path 存储目的目录
     * @return  文件绝对路径
     * @throws IOException 生成文件夹出错、保存文件出错
     */
    private String saveFile(MultipartFile multipartFile, String path,FileFormatFilter filter) throws IOException
    {
        File file = new File(path);
        if (!file.exists()&&!file.mkdirs())
            throw new IOException();
        String postfix = filter.getPostfixOfFile(multipartFile);
        if(!filter.isPostfixSupported(postfix))
            throw new BusinessException(UPLOAD_FORMAT_NOT_SUPPORTED);
        String absolutePath= path+File.separator+multipartFile.getOriginalFilename();
                        //+File.separator+postfix;
        File saveFile=new File(absolutePath);
        multipartFile.transferTo(saveFile);
        this.logger.info("保存文件: "+absolutePath+" (absolutePath); "
                +saveFile.getAbsolutePath()+" (saveFile.getAbsolutePath());");
        return saveFile.getAbsolutePath();
    }
}
