package com.example.demo.security;

import org.apache.shiro.authc.UsernamePasswordToken;

/**
 * @Reference :https://blog.csdn.net/cckevincyh/article/details/79629022
 * @Description:
 * @Date created at 2018/6/30 18:23
 **/
public class UserToken extends UsernamePasswordToken {
    private String role;

    public UserToken(final String username, final String password, String role) {
        super(username,password);
        this.role = role;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }
}
