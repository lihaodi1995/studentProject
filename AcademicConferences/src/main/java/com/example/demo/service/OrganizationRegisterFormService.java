package com.example.demo.service;

import com.example.demo.model.entity.RegisterFormEntity;
import org.springframework.data.domain.Page;

/**
 * @Author : 叶明林
 * @Description: 机构注册表单的相关接口
 * @Date created at 2018/7/1 22:09
 **/
public interface OrganizationRegisterFormService {
    /**
     * 查找指定状态的注册表单
     * @param index 页号
     * @param size 页大小
     * @param status 状态
     * @return 符合条件的表单信息
     */
    Page<RegisterFormEntity> getRegisterFormsByStatus(Integer index, Integer size, RegisterFormEntity.HandleStatus status);

    /**
     * 根据注册申请表单id查看表单详细信息
     * @param formId 申请表单id
     * @return 表单详细信息
     */
    RegisterFormEntity getRegisterFormDetailsByFormId(Integer formId);


    /**
     * 修改指定注册申请表单的进度(不检查参数合法性，不合法时不进行任何操作)
     * @param formId 表单ID
     * @param newStatus 新的进度
     * @return true表示修改成功，false为失败
     **/
    boolean changeStatusOfRegisterForm(Integer formId,RegisterFormEntity.HandleStatus newStatus);

    /**
     * 设置某个机构注册表的审核结果
     * @param formId 注册表ID
     * @param registerResult 审核结果
     * @return 是否设置成功
     */
    boolean setHandleResultOfRegisterForm(Integer formId,String registerResult);
}
