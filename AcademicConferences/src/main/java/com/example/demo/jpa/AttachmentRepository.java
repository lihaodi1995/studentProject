package com.example.demo.jpa;

import com.example.demo.model.entity.AttachmentEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AttachmentRepository extends JpaRepository<AttachmentEntity,Integer> {
}
