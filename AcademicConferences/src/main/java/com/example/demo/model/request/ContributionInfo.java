package com.example.demo.model.request;

import io.swagger.annotations.ApiModelProperty;

import java.util.List;

/**
 * @Author : 陈瀚清
 * @Description: 投稿信息
 * @Date created at 2018/7/1
 **/
public class ContributionInfo {

    @ApiModelProperty(value = "论文标题")
    private String title;

    @ApiModelProperty(value = "摘要")
    private String abstractInfo;

    @ApiModelProperty(value = "投稿")
    private String file;

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAbstractInfo() {
        return abstractInfo;
    }

    public void setAbstractInfo(String abstractInfo) {
        this.abstractInfo = abstractInfo;
    }

    public String getFile() {
        return file;
    }

    public void setFile(String file) {
        this.file = file;
    }
}
