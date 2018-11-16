package com.example.demo.model.request;

import io.swagger.annotations.ApiModelProperty;

import java.util.List;

/**
 * Created by 44910_000 on 2018/7/1.
 */
public class JoinConferenceGroup {
    @ApiModelProperty(value = "论文编号")
    private Integer paperID;
    private List<JoinConferencePeople> joinConferencePeopleList;
    @ApiModelProperty(value = "注册费缴纳凭证")
    private List<String> evidence;

    public Integer getPaperID() {
        return paperID;
    }

    public void setPaperID(Integer paperID) {
        this.paperID = paperID;
    }

    public List<JoinConferencePeople> getJoinConferencePeopleList() {
        return joinConferencePeopleList;
    }

    public void setJoinConferencePeopleList(List<JoinConferencePeople> joinConferencePeopleList) {
        this.joinConferencePeopleList = joinConferencePeopleList;
    }

    public List<String> getEvidence() {
        return evidence;
    }

    public void setEvidence(List<String> evidence) {
        this.evidence = evidence;
    }
}
