package userController.utils;

import java.util.ArrayList;
import java.util.Arrays;

//本文作为对用户的控制层和的字符串的常见的约定
public class R {
    //reset password step
    public static final String SESSION_KEY_PASSWORD_PHONE = "pwPhone";
    public static final String SESSION_KEY_PASSWORD_CODE = "pwCode";

    public static final String PASSWORD_STEP1 = "step1";
    public static final String PASSWORD_STEP2 = "step2";

    //对所需的产品所在版块的枚举
    public static final String JSON_VALUE_TYPE_SELECTED = "selected";
    public static final String JSON_VALUE_TYPE_NEWEST = "newest";

    //约定一页的条目数量
    public static final Integer PAGE_SIZE = 16;
    public static final Integer PAGE_SIZE_12 = 20;

    //枚举操作的结果
    public static final String JSON_VALUE_VALUE_YES = "yes";
    public static final String JSON_VALUE_VALUE_NO = "no";
    //枚举新的操作结果。上面的作废
    public static final String JSON_VALUE_VALUE_SUCCESS = "success";
    public static final String JSON_VALUE_VALUE_FAIL = "fail";
    //商品的状态的status的枚举
    public static final Integer PRODUCT_STATUS_HIDDEN = -1;
    public static final Integer PRODUCT_STATUS_NOT_SEEN = 0;
    public static final Integer PRODUCT_STATUS_NORMAL = 1;
    public static final Integer PRODUCT_STATUS_RECOMMENDED = 2;
    public static final Integer PRODUCT_STATUS_APPLYING = 3;
    //在电话验证中，对type的枚举
    public static final String JSON_VALUE_TYPE_STEP1 = "step1";
    public static final String JSON_VALUE_TYPE_STEP2 = "step2";
    //session中放入的验证码
    public static final String SESSION_KEY_VERIFY_CODE = "verifyCode";
    public static final String SESSION_KEY_NEW_PHONE = "newPhone";
    public static final String SESSION_KEY_PASS_PHONE_CHECK = "passPhoneCheck";

    //session中放入的登录用户的对象
    public static final String SESSION_KEY_USER = "user";
    //对发表bbs的type的枚举
    public static final String JSON_VALUE_TYPE_BBS = "bbs";
    public static final String JSON_VALUE_TYPE_REPLY = "reply";

    //encode
    public static final String UTF8 = "utf-8";

    //Notifications
    public static final String NOT_USER_WELCOME = "";

    public static final String NOT_ISSUE_SUBMITTED = "您的投诉请求已经被系统受理,请耐心等待仲裁结果。";

    public static final String NOT_ISSUE_FAIL = "";

    public static final String NOT_INFO_EDIT_SUCCESS = "您成功修改了信息。";

    public static final String NOT_TITLE_SYS_NORMAL = "一般事务";

    public static final String NOT_TITLE_SYS_ISSUE = "仲裁庭";

    public static final String NOT_TYPE_SYS = "系统";
    //错误信息集
    public static final String FAIL_LOGIN_CHECK_FAIL = "电话和密码的校验错误!";
    public static final String FAIL_LOGOUT_NOT_EVEN_LOGIN_BEFOPRE = "您未曾登录!";
    public static final String FAIL_EDIT_INFO_NAME_HAS_BEEN_USED = "该名字已经被用过";
    public static final String FAIL_ID_CHECK_FAIL = "身份证认证失败,所输入的信息不正确!";
    public static final String FAIL_PHONE_CHECK_HAS_BEEN_UESD = "该电话已经被其他用户绑定.";
    public static final String FAIL_PHONE_CHECK_STEP1_NOT_DONE = "您甚至还没有发起过向手机发验证码的请求.";
    public static final String FAIL_PHONE_CHECK_CODE_WRONG = "您输入的验证码错误!";
    public static final String FAIL_NOT_LOGIN = "您还未登录或者身份信息有误";
    public static final String FAIL_FORMAT_WRONG = "您输入的信息有格式错误";
    public static final String FAIL_NO_SHOP_BOUND = "您还未绑定店铺";
    public static final String FAIL_NOT_LOGOUT_YET = "您还未注销登录";
    public static final String FAIL_NOT_PASS_PHONE_CHECK_YET = "您还未能通过电话验证";
    public static final String FAIL_NICK_HAS_BEEN_UESD_OR_FORMAT_WRONG = "昵称被使用过,或者输入的账户有格式错误!";
    public static final String FAIL_SHOP_HAS_BEEN_BOUND_BY_OTHERS = "店铺已经被他人绑定";
    public static final String FAIL_YOU_HAVE_BOUND_SHOP = "您已经绑定过了店铺";
    public static final String FAIL_PRODUCT_CHANGE_STATUS_PERMISSION_FAIL = "您无权将状态改到目标级别";
    public static final String FAIL_ARG_WRONG = "参数错误,目标项已经被删除或不存在";
    public static final String FAIL_NO_PERMISSION = "权限检查,非法操作!";
    //AD part 四张广告版块的图片
    public static final ArrayList<String> AD_PART_PICS = new ArrayList<>(Arrays.asList("s1.jpg",
            "s2.jpg",
            "s3.jpg",
            "s4.jpg"));


    //
    public static final String HEADER_KEY_CONTENT_TYPE="Content-Type";
    public static final String HEADER_VALUE_FORM_URL_ENCODE="application/x-www-form-urlencoded";

}
