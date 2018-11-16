package com.example.demo.service;


import com.example.demo.model.base.Identification;

/**
 * @Author : 叶明林
 * @Description: 用户登陆、登出、修改密码等认证操作
 * @Date created at 2018/5/16 16:14
 **/
public interface AuthentificationService {
    /**
     * 登陆
     * @param userName 用户名
     * @param password 密码
     * @param role 角色
     */
    void login(String userName,String password,String role);

    /**
     * 注册
     * @param userName 用户名
     * @param password 密码
     * @param role 角色
     * @return 注册后的用户信息
     */
    Identification register(String userName,String password,String role);

    /**
     * 注销
     */
    void logout();

    /**
     * 获取当前用户的详细信息
     * @return 当前用户的详细信息
     */
    Identification getCurrentUser();

    /**
     * 更改当前用户的用户名
     * @param newUserName 新的用户名
     */
    void changeUserName(String newUserName);

    /**
     * 更改密码
     * @param userName 用户名
     * @param role 角色
     * @param originalPassword 原来的密码
     * @param newPassword 新的密码
     */
    void changePassword(String userName,String role,String originalPassword,String newPassword);

    /**
     * 判断当前用户是否登陆
     * @return 当前用户已登录时返回true
     */
    boolean currentUserIsAuthenticated();
}
