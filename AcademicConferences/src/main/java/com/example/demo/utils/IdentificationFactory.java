package com.example.demo.utils;

import com.example.demo.component.SpringContextUtils;
import com.example.demo.jpa.AdminRepository;
import com.example.demo.jpa.OrganizationRepository;
import com.example.demo.jpa.UserRepository;
import com.example.demo.model.base.Identification;
import com.example.demo.model.base.Role;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * @Author : 叶明林
 * @Description: 处理用户和单位用户的工厂
 * @Date created at 2018/6/30 16:33
 **/
public class IdentificationFactory {
    private static IdentificationFactory factory = new IdentificationFactory();
    public static IdentificationFactory getInstance()
    {
        return IdentificationFactory.factory;
    }

    public JpaRepository getRepositoryByRole(String role)
    {
        switch (role)
        {
            case Role.ROLE_ORGANIZER:
                return SpringContextUtils.getBean(OrganizationRepository.class);
            case Role.ROLE_USER:
            case Role.ROLE_ADMIN:
                return SpringContextUtils.getBean(UserRepository.class);
            default:
                return null;
        }
    }
    public Identification getEntityByUserName(String userName,String role)
    {
        switch (role)
        {
            case Role.ROLE_ORGANIZER:
                AdminRepository jpaRepository = SpringContextUtils.getBean(AdminRepository.class);
                return jpaRepository.findByUserNameEquals(userName);
            case Role.ROLE_USER:
            case Role.ROLE_ADMIN:
                UserRepository jpaRepository1 = SpringContextUtils.getBean(UserRepository.class);
                return jpaRepository1.findByEmailEquals(userName);
            default:
                return null;
        }
    }
    public Identification saveEntity(Identification entity)
    {
        JpaRepository jpaRepository = this.getRepositoryByRole(entity.getRole());
        return (Identification)jpaRepository.save(entity);
    }

    public boolean checkUserNameExisted(String name,String role)
    {
        return this.getEntityByUserName(name, role) != null;
    }
}
