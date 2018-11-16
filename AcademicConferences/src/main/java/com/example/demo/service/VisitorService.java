package com.example.demo.service;

import com.example.demo.model.response.ConferenceListItem;
import com.example.demo.model.response.ListPage;

/**
 * @Author : 陈瀚清
 * @Description: 游客服务
 * @Date created at 2018/6/30
 **/
public interface VisitorService {

    /**
     * 查询论文
     * @param name
     * @param startDDL 截稿范围开始、结束
     * @param endDDL
     * @param startConf 会议范围开始、结束
     * @param endConf
     * @param organizationId 机构id
     * @param page
     * @return 分页查询结果
     */
    ListPage<ConferenceListItem> getConferenceList(String name,Long startDDL,Long endDDL,Long startConf,Long endConf,Long organizationId,Integer page);
}
