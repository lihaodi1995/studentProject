package com.example.demo.service;

import com.example.demo.model.base.ResourceType;
import com.example.demo.model.entity.AttachmentEntity;
import com.example.demo.model.entity.EntryFormEntity;
import com.example.demo.model.entity.PaperEntity;
import com.example.demo.model.entity.SuperParticipantEntity;
import com.example.demo.model.request.ConferenceChangeInfo;
import com.example.demo.model.entity.*;
import com.example.demo.model.request.ConferenceInfo;
import com.example.demo.model.request.OrganizationRegisterForm;
import com.example.demo.model.response.EntryFormInfo;
import com.example.demo.model.response.ListPage;
import com.example.demo.model.request.UserNameAndPassword;
import com.example.demo.model.response.PaperInfo;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Set;

public interface OrganizationService {
    /**
     * 提交单位注册相关资料
     * @param form 信息表单
     * @param evidence 证明附件
     */
    void handInRegistrationForm(OrganizationRegisterForm form, MultipartFile evidence);

    /**
     * 发布会议
     * @param organizationId 机构ID
     * @param conferenceInfo 会议信息
     * @param attachmentEntityList 论文模板
     */
    void conferencePost(Long organizationId, ConferenceInfo conferenceInfo,
                        List<AttachmentEntity> attachmentEntityList);

    List<AttachmentEntity> uploadResource(List<String>files, ResourceType type,
                                          Long organizationid);

    /**
     * 展示会议投稿情况
     * @param conferenceId 会议ID
     * @param page 页码
     * @return 投稿论文列表
     */
    ListPage<PaperInfo> getPaperList(Integer conferenceId, Integer page);

    /**
     * 录入评审结果
     * @param paperId 论文ID
     * @param judgeStatus 评审情况
     * @param opinion 评审意见
     */
    void setJudgeStatus(Integer paperId, PaperEntity.JudgeStatus judgeStatus, String opinion);

    /**
     * 修改会议信息
     * @param id 会议id
     * @param conferenceInfo 要修改的会议信息
     */
    void changeConferenceInfo(int id,ConferenceChangeInfo conferenceInfo);

    /**
     * 查看会议报名注册者
     * @param conferenceId 会议Id
     * @param page 页码
     * @return 会议报名注册者列表
     */
    ListPage<SuperParticipantEntity> getParticipants(Integer conferenceId, Integer page);

    /**
     * 处理报名注册
     * @param entryId 报名表Id
     * @param handleStatus 处理状态
     */
    void participantHandle(Integer entryId, EntryFormEntity.HandleStatus handleStatus);

    /**
     * 查看会议报名注册信息
     * @param conferenceId 会议Id
     * @param page 页码
     * @return 会议报名表
     */
    ListPage<EntryFormInfo> getEntryList(Integer conferenceId, Integer page);

    /**
     * 机构获得机构管理员列表
     * @param organizationID 组织ID
     * @param page 页码
     * @return  机构管理员列表
     */

    ListPage<AdminEntity> getAccountByOrganizationIDandPage(long organizationID,int page);

    /**
     * 机构添加机构管理用户
     * @param  userNameAndPassword 用户名和密码
     */

    void addAdmin(UserNameAndPassword userNameAndPassword);

    /**
     * 机构修改机构管理用户
     * @param id 机构管理员id
     * @param  userNameAndPassword 用户名和密码
     */

    void setAdmin(long id,UserNameAndPassword userNameAndPassword);

    /**
     * 机构删除机构管理用户
     * @param id 机构管理员id
     */

    void deleteAdmin(long id);

    /**
     * 机构删除会议
     * @param conferenceId 会议ID
     */
    void deleteConference(Integer conferenceId);


    /**
     * 机构导出会议投稿情况
     * @param conferenceId 会议Id
     */
    ResponseEntity<FileSystemResource> getExcelOfConference(int conferenceId);
}
