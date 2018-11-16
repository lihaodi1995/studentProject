package com.example.demo.model.entity;

import io.swagger.annotations.ApiModelProperty;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class AttachmentEntity {
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "id")
    private Integer id;

    @ApiModelProperty(value = "存储路径")
    @Column(columnDefinition = "text")
    private String storagePath;

    public AttachmentEntity() {
    }

    public AttachmentEntity(String storagePath) {
        this.storagePath = storagePath;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getStoragePath() {
        return storagePath;
    }

    public void setStoragePath(String storagePath) {
        this.storagePath = storagePath;
    }

//    public enum ResourceType
//    {
//        Paper,Template;
//
//        public static boolean contains(String type)
//        {
//            ResourceType[] types = values();
//            for(ResourceType tmp:types)
//                if(tmp.name().equals(type))
//                    return true;
//            return false;
//        }
//    }
}
