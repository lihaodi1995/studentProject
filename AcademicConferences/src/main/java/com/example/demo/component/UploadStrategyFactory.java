package com.example.demo.component;

import com.example.demo.model.base.ResourceType;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

/**
 * @Author : 叶明林
 * @Description: 成果上传service工厂
 * @Date created at 2018/6/1 14:38
 **/
@Component
public class UploadStrategyFactory implements InitializingBean, ApplicationContextAware {
    private ApplicationContext applicationContext;

    private Map<ResourceType, UploadStrategy> serviceImpMap = new HashMap<>();

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        this.applicationContext = applicationContext;
    }

    @Override
    public void afterPropertiesSet(){
        Map<String, UploadStrategy> beanMap = applicationContext.getBeansOfType(UploadStrategy.class);
        for (UploadStrategy strategy : beanMap.values())
        {
            ResourceType resourceType = strategy.getSupportResourceType();
            if(resourceType!=null)
                serviceImpMap.put(resourceType,strategy);
        }
    }

    public UploadStrategy getUploadStrategy(ResourceType type) {
        return serviceImpMap.get(type);
    }
}
