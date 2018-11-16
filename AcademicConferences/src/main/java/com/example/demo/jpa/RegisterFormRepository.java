package com.example.demo.jpa;

import com.example.demo.model.entity.RegisterFormEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/6/30 19:49
 **/
public interface RegisterFormRepository extends JpaRepository<RegisterFormEntity,Integer>{
    Page<RegisterFormEntity> findByHandleStatusEquals(RegisterFormEntity.HandleStatus status, Pageable pageable);

    List<RegisterFormEntity> findByHandleStatusEquals(RegisterFormEntity.HandleStatus status);
}
