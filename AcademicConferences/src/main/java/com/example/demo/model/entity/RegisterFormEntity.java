package com.example.demo.model.entity;

import com.example.demo.component.EmailsUtil;
import com.example.demo.exception.BusinessException;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.*;
import java.io.Serializable;
import java.util.*;

import static com.example.demo.exception.ExceptionInfo.EMAIL_INVALID;

@Entity
public class RegisterFormEntity implements Serializable{
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "注册id")
    private Integer id;

    @ApiModelProperty(value = "机构名称")
    private String organizationName;

    @ApiModelProperty(value = "统一社会信用代码")
    private String creditCode;

    @ApiModelProperty(value = "其他信息")
    @Column(columnDefinition = "text")
    private String legalInfo;

    @ApiModelProperty(value = "联系邮箱")
    private String mail;

    @ApiModelProperty(value = "附件")
    @OneToMany(cascade = CascadeType.PERSIST)
    private Set<AttachmentEntity> attachments;

    public RegisterFormEntity() {
    }

    public RegisterFormEntity(RegisterFormEntity formEntity) {
        this.organizationName = formEntity.organizationName;
        this.id = formEntity.id;
        this.creditCode = formEntity.creditCode;
        this.legalInfo = formEntity.legalInfo;
        this.handleStatus = formEntity.handleStatus;
        this.attachments = formEntity.attachments;
        this.mail = formEntity.mail;
    }

    public HandleStatus getHandleStatus() {
        return handleStatus;
    }

    public void setHandleStatus(HandleStatus handleStatus) {
        this.handleStatus = handleStatus;
    }

    public String getRegisterResult() {
        return registerResult;
    }

    public void setRegisterResult(String registerResult) {
        this.registerResult = registerResult;
    }

    public enum HandleStatus {
        Handling("Handling"),
        Refuse("Refuse"),
        Pending("Pending"),
        Accepted("Accepted");

        private String status;

        private static final Map<HandleStatus,Integer> priorityMap = new HashMap<>();

        static {
            priorityMap.put(Handling,0);
            priorityMap.put(Pending,1);
            priorityMap.put(Refuse,2);
            priorityMap.put(Accepted,2);
        }

        HandleStatus(String status) {
            this.status = status;
        }

        public String getStatus() {
            return status;
        }

        public static boolean contains(String type){
            HandleStatus[] allValues = values();
            for(HandleStatus status:allValues)
                if(status.name().equals(type))
                    return true;
            return false;
        }

        public Integer getPriority()
        {
            return priorityMap.get(HandleStatus.valueOf(status));
        }
    }

    public String getOrganizationName() {
        return organizationName;
    }

    public void setOrganizationName(String organizationName) {
        this.organizationName = organizationName;
    }

    @Column(columnDefinition = "char(10)")
    private HandleStatus handleStatus = HandleStatus.Pending;

    private String registerResult;              //审核结果

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getId() {
        return id;
    }

    public void setAttachments(Set<AttachmentEntity> attachments) {
        this.attachments = attachments;
    }

    public Set<AttachmentEntity> getAttachments() {
        return attachments;
    }

    public String getCreditCode() {
        return creditCode;
    }

    public void setCreditCode(String creditCode) {
        this.creditCode = creditCode;
    }

    public String getLegalInfo() {
        return legalInfo;
    }

    public void setLegalInfo(String legalInfo) {
        this.legalInfo = legalInfo;
    }

    public synchronized void addAttachments(Collection<? extends AttachmentEntity> collection)
    {
        if(this.attachments == null)
            this.attachments = new HashSet<>(collection == null?16:collection.size());
        if(collection!=null)
            this.attachments.addAll(collection);
    }

    public String getMail() {
        return mail;
    }

    public void setMail(String mail) {
        if(!EmailsUtil.isEmail(mail))
            throw new BusinessException(EMAIL_INVALID);
        this.mail = mail;
    }
}
