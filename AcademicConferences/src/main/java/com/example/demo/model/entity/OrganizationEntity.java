package com.example.demo.model.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.*;
import java.io.Serializable;
import java.util.HashSet;
import java.util.Set;

@Entity
public class OrganizationEntity implements Serializable{
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "机构id")
    private Long id;

    @ApiModelProperty(value = "机构名称")
    private String name;

    @ApiModelProperty(value = "机构简介")
    @Column(columnDefinition = "text")
    private String intro;

    @ApiModelProperty(value = "会议")
    @OneToMany(mappedBy = "organization")
    @JsonIgnore
    private Set<ConferenceEntity> conferences;

    @ApiModelProperty(value = "机构管理员")
    @OneToMany(mappedBy = "organization")
    @JsonIgnore
    private Set<AdminEntity> admins;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getId() {
        return id;
    }

    public Set<ConferenceEntity> getConferences() {
        return conferences;
    }

    public void setConferences(Set<ConferenceEntity> conferences) {
        this.conferences = conferences;
    }

    public String getIntro() {
        return intro;
    }

    public void setIntro(String intro) {
        this.intro = intro;
    }

    public Set<AdminEntity> getAdmins() {
        return admins;
    }

    public void setAdmins(Set<AdminEntity> admins) {
        this.admins = admins;
    }

    public synchronized boolean addAdmin(AdminEntity admin)
    {
        if(this.admins == null)
            this.admins = new HashSet<>();
        if(!this.admins.contains(admin))
            this.admins.add(admin);
        else
            return false;
        return true;
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof OrganizationEntity && this.id.equals(((OrganizationEntity) obj).id);
    }
}
