package com.example.demo.jpa;

import com.example.demo.model.entity.AdminEntity;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/4 16:26
 **/
public interface AdminRepository extends JpaRepository<AdminEntity,Long>{
    AdminEntity findByUserNameEquals(String userName);
}
