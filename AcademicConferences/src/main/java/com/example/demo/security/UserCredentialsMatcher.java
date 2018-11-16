package com.example.demo.security;

import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import org.apache.shiro.authc.AuthenticationInfo;
import org.apache.shiro.authc.AuthenticationToken;
import org.apache.shiro.authc.SimpleAuthenticationInfo;
import org.apache.shiro.authc.UsernamePasswordToken;
import org.apache.shiro.authc.credential.SimpleCredentialsMatcher;
import org.apache.shiro.cache.Cache;
import org.apache.shiro.cache.CacheManager;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * @Author : 叶明林
 * @Description: 登陆信息匹配
 * @Date created at 2018/5/17 11:55
 **/

public class UserCredentialsMatcher extends SimpleCredentialsMatcher {
    /*
    * 用户最多连续输入错误密码次数
    */
    private static final int ERROR_TIMES_LIMITED=5;

    private Cache<String, AtomicInteger> passwordRetryCache;

    UserCredentialsMatcher(CacheManager cacheManager) {
        passwordRetryCache = cacheManager.getCache("passwordRetryCache");
    }

    @Override
    public boolean doCredentialsMatch(AuthenticationToken token, AuthenticationInfo info) {
        UsernamePasswordToken usernamePasswordToken = (UsernamePasswordToken) token;
        SimpleAuthenticationInfo authenticationInfo  = (SimpleAuthenticationInfo)info;

        String passwordInDb = authenticationInfo.getCredentials().toString();

        String username = usernamePasswordToken.getUsername();
        String password = PasswordEncryption.encryptPassword(
                String.valueOf(usernamePasswordToken.getPassword()),
                new String(authenticationInfo.getCredentialsSalt().getBytes()));

        checkErrorTimes(username);

        boolean match = password!=null&&password.equals(passwordInDb);
        if (match)
            passwordRetryCache.remove(username);
        return match;
    }

    private void checkErrorTimes(String userName)
    {
        AtomicInteger retryCount = passwordRetryCache.get(userName);
        if (retryCount == null)
        {
            retryCount = new AtomicInteger(0);
            passwordRetryCache.put(userName, retryCount);
        }
        // 当用户连续输入密码错误5次以上禁止用户登录一段时间
        if (retryCount.incrementAndGet() > ERROR_TIMES_LIMITED)
            throw new BusinessException(ExceptionInfo.PASSWORD_ERROR_LIMIT);
    }
}
