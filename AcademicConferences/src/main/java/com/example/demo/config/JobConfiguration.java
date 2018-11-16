package com.example.demo.config;

import com.example.demo.component.AutowireJobFactory;
import com.example.demo.component.SendingEmailJob;
import com.example.demo.jpa.CollectionClassificationRepository;
import com.example.demo.model.entity.CollectionClassificationEntity;
import com.example.demo.model.entity.ConferenceEntity;
import org.quartz.DateBuilder;
import org.quartz.JobDetail;
import org.quartz.Trigger;
import org.quartz.spi.JobFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.quartz.JobDetailFactoryBean;
import org.springframework.scheduling.quartz.SchedulerFactoryBean;
import org.springframework.scheduling.quartz.SimpleTriggerFactoryBean;

import java.util.*;

/**
 * @Author : 陈瀚清
 * @Description: job配置
 * @Date created at 2018/7/5
 **/
@Configuration
public class JobConfiguration {

    private final CollectionClassificationRepository repository;
    private Map<String,Set<ConferenceEntity>> map=new HashMap<>();

    public JobConfiguration(CollectionClassificationRepository repository) {
        this.repository = repository;
        addData();
    }

    @Bean
    public JobFactory jobFactory(ApplicationContext applicationContext){
        AutowireJobFactory jobFactory=new AutowireJobFactory();
        jobFactory.setApplicationContext(applicationContext);
        return jobFactory;
    }

    @Bean
    public SchedulerFactoryBean schedulerFactory(@Qualifier("jobFactory")JobFactory jobFactory,
                                                 @Qualifier("simpleTriggerFactory") Trigger simpleJobTrigger){
        SchedulerFactoryBean factory = new SchedulerFactoryBean();
        factory.setJobFactory(jobFactory);
        factory.setTriggers(simpleJobTrigger);
        return factory;
    }

    @Bean
    public SimpleTriggerFactoryBean simpleTriggerFactory(@Qualifier("jobDetailFactory") JobDetail jobDetail){
        SimpleTriggerFactoryBean bean=new SimpleTriggerFactoryBean();
        //Date date=DateBuilder.nextGivenMinuteDate(null,5);//接下来整5分钟启动
        //bean.setStartTime(date);
        bean.setJobDetail(jobDetail);
        bean.setRepeatInterval(10*60*1000);
        return bean;
    }

    @Bean
    public JobDetailFactoryBean jobDetailFactory(){
        JobDetailFactoryBean jobDetailFactoryBean=new JobDetailFactoryBean();
        jobDetailFactoryBean.setJobClass(SendingEmailJob.class);
        jobDetailFactoryBean.setName("email_job");
        jobDetailFactoryBean.setGroup("如来佛组");
        jobDetailFactoryBean.setJobDataAsMap(map);
        return jobDetailFactoryBean;
    }

    private void addData(){
        List<CollectionClassificationEntity> entityList=this.repository.findAll();
        if(entityList!=null){
            for(CollectionClassificationEntity entity:entityList){
                String email=entity.getOwner().getEmail();
                if(email==null||email.isEmpty()) continue;
                Set<ConferenceEntity> set=entity.getConferences();
                map.put(email,set);
            }
        }
    }
}
