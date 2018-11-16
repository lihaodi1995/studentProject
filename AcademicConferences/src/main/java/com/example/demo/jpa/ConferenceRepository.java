package com.example.demo.jpa;

import com.example.demo.model.entity.ConferenceEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface ConferenceRepository extends JpaRepository<ConferenceEntity,Integer>,JpaSpecificationExecutor<ConferenceEntity> {
    Page<ConferenceEntity> findAll(Specification<ConferenceEntity> spec, Pageable pageRequest);
}
