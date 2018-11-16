package com.example.demo.model.entity;

import com.example.demo.model.base.Identification;
import com.example.demo.model.base.Role;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import java.io.Serializable;

/**
 * @Author : 叶明林
 * @Description: 记录可获得某个资源的组或者用户
 * @Date created at 2018/7/6 16:53
 **/
//@Entity
public class AccessEntity implements Serializable{
    @Id
    @GeneratedValue
    private Long id;

    private String role;

    private Long identificationId;


    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public boolean isIdentificationPermitted(Identification user)
    {
        if (role == null || role.equals(Role.ROLE_GUEST)) {
            return true;
        }
        else {
            return role.equals(user.getRole()) && this.identificationId == null ||
                    role.equals(user.getRole()) && this.identificationId != null
                            && user.getId().equals(this.identificationId);
        }
    }

    public Long getIdentificationId() {
        return identificationId;
    }

    public void setIdentificationId(Long identificationId) {
        this.identificationId = identificationId;
    }
}
