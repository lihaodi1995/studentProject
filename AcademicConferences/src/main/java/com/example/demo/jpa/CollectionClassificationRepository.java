package com.example.demo.jpa;

import com.example.demo.model.entity.CollectionClassificationEntity;
import com.example.demo.model.entity.ConferenceEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

import java.util.List;
import java.util.Optional;

/**
 * @Author : 陈瀚清
 * @Date created at 2018/6/7
 **/
public interface CollectionClassificationRepository extends JpaRepository<CollectionClassificationEntity,Integer> {
    Optional<CollectionClassificationEntity> findByOwner_IdAndName(Long ownerId, String name);
    void deleteAllByOwner_Id(Long ownerId);
    Optional<CollectionClassificationEntity> findByOwner_IdAndConferences_Id(Long ownerId, int conferenceId);

    CollectionClassificationEntity findByConferencesContains(ConferenceEntity conferenceEntity);
}
