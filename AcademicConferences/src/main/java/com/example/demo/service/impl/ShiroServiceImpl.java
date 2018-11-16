package com.example.demo.service.impl;

import com.example.demo.exception.BusinessException;
import com.example.demo.jpa.AdminRepository;
import com.example.demo.jpa.OrganizationRepository;
import com.example.demo.jpa.UserRepository;
import com.example.demo.model.base.Identification;
import com.example.demo.model.base.Role;
import com.example.demo.model.entity.AdminEntity;
import com.example.demo.model.entity.UserEntity;
import com.example.demo.security.PasswordEncryption;
import com.example.demo.security.UserToken;
import com.example.demo.service.AuthentificationService;
import com.example.demo.utils.IdentificationFactory;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.subject.Subject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import static com.example.demo.exception.ExceptionInfo.*;


/**
 * @Author : 叶明林
 * @Description: 基于shiro框架的认证实现类
 * @Date created at 2018/5/16 16:19
 **/
@Service
public class ShiroServiceImpl implements AuthentificationService{

    private final UserRepository userRepository;

    private final OrganizationRepository organizationRepository;

    private final AdminRepository adminRepository;

    private IdentificationFactory factory = IdentificationFactory.getInstance();

    @Autowired
    public ShiroServiceImpl(UserRepository userRepository, OrganizationRepository organizationRepository, AdminRepository adminRepository) {
        this.userRepository = userRepository;
        this.organizationRepository = organizationRepository;
        this.adminRepository = adminRepository;
    }

    @Override
    public void login(String userName, String password,String role) {
        Subject currentUser = SecurityUtils.getSubject();
        if(currentUser.isAuthenticated()&&getNameOfCurrentUser().equals(userName))
            return;
        UserToken token = new UserToken(userName,password,role);
        currentUser.login(token);
    }

    @Override
    public Identification register(String userName, String password,String role) {
        if(userName == null || userName.isEmpty()||
                password == null||password.isEmpty()||
                 role == null || role.isEmpty())
            throw new BusinessException(PARAMS_ILLEGAL);

        switch (role)
        {
            case Role.ROLE_USER:
                if(userRepository.findByEmailEquals(userName) != null)
                    throw new BusinessException(USERNAME_EXISTED);
                UserEntity userToRegister =new UserEntity();
                userToRegister.setUserName(userName);
                userToRegister.setPassword(password);
                return userRepository.save(userToRegister);
            case Role.ROLE_ORGANIZER:
                if(adminRepository.findByUserNameEquals(userName) != null)
                    throw new BusinessException(USERNAME_EXISTED);
                AdminEntity adminEntityToRegister =new AdminEntity();
                adminEntityToRegister.setUserName(userName);
                adminEntityToRegister.setPassword(password);
                return this.adminRepository.save(adminEntityToRegister);
            default:
                throw new BusinessException(PARAMS_ILLEGAL);
        }

    }

    @Override
    public void logout() {
        Subject currentUser = SecurityUtils.getSubject();
        currentUser.logout();
    }

    @Override
    public Identification getCurrentUser() {
        return   (Identification)SecurityUtils.getSubject().getPrincipal();
    }

    @Override
    public void changeUserName(String newUserName) {
        Identification currentUser = this.getCurrentUser();
        if(currentUser.getUserName().equals(newUserName))
            return ;
        synchronized (newUserName.intern())
        {
            if(this.factory.checkUserNameExisted(newUserName,currentUser.getRole()))
                throw new BusinessException(USERNAME_EXISTED);
            currentUser.setUserName(newUserName);
            factory.saveEntity(currentUser);
        }
        Identification user = (Identification)SecurityUtils.getSubject().getPrincipal();
        user.setUserName(newUserName);
    }

    @Override
    public void changePassword(String userName,String role, String originalPassword, String newPassword) {
        Identification user = factory.getEntityByUserName(userName,role);
        if(user == null)
            throw new BusinessException(USER_NOT_EXIST);

        String pwd = PasswordEncryption.encryptPassword(originalPassword,user.getSalt());
        if(!user.getPassword().equals(pwd))
            throw new BusinessException(PWD_NOT_MATHCHED);

        user.setPassword(newPassword);
        this.factory.saveEntity(user);
        this.logout();
    }

    private String getNameOfCurrentUser() {
        return getCurrentUser().getUserName();
    }

    @Override
    public boolean currentUserIsAuthenticated() {
        return SecurityUtils.getSubject().isAuthenticated();
    }

}
