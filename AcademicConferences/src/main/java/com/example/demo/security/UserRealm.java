package com.example.demo.security;

import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import com.example.demo.model.base.Identification;
import com.example.demo.utils.IdentificationFactory;
import org.apache.log4j.Logger;
import org.apache.shiro.authc.AuthenticationException;
import org.apache.shiro.authc.AuthenticationInfo;
import org.apache.shiro.authc.AuthenticationToken;
import org.apache.shiro.authc.SimpleAuthenticationInfo;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.authz.SimpleAuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.subject.PrincipalCollection;
import org.apache.shiro.util.ByteSource;

import javax.annotation.PostConstruct;
import java.util.HashSet;
import java.util.Set;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/5/17 12:01
 **/
public class UserRealm extends AuthorizingRealm {
    private Logger logger = Logger.getLogger(UserRealm.class);

    private IdentificationFactory factory = IdentificationFactory.getInstance();

    /**
     * 提供用户信息返回权限信息
     */
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principals) {
        Identification identification = (Identification) principals.getPrimaryPrincipal();
        String username = identification.getUserName();
        logger.info(username+" 权限验证");
        SimpleAuthorizationInfo authorizationInfo = new SimpleAuthorizationInfo();
        // 根据用户名查询当前用户拥有的角色
        Identification user = this.factory.getEntityByUserName(username,identification.getRole());
        Set<String> roleNames = new HashSet<>();
        roleNames.add(user.getRole());
        authorizationInfo.setRoles(roleNames);
        return authorizationInfo;
    }

    /**
     * 提供账户信息返回认证信息
     */
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken token) throws AuthenticationException {
        UserToken userToken = (UserToken) token;
        String username = userToken.getPrincipal().toString();

        Identification user = this.factory.getEntityByUserName(username,userToken.getRole());
        if(user == null)
            throw  new BusinessException(ExceptionInfo.USER_NOT_EXIST);
        return new SimpleAuthenticationInfo(
                user,
                user.getPassword(),
                ByteSource.Util.bytes(user.getSalt()),
                getName()
        );
    }


    @PostConstruct
    public void initCredentialsMatcher() {
        setCredentialsMatcher(new UserCredentialsMatcher(getCacheManager()));
    }
}