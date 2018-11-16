package com.example.demo.controller;

import com.example.demo.exception.BusinessException;
import com.example.demo.model.base.ResourceType;
import com.example.demo.model.base.Role;
import com.example.demo.model.entity.*;
import com.example.demo.model.request.AllConferenceInfo;
import com.example.demo.model.request.ConferenceChangeInfo;
import com.example.demo.model.request.OrganizationRegisterForm;
import com.example.demo.model.request.UserNameAndPassword;
import com.example.demo.model.response.EntryFormInfo;
import com.example.demo.model.response.ListPage;
import com.example.demo.model.response.PaperInfo;
import com.example.demo.service.AuthentificationService;
import com.example.demo.service.OrganizationService;
import com.example.demo.utils.FileTransform;
import com.example.demo.utils.Node;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import io.swagger.annotations.ApiOperation;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

import static com.example.demo.exception.ExceptionInfo.WRONG_JUDGESTATUS;

@RestController
@RequestMapping(value = "/api/organization")
@ApiModel(value = "组织机构模块")
public class OrganizationController {
    private final OrganizationService organizationService;
    private final AuthentificationService authentificationService;

    @Autowired
    public OrganizationController(OrganizationService organizationService, AuthentificationService authentificationService){
        this.organizationService = organizationService;
        this.authentificationService = authentificationService;
    }

    @PostMapping("/post/{organizationId}")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiOperation(value = "机构发布会议")
    public void conferencePost(@PathVariable Long organizationId, @RequestBody AllConferenceInfo conferenceInfo){
        ResourceType resourceType = ResourceType.valueOf("Template");
        List<AttachmentEntity> attachmentEntityList;
        if(conferenceInfo.getFiles() == null)
            attachmentEntityList = null;
        else
            attachmentEntityList = organizationService.uploadResource(conferenceInfo.getFiles(), resourceType, organizationId);
        organizationService.conferencePost(organizationId, conferenceInfo, attachmentEntityList);
    }

    @GetMapping("/{conferenceId}/paperlist/{page}")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiOperation(value = "展示会议投稿情况")
    public Node<String, ListPage<PaperInfo>> getPaperList(@PathVariable Integer conferenceId, @PathVariable Integer page){
        return new Node<>("paperList", organizationService.getPaperList(conferenceId, page));
    }

    @PostMapping(value = "/registration")
    @ApiOperation(value = "提交机构注册信息")
    public void organizationRegistration(@RequestBody OrganizationRegisterForm form )
    {
        MultipartFile file = FileTransform.Base64ToMultipartFile(form.getFile());
        this.organizationService.handInRegistrationForm(form,file);
    }

    @GetMapping("/setjudge/{paperId}")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiModelProperty("机构录入评审结果")
    public void setJudgeStatus(@PathVariable Integer paperId, @RequestParam int judgeStatusInt,
                               @RequestParam String opinion){
        PaperEntity.JudgeStatus judgeStatus;
        switch(judgeStatusInt){
            case 0:
                judgeStatus = PaperEntity.JudgeStatus.Not_qualified;
                break;
            case 1:
                judgeStatus = PaperEntity.JudgeStatus.Pending;
                break;
            case 2:
                judgeStatus = PaperEntity.JudgeStatus.Qualified;
                break;
            case 3:
                judgeStatus = PaperEntity.JudgeStatus.Qualified_after_modified;
                break;
            default:
                throw new BusinessException(WRONG_JUDGESTATUS);
        }
        organizationService.setJudgeStatus(paperId, judgeStatus, opinion);
    }

    @PostMapping("/session")
    @ApiOperation(value = "机构登陆")
    public void login(@RequestBody UserNameAndPassword userInfo)
    {
        authentificationService.login(userInfo.getUserName(),userInfo.getPassword(),Role.ROLE_ORGANIZER);
    }


    @PostMapping("/change_conference/{conferenceId}")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiModelProperty("机构更新会议信息")
    public void setJudgeStatus(@PathVariable Integer conferenceId, @RequestBody ConferenceChangeInfo conferenceInfo){
        organizationService.changeConferenceInfo(conferenceId,conferenceInfo);
    }

    @DeleteMapping("/conference")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiModelProperty("机构删除会议")
    public void deleteConference(@RequestParam int conference_id){
        organizationService.deleteConference(conference_id);
    }

    @GetMapping("/participants/{conferenceId}/{page}")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiOperation(value = "机构查看会议报名注册者")
    public Node<String, ListPage<SuperParticipantEntity>> getParticipants(@PathVariable Integer conferenceId, @PathVariable Integer page){
        return new Node<>("participants", organizationService.getParticipants(conferenceId, page));
    }

    @PostMapping("/parthandle/{entryId}")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiOperation(value = "机构处理报名注册")
    public void participantHandle(@PathVariable Integer entryId, @RequestParam String handleStatusStr){
        EntryFormEntity.HandleStatus handleStatus = EntryFormEntity.HandleStatus.valueOf(handleStatusStr);
        organizationService.participantHandle(entryId, handleStatus);
    }

    @GetMapping("/entrylist/{conferenceId}/{page}")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiOperation(value = "机构查看会议报名注册信息")
    public Node<String, ListPage<EntryFormInfo>> getEntryList(@PathVariable(value = "conferenceId") Integer conferenceId,
                                                              @PathVariable(value = "page") Integer page){
        return new Node<>("entryList", organizationService.getEntryList(conferenceId, page));
    }

    @GetMapping("/accountList/{organizationID}/{page}")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiModelProperty("查看机构下辖机构管理账号列表")
    public Node<String,ListPage<AdminEntity>> getAccountByOrganizationName(@PathVariable Integer organizationID,@PathVariable Integer page){
        return new Node<>("adminList",organizationService.getAccountByOrganizationIDandPage(organizationID,page));
    }

    @PostMapping("/account/add")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiModelProperty("配置机构管理账号")
    public void addAdmin(@RequestBody UserNameAndPassword userNameAndPassword){
        this.organizationService.addAdmin(userNameAndPassword);
    }

    @PostMapping("/account/manage")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiModelProperty("修改机构管理账号")
    public void manageAdmin(@RequestParam long id,@RequestBody UserNameAndPassword userNameAndPassword){
        this.organizationService.setAdmin(id,userNameAndPassword);
    }

    @PostMapping("/account/delete")
    @RequiresRoles(value = {Role.ROLE_ORGANIZER})
    @ApiModelProperty("删除机构管理账号")
    public void deleteAdmin(@RequestParam long id){
        this.organizationService.deleteAdmin(id);
    }


}