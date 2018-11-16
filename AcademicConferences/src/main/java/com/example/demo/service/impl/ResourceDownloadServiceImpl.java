package com.example.demo.service.impl;

import com.example.demo.exception.BusinessException;
import com.example.demo.service.ResourceDownloadService;
import com.example.demo.utils.FileFormatFilter;
import org.apache.log4j.Logger;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.List;

import static com.example.demo.exception.ExceptionInfo.FILE_DOWNLOAD_ERROR;
import static com.example.demo.exception.ExceptionInfo.FILE_NOT_EXIST;

/**
 * @Reference : https://blog.csdn.net/Colton_Null/article/details/76696674
 *              https://blog.csdn.net/qq_33392133/article/details/78662439
 * @Description:
 * @Date created at 2018/7/4 11:52
 **/
@Service
public class ResourceDownloadServiceImpl implements ResourceDownloadService{
    private Logger logger = Logger.getLogger(ResourceDownloadServiceImpl.class);

    private FileFormatFilter fileFormatFilter = new FileFormatFilter() {
        @Override
        protected List<String> generateAcceptType() {
            return null;
        }
    };

    /**
     * @param url 资源的url
     * @param mediaType 资源mediaType
     * @return 下载文件实体
     */
    @Override
    public ResponseEntity<FileSystemResource> download(String url,MediaType mediaType) throws UnsupportedEncodingException {
        if(url == null)
            return null;

        File file = new File(url);
        if (file.exists()) {
            HttpHeaders headers = new HttpHeaders();
            String contentDisposition = new String(file.getName().getBytes(),"utf-8");
            headers.add("Cache-Control", "no-cache, no-store, must-revalidate");
            headers.add("Content-Disposition", String.format("attachment;filename=\"%s\"",contentDisposition) );
            headers.add("Pragma", "no-cache");
            headers.add("Expires", "0");
            ResponseEntity<FileSystemResource> responseEntity ;
            try
            {
                MediaType contentType = (mediaType == null?this.fileFormatFilter.getMediaType(file):mediaType);
                this.logger.info("download contentType: "+contentType.getType());
                responseEntity = ResponseEntity
                        .ok()
                        .headers(headers)
                        .contentLength(file.length())
                        .contentType(contentType)
                        .body(new FileSystemResource(file));
            }
            catch (IOException e)
            {
                this.logger.info(e.getMessage());
                throw new BusinessException(FILE_DOWNLOAD_ERROR);
            }

            return responseEntity;
        }
        throw new BusinessException(FILE_NOT_EXIST);
    }
}
