package com.example.demo.model.request;

import io.swagger.annotations.ApiModelProperty;

import java.util.List;

public class AllConferenceInfo extends ConferenceInfo {

    @ApiModelProperty(value = "附件")
    private List<String> files;

    public List<String> getFiles() {
        return files;
    }

    public void setFiles(List<String> files) {
        this.files = files;
    }
}
