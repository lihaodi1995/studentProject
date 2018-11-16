package com.example.demo.controller;

import com.example.demo.model.base.Role;
import com.example.demo.model.entity.RegisterFormEntity;
import com.example.demo.model.request.AdminHandleRegisterReq;
import com.example.demo.model.response.ListPage;
import com.example.demo.model.response.RegisterFormInfo;
import com.example.demo.service.AdministratorService;
import com.example.demo.service.AuthentificationService;
import com.example.demo.service.OrganizationRegisterFormService;
import com.example.demo.utils.Node;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiOperation;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;


/**
 * @Author : 叶明林
 * @Description: 管理员模块
 * @Date created at 2018/6/30 21:56
 **/
@RequestMapping(value = "/api/admin")
@ApiModel(value = "管理员模块")
@RestController
public class AdministratorController {
    private final AdministratorService administratorService;
    private final AuthentificationService authentificationService;
    private final OrganizationRegisterFormService organizationRegisterFormService;

    @Autowired
    public AdministratorController(AdministratorService administratorService, AuthentificationService authentificationService, OrganizationRegisterFormService organizationRegisterFormService) {
        this.administratorService = administratorService;
        this.authentificationService = authentificationService;
        this.organizationRegisterFormService = organizationRegisterFormService;
    }

    @GetMapping(value = "/registration/list")
    @RequiresRoles(value = Role.ROLE_ADMIN)
    public Node<String,ListPage<RegisterFormInfo>> getRegisterForms(@RequestParam(required = false) Integer page,
                                      @RequestParam(required = false) Integer size,@RequestParam(required = false) String status)
    {
        if(page!=null&&page<0||size!=null&&size<0)
        {
            page = null;
            size = null;
        }

        RegisterFormEntity.HandleStatus status1 ;

        if(!RegisterFormEntity.HandleStatus.contains(status))
            status1 = null;
        else
            status1 = RegisterFormEntity.HandleStatus.valueOf(status);
        return new Node<>("data",this.administratorService.getRegisterFormsByStatus(page,size,status1));
    }

    @GetMapping(value = "/registration/{registrationID}/detail")
    @ApiOperation(value = "管理员查询特定ID的注册表单")
    @RequiresRoles(value = Role.ROLE_ADMIN)
    public Node<String,RegisterFormInfo> getRegisterForm(@PathVariable Integer registrationID)
    {
        RegisterFormEntity registerFormEntity = this.organizationRegisterFormService.getRegisterFormDetailsByFormId(registrationID);
        this.organizationRegisterFormService.changeStatusOfRegisterForm(registrationID, RegisterFormEntity.HandleStatus.Handling);
        return new Node<>("data",new RegisterFormInfo(registerFormEntity));
    }

    @PostMapping("/registration/{registrationID}/handle")
    @ApiOperation(value = "管理员处理机构注册表单")
    @RequiresRoles(value = Role.ROLE_ADMIN)
    public void handleRegistrationForm(@PathVariable Integer registrationID , @RequestBody AdminHandleRegisterReq params)
    {
        this.administratorService.handleRegistrationForm(registrationID,
                params.isOrganizationStatus(),params.getResult());
    }

}
