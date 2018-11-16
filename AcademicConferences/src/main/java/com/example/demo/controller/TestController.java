package com.example.demo.controller;

import com.example.demo.component.ExcelGenerator;
import com.example.demo.component.UploadStrategy;
import com.example.demo.model.base.Identification;
import com.example.demo.model.base.ResourceType;
import com.example.demo.model.base.Role;
import com.example.demo.service.ResourceDownloadService;
import com.example.demo.service.impl.ResourceUploadService;
import com.example.demo.service.impl.ResourceUploadService;
import com.example.demo.utils.FileTransform;
import com.example.demo.utils.IdentificationFactory;
import io.swagger.annotations.ApiModel;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.Arrays;
import java.util.List;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/4 14:12
 **/
@ApiModel(value = "测试")
@RestController
public class TestController {
    private final ResourceDownloadService resourceDownloadService;
    private final ResourceUploadService resourceUploadService;

    private final ExcelGenerator excelGenerator;

    private IdentificationFactory factory = IdentificationFactory.getInstance();

    @Autowired
    public TestController(ResourceDownloadService resourceDownloadService, ResourceUploadService resourceUploadService, ExcelGenerator excelGenerator) {
        this.resourceDownloadService = resourceDownloadService;
        this.resourceUploadService = resourceUploadService;
        this.excelGenerator = excelGenerator;
    }

    @GetMapping(value = "/file/download")
    public ResponseEntity<FileSystemResource> downloadFile(@RequestParam String fileUrl) throws UnsupportedEncodingException {
        return this.resourceDownloadService.download(fileUrl,null);
    }

    @PostMapping(value = "/file/upload")
    public void uploadTest(@RequestBody MultipartFile file){
        resourceUploadService.uploadFile(file, null, new UploadStrategy() {
            @Override
            public String getStorePath(Object object) {
                return "/usr/share/conferenceRegistrationForm";
            }
            @Override
            public List<String> getSupportTypeOfUploadFile() {
                return Arrays.asList("doc","docx","pdf");
            }
            @Override
            public ResourceType getSupportResourceType() {
                return ResourceType.Paper;
            }
        });
    }


    @GetMapping("/password")
    public void changePassword(@RequestParam String username,@RequestParam String password,@RequestParam String role)
    {
        Identification identification = factory.getEntityByUserName(username,role);
        identification.setPassword(password);
        factory.saveEntity(identification);
    }
}
