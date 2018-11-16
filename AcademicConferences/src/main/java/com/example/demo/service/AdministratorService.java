package com.example.demo.service;

import com.example.demo.model.entity.RegisterFormEntity;
import com.example.demo.model.response.ListPage;
import com.example.demo.model.response.RegisterFormInfo;

import java.util.List;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/6/30 20:35
 **/
public interface AdministratorService {
    /**
     * 管理员查找指定状态的注册表单
     * @param index 页号
     * @param size 页大小
     * @param status 状态
     * @return 含有统计信息的数据
     */
    ListPage<RegisterFormInfo> getRegisterFormsByStatus(Integer index, Integer size,
                                                  RegisterFormEntity.HandleStatus status);

    /**
     * 管理员处理机构注册表单
     * @param registrationID 表单ID
     * @param organizationStatus 是否同意机构注册
     * @param result 审核意见
     */
    void handleRegistrationForm(Integer registrationID ,boolean organizationStatus,String result);
}
