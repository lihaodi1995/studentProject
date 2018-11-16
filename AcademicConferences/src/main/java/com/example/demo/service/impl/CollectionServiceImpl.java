package com.example.demo.service.impl;

import com.example.demo.component.SendingEmailJob;
import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import com.example.demo.jpa.*;
import com.example.demo.model.entity.*;
import com.example.demo.model.response.ConferenceListItem;
import com.example.demo.model.response.ListPage;
import com.example.demo.service.AuthentificationService;
import com.example.demo.service.CollectionService;
import com.example.demo.utils.PageFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

/**
 * @Author : 陈瀚清
 * @Description: 收藏相关操作
 * @Date created at 2018/6/7
 **/
@Service
public class CollectionServiceImpl implements CollectionService {

    private final UserRepository userRepository;
    private final AuthentificationService authentificationService;
    private final CollectionClassificationRepository collectionClassificationRepository;
    private final ConferenceRepository conferenceRepository;

    public CollectionServiceImpl(UserRepository userRepository, AuthentificationService authentificationService, CollectionClassificationRepository collectionClassificationRepository, ConferenceRepository conferenceRepository) {
        this.userRepository = userRepository;
        this.authentificationService = authentificationService;
        this.collectionClassificationRepository = collectionClassificationRepository;
        this.conferenceRepository = conferenceRepository;
    }

    @Override
    public void addCollection(int conferenceId) {
        UserEntity user=(UserEntity) authentificationService.getCurrentUser();
        Optional<CollectionClassificationEntity> collection=this.collectionClassificationRepository.
                findByOwner_IdAndName(user.getId(),null);
        Optional<ConferenceEntity> conference=this.conferenceRepository.findById(conferenceId);
        if(!conference.isPresent()) throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        ConferenceEntity conferenceEntity=conference.get();
        if(collection.isPresent()){
            CollectionClassificationEntity entity=collection.get();
            Set<ConferenceEntity> set=entity.getConferences();
            set.add(conferenceEntity);
            SendingEmailJob.changeMap(user.getEmail(),set);//更新map
            this.collectionClassificationRepository.save(entity);
        }
        else{
            CollectionClassificationEntity newCollection=getCollectionEntity(null,user);
            Set<ConferenceEntity> set=new HashSet<>();
            set.add(conferenceEntity);
            newCollection.setConferences(set);
            this.collectionClassificationRepository.save(newCollection);
        }
    }

    @Transactional
    @Override
    public void deleteCollection(int conferenceId) {
        UserEntity user=(UserEntity) this.authentificationService.getCurrentUser();
        Optional<CollectionClassificationEntity> opt=
                this.collectionClassificationRepository.findByOwner_IdAndName(user.getId(),null);
        Optional<ConferenceEntity> conference=this.conferenceRepository.findById(conferenceId);
        if(!conference.isPresent()) throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        if(opt.isPresent()){
            CollectionClassificationEntity entity=opt.get();
            Set<ConferenceEntity> set=entity.getConferences();
            set.remove(conference.get());
            SendingEmailJob.changeMap(user.getEmail(),set);//更新map
            this.collectionClassificationRepository.save(entity);
        }
        else{
            throw new BusinessException(ExceptionInfo.COLLECTION_NOT_FOUND);
        }
    }


    @Transactional
    @Override
    public void clearCollection() {
        UserEntity user=(UserEntity) this.authentificationService.getCurrentUser();
        this.collectionClassificationRepository.deleteAllByOwner_Id(user.getId());
        SendingEmailJob.changeMap(user.getEmail(),null);//更新map
    }

    @Override
    public ListPage<ConferenceListItem> getCollection(int pageNumber) {
        UserEntity user=(UserEntity) this.authentificationService.getCurrentUser();
        Optional<CollectionClassificationEntity> opt=
                this.collectionClassificationRepository.findByOwner_IdAndName(user.getId(),null);
        pageNumber=PageFactory.checkPageNumber(pageNumber);
        if(opt.isPresent()){
            CollectionClassificationEntity entity=opt.get();
            Set<ConferenceEntity> set=entity.getConferences();
            Iterator<ConferenceEntity> iter=set.iterator();
            List<ConferenceListItem> list=new ArrayList<>();
            while(iter.hasNext()){
                ConferenceEntity conferenceEntity=iter.next();
                ConferenceListItem item=new ConferenceListItem(conferenceEntity);
                list.add(item);
            }
            return new ListPage<>(list,pageNumber,ConferenceListItem.PAGESIZE);
        }
        else{
            return new ListPage<>(null,pageNumber,ConferenceListItem.PAGESIZE);
        }
    }


    @Override
    public boolean haveCollected(int conferenceId){
        UserEntity user=(UserEntity) this.authentificationService.getCurrentUser();
        Optional<CollectionClassificationEntity> collection=this.collectionClassificationRepository.
                findByOwner_IdAndConferences_Id(user.getId(),conferenceId);
        if(collection.isPresent()){
            return true;
        }
        return false;
    }

    private CollectionClassificationEntity getCollectionEntity(String collectionName,UserEntity user){
        CollectionClassificationEntity collection=new CollectionClassificationEntity();
        collection.setName(collectionName);
        collection.setOwner(user);
        return collection;
    }
}
