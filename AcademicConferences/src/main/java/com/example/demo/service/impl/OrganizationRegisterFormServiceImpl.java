package com.example.demo.service.impl;

import com.example.demo.jpa.RegisterFormRepository;
import com.example.demo.model.entity.RegisterFormEntity;
import com.example.demo.service.OrganizationRegisterFormService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.Optional;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/1 22:13
 **/
@Service
public class OrganizationRegisterFormServiceImpl implements OrganizationRegisterFormService{
    private final RegisterFormRepository registerFormRepository;

    @Autowired
    public OrganizationRegisterFormServiceImpl(RegisterFormRepository registerFormRepository) {
        this.registerFormRepository = registerFormRepository;
    }

    @Override
    public Page<RegisterFormEntity> getRegisterFormsByStatus(Integer index, Integer size, RegisterFormEntity.HandleStatus status) {
        if(index == null)
            index = 0;
        if(size == null)
            size = 10;
        return this.registerFormRepository.findByHandleStatusEquals(status, PageRequest.of(index,size));
    }

    @Override
    public RegisterFormEntity getRegisterFormDetailsByFormId(Integer formId) {
        Optional<RegisterFormEntity> optional = this.registerFormRepository.findById(formId);
        return optional.orElse(null);
    }

    @Override
    public boolean changeStatusOfRegisterForm(Integer formId, RegisterFormEntity.HandleStatus newStatus) {
        Optional<RegisterFormEntity> optional = this.registerFormRepository.findById(formId);
        if(!optional.isPresent())
            return false;
        RegisterFormEntity registerForm = optional.get();
        if(!checkNewStatusLegal(registerForm.getHandleStatus(),newStatus))
            return false;
        registerForm.setHandleStatus(newStatus);
        this.registerFormRepository.save(registerForm);
        return true;
    }

    @Override
    public boolean setHandleResultOfRegisterForm(Integer formId,String registerResult) {
        Optional<RegisterFormEntity> optional = this.registerFormRepository.findById(formId);
        if(!optional.isPresent())
            return false;
        RegisterFormEntity registerForm = optional.get();
        registerForm.setRegisterResult(registerResult);
        this.registerFormRepository.save(registerForm);
        return true;
    }

    private boolean checkNewStatusLegal(RegisterFormEntity.HandleStatus oldStatus ,RegisterFormEntity.HandleStatus newStatus)
    {
        return oldStatus.getPriority()<newStatus.getPriority();
    }
}
