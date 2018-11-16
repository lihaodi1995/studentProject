package com.example.demo.jpa;

import com.example.demo.model.entity.EntryFormEntity;
import com.example.demo.model.entity.UserEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * Created by 44910_000 on 2018/7/1.
 */
public interface EntryFormRepository extends JpaRepository<EntryFormEntity,Integer> {
    List<EntryFormEntity> findAllByUserEquals(UserEntity user);
}
