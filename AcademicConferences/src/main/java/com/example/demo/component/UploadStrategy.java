package com.example.demo.component;

import com.example.demo.model.base.ResourceType;

import java.util.List;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/2 15:37
 **/
public interface UploadStrategy {
    /**
     * @return 上传文件存放目录
     */
    String getStorePath(Object object);

    /**
     * @return 文件支持类型
     */
    List<String> getSupportTypeOfUploadFile();

    /**
     * @return 使用该策略的资源类型
     */
    ResourceType getSupportResourceType();
}
