package com.example.demo.model.response;

import java.util.List;

public class RepostInfo {

    private String modInfo;

    private List<String> files;

    private Long repostDate;

    public RepostInfo() {
    }

    public String getModInfo() {
        return modInfo;
    }

    public void setModInfo(String modInfo) {
        this.modInfo = modInfo;
    }

    public List<String> getFiles() {
        return files;
    }

    public void setFiles(List<String> files) {
        this.files = files;
    }

    public Long getRepostDate() {
        return repostDate;
    }

    public void setRepostDate(Long repostDate) {
        this.repostDate = repostDate;
    }
}
