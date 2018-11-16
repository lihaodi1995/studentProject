package com.example.demo.service.impl;

import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import com.example.demo.jpa.ConferenceRepository;
import com.example.demo.model.entity.ConferenceEntity;
import com.example.demo.model.entity.PaperEntity;
import com.example.demo.model.response.ConferenceListItem;
import com.example.demo.model.response.ListPage;
import com.example.demo.service.VisitorService;
import com.example.demo.utils.PageFactory;
import org.apache.log4j.Logger;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;

import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import java.sql.Date;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

/**
 * @Author : 陈瀚清
 * @Description: 游客服务
 * @Date created at 2018/6/30
 **/
@Service
public class VisitorServiceImpl implements VisitorService {
    private final PageFactory<ConferenceListItem,ConferenceEntity> pageFactory=new PageFactory<>();
    private final ConferenceListItem conferenceListItem=new ConferenceListItem();
    private final ConferenceRepository conferenceRepository;


    public VisitorServiceImpl(ConferenceRepository conferenceRepository) {
        this.conferenceRepository = conferenceRepository;
    }

    @Override
    public ListPage<ConferenceListItem> getConferenceList(String name, Long startDDL, Long endDDL, Long startConf, Long endConf,Long organizationId,Integer page) {
        Timestamp sDDL=timestampToString(startDDL);
        Timestamp eDDL=timestampToString(endDDL);
        Timestamp sConf=timestampToString(startConf);
        Timestamp eConf=timestampToString(endConf);
        return conferenceList(name,sDDL,eDDL,sConf,eConf,organizationId,page);
    }

    private ListPage<ConferenceListItem> conferenceList(String name,Timestamp sDDL,Timestamp eDDL,Timestamp sConf,Timestamp eConf,Long organizationId,Integer page){
        page=PageFactory.checkPageNumber(page);//检查输入页号
        ListPage<ConferenceListItem> p;
        GetSpecification getSpec=new GetSpecification<ConferenceEntity>(name, sDDL, eDDL, sConf, eConf,organizationId);
        Specification<ConferenceEntity> spec=getSpec.getSpecName();
        Page<ConferenceEntity> list= this.conferenceRepository.findAll(spec,PageRequest.of(page,ConferenceListItem.PAGESIZE,
                new Sort(Sort.Direction.DESC,"setDate")));
        PageFactory.checkPageNumber(list);//检查结果页号
        p=pageFactory.getListPage(list,ConferenceListItem.PAGESIZE,conferenceListItem);
        return p;
    }

    public Timestamp timestampToString(Long str){
        if(str!=null){
            try{
                return new Timestamp(str);
            }catch (IllegalArgumentException e){
                throw new BusinessException(ExceptionInfo.PARAMS_ILLEGAL);
            }
        }
        else return null;
    }
}

//获得动态查询条件
class GetSpecification<T>{

    private String name;//名称
    private Timestamp startDDL;
    private Timestamp endDDL;
    private Timestamp startConf;
    private Timestamp endConf;
    private Long organizationId;

    private final Logger logger=Logger.getLogger(GetSpecification.class);
    private Specification<T> specName=new Specification<T>() {
        @Override
        public Predicate toPredicate(Root<T> root, CriteriaQuery<?> criteriaQuery, CriteriaBuilder criteriaBuilder) {
            List<Predicate> list=new ArrayList<>();

            if(name!=null){
                list.add(criteriaBuilder.like(root.get("name").as(String.class),'%'+name+'%'));
            }
            if(startDDL!=null&&endDDL!=null){
                Calendar a=Calendar.getInstance();
                a.setTimeInMillis(startDDL.getTime());
                Calendar b=Calendar.getInstance();
                b.setTimeInMillis(endDDL.getTime());
                logger.info(a.toString());
                logger.info(b.toString());
                list.add(criteriaBuilder.between(root.get("ddlDate").as(Timestamp.class),startDDL,endDDL));
            }
            if(startConf!=null&&endConf!=null){
                list.add(criteriaBuilder.between(root.get("confBeginDate").as(Timestamp.class),startConf,endConf));
            }
            if(organizationId!=null){
                list.add(criteriaBuilder.equal(root.get("organization").get("id").as(Long.class),organizationId));
            }
            Predicate[] namePredicates=new Predicate[list.size()];
            Predicate namePredicate = criteriaBuilder.and(list.toArray(namePredicates));
            return namePredicate;
        }
    };

    public GetSpecification(String name, Timestamp startDDL, Timestamp endDDL, Timestamp startConf, Timestamp endConf,Long organizationId) {
        this.name = name;
        this.startDDL = startDDL;
        this.endDDL = endDDL;
        this.startConf = startConf;
        this.endConf = endConf;
        this.organizationId=organizationId;
    }

    public Specification<T> getSpecName() {
        return specName;
    }

    public void setSpec(Specification<T> specName) {
        this.specName = specName;
    }
}
