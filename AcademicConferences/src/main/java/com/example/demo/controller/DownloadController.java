package com.example.demo.controller;

import com.example.demo.model.base.Role;
import com.example.demo.service.OrganizationService;
import com.example.demo.service.ResourceDownloadService;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.UnsupportedEncodingException;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/6 16:12
 **/
@RestController
@RequestMapping(value = "/download")
public class DownloadController {
    private final ResourceDownloadService resourceDownloadService;

    private final OrganizationService organizationService;

    @Autowired
    public DownloadController(ResourceDownloadService resourceDownloadService, OrganizationService organizationService) {
        this.resourceDownloadService = resourceDownloadService;
        this.organizationService = organizationService;
    }

    @GetMapping(value = "/excel/conference")
    @RequiresRoles(value = Role.ROLE_ORGANIZER)
    public ResponseEntity<FileSystemResource> downloadExcel(@RequestParam int conference_id)
    {
        return this.organizationService.getExcelOfConference(conference_id);
    }

    @GetMapping(value = "/file")
    public ResponseEntity<FileSystemResource> downloadFile(@RequestParam String url) throws UnsupportedEncodingException {
        return this.resourceDownloadService.download(url,null);
    }
}
