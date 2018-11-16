package com.example.demo.service;

import com.example.demo.model.response.ConferenceListItem;
import com.example.demo.model.response.ListPage;

import java.util.List;

/**
 * @Author : 陈瀚清
 * @Description: 收藏相关操作
 * @Date created at 2018/6/7
 **/
public interface CollectionService {
    /**
     * 添加收藏
     * @param conferenceId 会议id号
     */
    public void addCollection(int conferenceId);

    /**
     * 取消收藏
     * @param conferenceId 会议id号
     */
    public void deleteCollection(int conferenceId);

    /**
     * 清空收藏
     */
    public void clearCollection();

    /**
     * 获得收藏列表
     */
    public ListPage<ConferenceListItem> getCollection(int pageNumber);


    /**
     * 用户是否收藏
     * @param conferenceId 会议id
     * @return 用户是否收藏
     */
    public boolean haveCollected(int conferenceId);
}
