package com.example.demo.service;

import com.example.demo.model.base.ResourceType;
import com.example.demo.model.request.ContributionInfo;
import com.example.demo.model.request.IModifyUserInfo;
import com.example.demo.model.request.JoinConferenceGroup;
import com.example.demo.model.response.ConferenceDetail;
import com.example.demo.model.response.EntryFormInfo;
import com.example.demo.model.response.JudgeDetail;
import com.example.demo.model.response.RepostInfo;

import java.util.List;

/**
 * @Author : 陈瀚清
 * @Description: 用户服务
 * @Date created at 2018/6/30
 **/
public interface UserService {
    /**
     * 查询论文详细信息
     * @param id 会议Id
     * @return 查询结果
     */
    ConferenceDetail getConference(Integer id);

    /**
     * 上传论文
     * @param conferenceId 会议id
     * @param contributionInfo 论文信息
     * @return 查询结果
     */
    void contributePaper(Integer conferenceId, ContributionInfo contributionInfo);

    /**
     * 注册会议
     * @param conferenceID 会议id
     * @param joinConferenceGroup 参与者集合
     */
    void handInConferenceRegistrationForm(int conferenceID, JoinConferenceGroup joinConferenceGroup);

    List<JudgeDetail> getJudgeDetail();

    void repostPaper(Integer paperId, ResourceType type, RepostInfo repostInfo);

    /**
     * 修改当前用户的信息
     * @param userInfo 用户信息
     */
    void modifyUserInfo(IModifyUserInfo userInfo);

    List<EntryFormInfo> getEntry();
}
