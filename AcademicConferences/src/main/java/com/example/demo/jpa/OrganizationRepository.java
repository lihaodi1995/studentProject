package com.example.demo.jpa;

import com.example.demo.model.entity.OrganizationEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface OrganizationRepository extends JpaRepository<OrganizationEntity,Long>,JpaSpecificationExecutor<OrganizationEntity> {
}
