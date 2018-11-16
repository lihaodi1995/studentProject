package com.example.demo.jpa;

import com.example.demo.model.entity.PaperEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface PaperRepository extends JpaRepository<PaperEntity,Integer>, JpaSpecificationExecutor<PaperEntity> {
}
