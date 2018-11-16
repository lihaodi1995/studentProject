package com.example.demo.model.entity;

import com.example.demo.exception.BusinessException;
import com.example.demo.model.base.EntityBase;
import com.example.demo.model.request.ConferenceInfo;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.*;
import java.io.Serializable;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Set;

import static com.example.demo.exception.ExceptionInfo.WRONG_DATE_RELATION;

@Entity
public class ConferenceEntity implements Serializable,EntityBase {
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "会议id")
    private Integer id;

    @ApiModelProperty(value = "会议标题")
    private String name;

    @ApiModelProperty(value = "会议简介")
    @Column(columnDefinition = "text")
    private String introduction;

    @ApiModelProperty(value = "征文信息")
    @Column(columnDefinition = "text")
    private String requirement;

    @ApiModelProperty(value = "创建日期")
    private Timestamp setDate;

    @ApiModelProperty(value = "截稿日期")
    private Timestamp ddlDate;

    @ApiModelProperty(value = "修改稿截止日期")
    private Timestamp repostDdlDate;

    @ApiModelProperty(value = "录用通知日期")
    private Timestamp informDate;

    @ApiModelProperty(value = "注册日期")
    private Timestamp registerDate;

    @ApiModelProperty(value = "会议开始日期")
    private Timestamp confBeginDate;

    @ApiModelProperty(value = "会议结束日期")
    private Timestamp confEndDate;

    @ApiModelProperty(value = "日程安排")
    @Column(columnDefinition = "text")
    private String schedule;

    @ApiModelProperty(value = "组织机构")
    @ManyToOne
    private OrganizationEntity organization;

    @ApiModelProperty(value = "论文模板")
    @OneToMany(cascade = CascadeType.PERSIST)
    private List<AttachmentEntity> template;

    @ApiModelProperty(value = "注册费用")
    private String cost;

    @ApiModelProperty(value = "住宿交通信息")
    @Column(columnDefinition = "text")
    private String accommodationInfo;

    @ApiModelProperty(value = "联系方式")
    private String contact;

    @ApiModelProperty(value = "投稿论文")
    @OneToMany(mappedBy = "conference")
    private Set<PaperEntity> papers;

    @ApiModelProperty(value = "参会报名表")
    @OneToMany(mappedBy = "conference")
    private Set<EntryFormEntity> entryForms;

//    public ConferenceEntity(OrganizationEntity organization, String title, String introduction, String requirement,
//                            Timestamp ddlDate, Timestamp informDate, Timestamp registerDate,
//                            Timestamp confBeginDate, Timestamp confEndDate, String schedule,
//                            AttachmentEntity template, String cost, String accommodationInfo, String contact){
//        setContact(contact);
//        setCost(cost);
//        setIntroduction(introduction);
//        setOrganization(organization);
//        setRequirement(requirement);
//        setSchedule(schedule);
//        setTemplate(template);
//        setTitle(title);
//        setAccommodationInfo(accommodationInfo);
//        setConfBeginDate(confBeginDate);
//        setConfEndDate(confEndDate);
//        setDdlDate(ddlDate);
//        setInformDate(informDate);
//        setRegisterDate(registerDate);
//
//    }

    public ConferenceEntity(OrganizationEntity organization, ConferenceInfo conferenceInfo, List<AttachmentEntity> attachmentEntityList){
        setContact(conferenceInfo.getContact());
        setCost(conferenceInfo.getCost());
        setIntroduction(conferenceInfo.getIntroduction());
        setOrganization(organization);
        setRequirement(conferenceInfo.getRequirement());
        setSchedule(conferenceInfo.getSchedule());
        setTemplate(attachmentEntityList);
        setName(conferenceInfo.getTitle());
        setAccommodationInfo(conferenceInfo.getAccommodationInfo());

        List<Timestamp> timestampList = new ArrayList<>();
        for(Timestamp date: new ArrayList<>(Arrays.asList(conferenceInfo.getDdlDate(),
                                                            conferenceInfo.getInformDate(),
                                                            conferenceInfo.getRegisterDate(),
                                                            conferenceInfo.getConfBeginDate(),
                                                            conferenceInfo.getConfEndDate()))){
            if(date != null)
                timestampList.add(date);
        }
        for(int i = 0; i < timestampList.size()-1; i++){
            if (!timestampList.get(i).before(timestampList.get(i+1)))
                throw new BusinessException(WRONG_DATE_RELATION);
        }
        setConfBeginDate(conferenceInfo.getConfBeginDate());
        setConfEndDate(conferenceInfo.getConfEndDate());
        setDdlDate(conferenceInfo.getDdlDate());
        setInformDate(conferenceInfo.getInformDate());
        setRegisterDate(conferenceInfo.getRegisterDate());
    }

    public ConferenceEntity() {
    }

    public Timestamp getSetDate() {
        return setDate;
    }

    public void setSetDate(Timestamp setDate) {
        this.setDate = setDate;
    }
    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getId() {
        return id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public List<AttachmentEntity> getTemplate() {
        return template;
    }

    public void setTemplate(List<AttachmentEntity> template) {
        this.template = template;
    }

    public OrganizationEntity getOrganization() {
        return organization;
    }

    public void setOrganization(OrganizationEntity organization) {
        this.organization = organization;
    }

    public Set<EntryFormEntity> getEntryForms() {
        return entryForms;
    }

    public void setEntryForms(Set<EntryFormEntity> entryForms) {
        this.entryForms = entryForms;
    }

    public Set<PaperEntity> getPapers() {
        return papers;
    }

    public void setPapers(Set<PaperEntity> papers) {
        this.papers = papers;
    }

    public String getAccommodationInfo() {
        return accommodationInfo;
    }

    public void setAccommodationInfo(String accommodationInfo) {
        this.accommodationInfo = accommodationInfo;
    }

    public String getContact() {
        return contact;
    }

    public void setContact(String contact) {
        this.contact = contact;
    }

    public String getCost() {
        return cost;
    }

    public void setCost(String cost) {
        this.cost = cost;
    }

    public String getIntroduction() {
        return introduction;
    }

    public void setIntroduction(String introduction) {
        this.introduction = introduction;
    }

    public String getRequirement() {
        return requirement;
    }

    public void setRequirement(String requirement) {
        this.requirement = requirement;
    }

    public Timestamp getConfBeginDate() {
        return confBeginDate;
    }

    public void setConfBeginDate(Timestamp confBeginDate) {
        this.confBeginDate = confBeginDate;
    }

    public Timestamp getConfEndDate() {
        return confEndDate;
    }

    public void setConfEndDate(Timestamp confEndDate) {
        this.confEndDate = confEndDate;
    }

    public Timestamp getDdlDate() {
        return ddlDate;
    }

    public void setDdlDate(Timestamp ddlDate) {
        this.ddlDate = ddlDate;
    }

    public Timestamp getInformDate() {
        return informDate;
    }

    public void setInformDate(Timestamp informDate) {
        this.informDate = informDate;
    }

    public Timestamp getRegisterDate() {
        return registerDate;
    }

    public void setRegisterDate(Timestamp registerDate) {
        this.registerDate = registerDate;
    }

    public String getSchedule() {
        return schedule;
    }

    public void setSchedule(String schedule) {
        this.schedule = schedule;
    }

    public Timestamp getRepostDdlDate() {
        return repostDdlDate;
    }

    public void setRepostDdlDate(Timestamp repostDdlDate) {
        this.repostDdlDate = repostDdlDate;
    }
}
