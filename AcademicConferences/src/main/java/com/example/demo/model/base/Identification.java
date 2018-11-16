package com.example.demo.model.base;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/6/30 18:51
 **/
public interface Identification {
    Long getId();

    String getUserName();

    String getRole();

    String getSalt();

    String getPassword();

    void setPassword(String password);

    void setUserName(String username);

    void setRole(String role);
}
