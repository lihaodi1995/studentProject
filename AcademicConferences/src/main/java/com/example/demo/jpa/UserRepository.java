package com.example.demo.jpa;

import com.example.demo.model.entity.UserEntity;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/6/30 16:59
 **/
public interface UserRepository extends JpaRepository<UserEntity,Long>{
    UserEntity findByEmailEquals(String email);

    boolean existsByNickNameEquals(String nickname);
}
