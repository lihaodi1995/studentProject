package com.example.demo.service;

import com.example.demo.model.entity.AttachmentEntity;
import com.example.demo.component.UploadStrategy;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

/**
 * @Author : 叶明林
 * @Description: 文件上传
 * @Date created at 2018/5/31 12:11
 **/
public interface UploadFileService {
    /**
     * @param files 文件
     * @param object 生成文件储存路径的参考标志
     * @return 上传文件存储路径实体
     */
    List<AttachmentEntity> uploadFiles(List<MultipartFile> files, Object object,UploadStrategy uploadStrategy)throws IOException;

    /**
     * @param file 文件
     * @param object 生成文件储存路径的参考标志
     * @return 上传文件存储实体
     */
    AttachmentEntity uploadFile(MultipartFile file, Object object,UploadStrategy uploadStrategy)throws IOException;
}
