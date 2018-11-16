package com.example.demo.model.response;

import com.example.demo.model.entity.AttachmentEntity;
import com.example.demo.model.entity.RegisterFormEntity;
import com.fasterxml.jackson.annotation.JsonIgnore;

import java.util.HashSet;
import java.util.Set;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/6/30 20:42
 **/
public class RegisterFormInfo extends RegisterFormEntity{
    private Set<String> attachmentURLs;

    public RegisterFormInfo(RegisterFormEntity registerFormEntity) {
        super(registerFormEntity);
        Set<AttachmentEntity> attachmentEntities = registerFormEntity.getAttachments();
        if(attachmentEntities!=null)
        {
            this.attachmentURLs = new HashSet<>(attachmentEntities.size());
            for(AttachmentEntity x:attachmentEntities)
                this.attachmentURLs.add(x.getStoragePath());
        }
    }

    @Override
    @JsonIgnore
    public Set<AttachmentEntity> getAttachments() {
        return null;
    }

    public Set<String> getAttachmentURLs() {
        return attachmentURLs;
    }

    public void setAttachmentURLs(Set<String> attachmentURLs) {
        this.attachmentURLs = attachmentURLs;
    }
}
