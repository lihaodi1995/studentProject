package com.example.demo.service.impl;

import com.example.demo.component.EmailsUtil;
import com.example.demo.component.SendingEmailJob;
import com.example.demo.exception.BusinessException;
import com.example.demo.jpa.OrganizationRepository;
import com.example.demo.jpa.RegisterFormRepository;
import com.example.demo.model.base.Identification;
import com.example.demo.model.base.Role;
import com.example.demo.model.entity.AdminEntity;
import com.example.demo.model.entity.OrganizationEntity;
import com.example.demo.model.entity.RegisterFormEntity;
import com.example.demo.model.response.ListPage;
import com.example.demo.model.response.RegisterFormInfo;
import com.example.demo.security.PasswordEncryption;
import com.example.demo.service.AdministratorService;
import com.example.demo.service.AuthentificationService;
import com.example.demo.service.OrganizationRegisterFormService;
import com.example.demo.utils.IdentificationFactory;
import com.sun.mail.smtp.SMTPAddressFailedException;
import com.sun.mail.util.MailConnectException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.mail.MailAuthenticationException;
import org.springframework.mail.MailSendException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.mail.SendFailedException;
import java.util.*;
import java.util.concurrent.Future;

import static com.example.demo.exception.ExceptionInfo.*;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/6/30 21:06
 **/
@Service
public class AdministratorServiceImpl implements AdministratorService{

    private final OrganizationRegisterFormService organizationRegisterFormService;

    private final AuthentificationService authentificationService;

    private final EmailsUtil emailsUtil;

    private final OrganizationRepository organizationRepository;

    private final IdentificationFactory factory = IdentificationFactory.getInstance();

    private final RegisterFormRepository registerFormRepository;

    @Autowired
    public AdministratorServiceImpl(OrganizationRegisterFormService organizationRegisterFormService, AuthentificationService authentificationService, EmailsUtil emailsUtil, OrganizationRepository organizationRepository, RegisterFormRepository registerFormRepository) {
        this.organizationRegisterFormService = organizationRegisterFormService;
        this.authentificationService = authentificationService;
        this.emailsUtil = emailsUtil;
        this.organizationRepository = organizationRepository;
        this.registerFormRepository = registerFormRepository;
    }

    @Override
    public ListPage<RegisterFormInfo> getRegisterFormsByStatus(Integer index, Integer size, RegisterFormEntity.HandleStatus status) {
        if(index == null|| size ==null)
        {
            List<RegisterFormEntity> data ;
            if(status == null)
                data= this.registerFormRepository.findAll();
            else
                data = this.registerFormRepository.findByHandleStatusEquals(status);
            List<RegisterFormInfo> list = new ArrayList<>();
            for(RegisterFormEntity x:data)
                list.add(new RegisterFormInfo(x));
            ListPage<RegisterFormInfo> ans = new ListPage<>(list.size());
            ans.setItems(list);
            ans.setNowPage(0);
            ans.setPageSize(list.size());
            ans.setTotalElement(list.size());
            ans.setTotalPage(1);
            return ans;
        }
        ListPage<RegisterFormInfo> ans = new ListPage<>(size);
        Page<RegisterFormEntity> data = this.organizationRegisterFormService.getRegisterFormsByStatus(index,size,status);
        List<RegisterFormInfo> list = new ArrayList<>(data.getSize());
        for(RegisterFormEntity x:data)
            list.add(new RegisterFormInfo(x));
        ans.setItems(list);
        ans.setNowPage(index);
        ans.setPageSize(size);
        ans.setTotalElement(data.getTotalElements());
        ans.setTotalPage(data.getTotalPages());
        return ans;
    }

    @Override
    @Transactional
    public void handleRegistrationForm(Integer registrationID, boolean organizationStatus, String result) {
        RegisterFormEntity.HandleStatus newStatus = organizationStatus?RegisterFormEntity.HandleStatus.Accepted:
                RegisterFormEntity.HandleStatus.Refuse;

        Optional<RegisterFormEntity> optional = this.registerFormRepository.findById(registrationID);
        if(!optional.isPresent())
            throw new BusinessException(REGISTRATION_FORM_NOT_FOUND);
        if(!this.organizationRegisterFormService.changeStatusOfRegisterForm(registrationID,newStatus))
            throw new BusinessException(REGISTRATION_STATUS_CHANGE_ILLEGAL);

        if(newStatus .equals(RegisterFormEntity.HandleStatus.Accepted))
        {
            //更改注册表状态
            RegisterFormEntity formEntity = this.organizationRegisterFormService.getRegisterFormDetailsByFormId(registrationID);
            this.organizationRegisterFormService.setHandleResultOfRegisterForm(registrationID,result);
            //注册root管理员
            String pwd = PasswordEncryption.generateSalt();
            Identification identification = this.authentificationService.register(
                    formEntity.getMail(), pwd, Role.ROLE_ORGANIZER
            );
            //初始化机构实体并分配root管理员
            OrganizationEntity organization = this.initOrganization(formEntity.getOrganizationName());
            AdminEntity admin = (AdminEntity)identification;
            admin.setRoot(true);
            admin.setOrganization(organization);
            this.factory.saveEntity(admin);
            //发送邮件
            final String email = formEntity.getMail();
            if(email!=null&&!email.isEmpty())
            {
                final String content = "用户名:"+identification.getUserName()+" 密码:"+pwd;
                this.sendEmail(formEntity.getMail(),content);
            }
        }
    }


    private OrganizationEntity initOrganization(String organizationName)
    {
        OrganizationEntity organizationEntity =new OrganizationEntity();
        organizationEntity.setName(organizationName);
        return this.organizationRepository.save(organizationEntity);
    }

    private Future<String> sendEmail(String emailUrl,String content)
    {
        if(emailUrl == null)
            throw new BusinessException(EMAIL_NULL);
        return this.emailsUtil.sendEmail(this.emailsUtil.generateMessage(emailUrl,"注册成功",content));
    }
}
