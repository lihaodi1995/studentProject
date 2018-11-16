package com.example.demo.exception;

/**
 * @Author : 叶明林
 * @Description: 异常信息
 * @Date created at 2018/5/17 16:18
 **/
public final class ExceptionInfo {

    /**
     * 验证类错误码为1XX
     */
    public static final ErrorUnit USER_PERMISSION_NEEDED=
            ErrorUnit.info(100,"未登录");

    public static final ErrorUnit PERMISSION_DENIED=
            ErrorUnit.info(101,"没有权限");

    public static final ErrorUnit PWD_NOT_MATHCHED=
            ErrorUnit.info(103,"密码错误");

    public static final ErrorUnit PASSWORD_ERROR_LIMIT=
            ErrorUnit.info(104,"密码错误次数过多");
    /**
     * IO类错误码为2XX
     */
    public static final ErrorUnit UPLOAD_SAVE_ERROR=
            ErrorUnit.info(200,"保存文件出错");

    public static final ErrorUnit FORMAT_ERROR=
            ErrorUnit.info(201,"文件格式");

    public static final ErrorUnit UPLOAD_EMPTY_FILE=
            ErrorUnit.info(202,"上传空文件");

    public static final ErrorUnit UPLOAD_EMPTY_CONTENT_TYPE=
            ErrorUnit.info(203,"文件类型信息缺失");

    public static final ErrorUnit UPLOAD_FORMAT_NOT_SUPPORTED=
            ErrorUnit.info(204,"不支持的文件类型");

    public static final ErrorUnit BASE64_DECODE_ERROR=
            ErrorUnit.info(205,"base64解码错误");

    public static final ErrorUnit FILE_READ_ERROR=
            ErrorUnit.info(206,"文件读入错误");

    public static final ErrorUnit FILE_DOWNLOAD_ERROR=
            ErrorUnit.info(207,"文件下载发生错误");

    public static final ErrorUnit FILE_NOT_EXIST=
            ErrorUnit.info(208,"文件资源不存在");

    /**
     * 业务错误码为3XX
     */
    public static final ErrorUnit ORGANIZATION_NOT_EXIST=
            ErrorUnit.info(300,"组织机构不存在");

    public static final ErrorUnit USER_NOT_EXIST=
            ErrorUnit.info(301,"用户未注册");

    public static final ErrorUnit USERNAME_EXISTED=
            ErrorUnit.info(302,"用户已被注册");

    public static final ErrorUnit CONFERENCE_NOT_EXIST=
            ErrorUnit.info(303,"会议不存在");

    public static final ErrorUnit RESULT_NOT_FOUND=
            ErrorUnit.info(304,"查询结果为空");

    public static final ErrorUnit PAPER_NOT_EXIST=
            ErrorUnit.info(305,"论文不存在");

    public static final ErrorUnit PAPER_JUDGED=
            ErrorUnit.info(306,"论文已评审");

    public static final ErrorUnit REGISTRATION_FORM_NOT_FOUND=
            ErrorUnit.info(307,"注册表单不存在");

    public static final ErrorUnit REGISTRATION_STATUS_CHANGE_ILLEGAL=
            ErrorUnit.info(307,"非法的注册表单处理状态变更");

    public static final ErrorUnit PAPER_CAN_NOT_BE_MODIFIED=
            ErrorUnit.info(308,"论文第一作者不是当前用户，无法修改");

    public static final ErrorUnit COLLECTION_NOT_FOUND=
            ErrorUnit.info(309,"收藏不存在");

    public static final ErrorUnit ENTRYFORM_NOT_EXIST=
            ErrorUnit.info(310,"报名表不存在");

    public static final ErrorUnit ADMIN_NOT_EXIST=
            ErrorUnit.info(311,"管理员不存在");

    public static final ErrorUnit TIMEOUT=
            ErrorUnit.info(312,"已超过截止日期");

    public static final ErrorUnit ENTRY_HANDLED=
            ErrorUnit.info(313,"报名已处理");

    public static final ErrorUnit NO_PERMISSION=
            ErrorUnit.info(314,"没有查看权限");

    public static final ErrorUnit WRONG_DATE_RELATION=
            ErrorUnit.info(315,"日期关系错误");

    public static final ErrorUnit WRONG_JUDGESTATUS=
            ErrorUnit.info(316,"评审结果不合法");

    public static final ErrorUnit CONFERENCE_DELETE_NOT_ALLOWED=
            ErrorUnit.info(317,"该会议不允许被删除");

    public static final ErrorUnit EMAIL_NULL=
            ErrorUnit.info(318,"未设置邮箱");

    public static final ErrorUnit NICKNAME_EXIST=
            ErrorUnit.info(319,"昵称已被使用");

    public static final ErrorUnit PAPER_NOT_QUALIFIED=
            ErrorUnit.info(319,"该论文未通过");

    /**
     * 其他错误码为4XX
     */
    public static final ErrorUnit PARAMS_ILLEGAL=
            ErrorUnit.info(400,"参数错误");

    public static final ErrorUnit PAGENUMBER_INVALID=
            ErrorUnit.info(401,"页号非法");

    public static final ErrorUnit EMAIL_INVALID=
            ErrorUnit.info(402,"邮箱地址格式错误");

    public static final ErrorUnit EMAIL_AUTHORIZE_ERROR =
            ErrorUnit.info(403,"邮箱授权错误");

    public static final ErrorUnit EMAIL_ADDRESS_NOT_EXIST =
            ErrorUnit.info(404,"邮箱不可达");

    public static final ErrorUnit EMAIL_SENDING_ERROR =
            ErrorUnit.info(405,"发送邮件时发生错误");
}
