package com.example.demo.controller;

import com.example.demo.component.SpringContextUtils;
import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import com.example.demo.model.base.Identification;
import com.example.demo.model.base.ResourceType;
import com.example.demo.model.base.Role;
import com.example.demo.model.entity.UserEntity;
import com.example.demo.model.request.*;
import com.example.demo.model.response.EntryFormInfo;
import com.example.demo.model.response.JudgeDetail;
import com.example.demo.model.response.RepostInfo;
import com.example.demo.service.AuthentificationService;
import com.example.demo.service.CollectionService;
import com.example.demo.service.UserService;
import com.example.demo.service.VisitorService;
import com.example.demo.utils.IdentificationFactory;
import com.example.demo.utils.Node;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiOperation;
import org.apache.shiro.authz.UnauthenticatedException;
import org.apache.shiro.authz.annotation.RequiresAuthentication;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import java.util.List;

/**
 * @Author : 陈瀚清
 * @Description: 游客功能
 * @Date created at 2018/6/30
 **/
@RestController
@RequestMapping("/api/user")
@ApiModel("用户模块")
public class UserController {
    private final VisitorService visitorService;
    private final UserService userService;
    private final AuthentificationService authentificationService;
    private final CollectionService collectionService;

    @Autowired
    public UserController(VisitorService visitorService, UserService userService, AuthentificationService authentificationService, CollectionService collectionService) {
        this.visitorService = visitorService;
        this.userService = userService;
        this.authentificationService = authentificationService;
        this.collectionService = collectionService;
    }

    @GetMapping("/search/{page}")
    @ApiOperation(value = "搜索会议")
    public Node<String,Object> searchConference(@RequestParam(required = false)String name,
                                                @RequestParam(required = false)Long startDDL,
                                                @RequestParam(required = false)Long endDDL,
                                                @RequestParam(required = false)Long startConfDate,
                                                @RequestParam(required = false)Long endConfDate,
                                                @RequestParam(required = false)Long organizationId,
                                                @PathVariable Integer page){
        if(page==null){
            throw new BusinessException(ExceptionInfo.PAGENUMBER_INVALID);
        }
        boolean emptyParam=name==null&&startDDL==null&&endDDL==null&&startConfDate==null
                &&endConfDate==null&&organizationId==null;
        boolean DDLInvalid=(startDDL!=null&&endDDL==null)||(startDDL==null&&endDDL!=null);
        boolean ConfDateInvalid=(startConfDate!=null&&endConfDate==null)||(startConfDate==null&&endConfDate!=null);
        if(emptyParam){
            name="";//全部返回
        }
        else if(DDLInvalid||ConfDateInvalid){
            throw new BusinessException(ExceptionInfo.PARAMS_ILLEGAL);
        }
        return new Node<>("data",
                this.visitorService.getConferenceList(name,startDDL,endDDL,startConfDate,endConfDate,organizationId,page));
    }

    @RequiresAuthentication
    @PostMapping("/conference/join/registration")
    @ApiOperation(value = "注册会议")
    public void handInConferenceRegistrationForm(@RequestBody UserConferenceRegistrationForm userConferenceRegistrationForm){
        int CID= userConferenceRegistrationForm.getConferenceID();
        JoinConferenceGroup joinConferenceGroup=userConferenceRegistrationForm.getJoinConferenceGroup();
        this.userService.handInConferenceRegistrationForm(CID,joinConferenceGroup);
    }

    @RequiresAuthentication
    @ApiOperation(value = "查看会议详情")
    @GetMapping("/conference/{id}")
    public Node<String,Object> getConference(@PathVariable Integer id){
        return new Node<>("data",
                this.userService.getConference(id));
    }

    @RequiresAuthentication
    @ApiOperation(value = "投稿")
    @PostMapping("/contribute/{conferenceId}")
    public void putContribution(@PathVariable Integer conferenceId, @RequestBody ContributionInfo contributionInfo){
        userService.contributePaper(conferenceId,contributionInfo);
    }

    @PostMapping("/session")
    @ApiOperation(value = "用户登录")
    public void login(@RequestBody UserNameAndPassword userInfo)
    {
        authentificationService.login(userInfo.getUserName(),userInfo.getPassword(),Role.ROLE_USER);
    }

    @PostMapping("/registration")
    @ApiOperation(value = "用户注册")
    public void register(@RequestBody UserRegisterInfo userInfo)
    {
        Identification identification = authentificationService.register(userInfo.getEmail(),userInfo.getPassword(),Role.ROLE_USER);
        UserEntity userEntity = (UserEntity) identification;
        if(userEntity!=null)
        {
            IdentificationFactory factory = IdentificationFactory.getInstance();
            factory.saveEntity(userEntity);
        }
    }

    @GetMapping("/session/info")
    @ApiOperation(value = "获取当前用户信息")
    public Node<String, Object> getCurrentUserInfo()
    {
        checkSessionExpired();
        Identification ans = this.authentificationService.getCurrentUser();
        Identification user ;
        if(ans == null)
        {
            user = new UserEntity();
            user.setRole(null);
        }
        else
            user = ans;
        return new Node<>("data",user);
    }

    @RequiresAuthentication
    @DeleteMapping("/session")
    @ApiOperation(value = "用户注销")
    public void logout()
    {
        this.authentificationService.logout();
    }

    @RequiresAuthentication
    @GetMapping("/getjudge")
    @ApiOperation(value = "查看评审结果")
    public Node<String, List<JudgeDetail>> getJudgeDetail(){
        return new Node<>("judgeDetail", this.userService.getJudgeDetail());
    }

    @RequiresAuthentication
    @PostMapping("/repostpaper/{paperId}")
    @ApiOperation(value = "上传修改稿")
    public void repostPaper(@PathVariable Integer paperId, @RequestBody RepostInfo repostInfo){
        ResourceType resourceType = ResourceType.valueOf("Paper");
        userService.repostPaper(paperId, resourceType, repostInfo);
    }

    @RequiresAuthentication
    @GetMapping("/collection_list/{pageNumber}")
    @ApiOperation(value = "查看收藏")
    public Node<String, Object> getCollection(@PathVariable Integer pageNumber){
        return new Node<>("data", this.collectionService.getCollection(pageNumber));
    }

    @RequiresAuthentication
    @GetMapping("/collection/{conferenceId}")
    @ApiOperation(value = "收藏某个会议")
    public void collection(@PathVariable Integer conferenceId){
        this.collectionService.addCollection(conferenceId);
    }

    @RequiresAuthentication
    @DeleteMapping("/undo_collection/{conferenceId}")
    @ApiOperation(value = "取消收藏某个会议")
    public void deleteCollection(@PathVariable Integer conferenceId){
        this.collectionService.deleteCollection(conferenceId);
    }

    @RequiresAuthentication
    @DeleteMapping("/clear_collection")
    @ApiOperation(value = "清空收藏")
    public void clearCollection(){
        this.collectionService.clearCollection();
    }

    @RequiresAuthentication
    @GetMapping("/check_collection/{conferenceId}")
    @ApiOperation(value = "检查是否收藏")
    public Node<String,Object> checkCollection(@PathVariable Integer conferenceId){
        return new Node<>("data",this.collectionService.haveCollected(conferenceId));
    }

    @PostMapping("/password/reset")
    @ApiOperation("修改当前用户的密码")
    @RequiresAuthentication
    public void changeCurrentUserPassword(@RequestBody PasswordAlteration params)
    {
        Identification identification = this.authentificationService.getCurrentUser();
        this.authentificationService.changePassword(identification.getUserName(),identification.getRole(),
                params.getOriginalPassword(),params.getNewPassword());
    }

    private void checkSessionExpired()
    {
        if(this.authentificationService.currentUserIsAuthenticated())
            return ;
        HttpServletRequest httpServletRequest = SpringContextUtils.getHttpServletRequest();
        Cookie[] cookies = httpServletRequest.getCookies();
        if(cookies !=null)
        {
            for(Cookie cookie:cookies)
                if(cookie.getName().equals("JSESSIONID"))
                    throw new UnauthenticatedException();
        }
    }

    @ApiOperation(value = "修改当前普通用户信息")
    @PostMapping(value = "/info/modify")
    @RequiresRoles(value = Role.ROLE_USER)
    public void modifyUserInfo(@RequestBody UserInfoModificationReq params)
    {
        this.userService.modifyUserInfo(params);
    }

    @ApiOperation(value = "查看报名信息")
    @GetMapping(value = "/getentry")
    @RequiresRoles(value = Role.ROLE_USER)
    public Node<String, List<EntryFormInfo>> getEntry(){
        return new Node<>("getEntry", userService.getEntry());
    }
}
