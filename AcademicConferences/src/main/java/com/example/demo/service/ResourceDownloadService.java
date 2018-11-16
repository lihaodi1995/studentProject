package com.example.demo.service;

import org.springframework.core.io.FileSystemResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import java.io.UnsupportedEncodingException;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/4 11:44
 **/
public interface ResourceDownloadService {
    /**
     * 下载指定资源
     * @param url 资源的url
     * @param mediaType 资源的mediaType
     * @return 下载实体
     * @throws UnsupportedEncodingException
     */
    ResponseEntity<FileSystemResource> download(String url,MediaType mediaType) throws UnsupportedEncodingException;
}
