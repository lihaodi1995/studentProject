package dataAccessLayer.util;

import org.apache.commons.lang.math.RandomUtils;

import java.util.Date;

//本资源作为数据访问层密集信息内聚的字符串管理
public class R {

    //一些字段的取值枚举，在格式上为 表名_字段名_枚举名
    public static final String TIME_STANDERD_FORMAT = "yyyy-MM-dd HH:mm:ss";


    public static final int USER_BBSSTATUS_BAN = -1;

    public static final int PRODUCT_RECOMMENDSTATUS_HIDDEN = 0;
    public static final int PRODUCT_RECOMMENDSTATUS_NORMAL = 1;
    public static final int PRODUCT_RECOMMENDSTATUS_RECOMMEND = 2;
    public static final int PRODUCT_RECOMMENDSTATUS_APPLY = 3;

    public static final int AD_SORTREF_INIT = 0;

    public static final int AD_ZONECODE_INIT = 10;

    public static final int BBSPART_SORTREF_INIT = 0;
    //对商铺状态的枚举,{-2,-1,0,1,2}分别对应{有店铺且被取缔,没有店铺，有店铺但是没认证，有店铺等待认证，有店铺且被认证}
    public static final Integer SHOP_REVOKED = -2;
    public static final Integer SHOP_NOT_BOUND = -1;
    public static final Integer SHOP_BOUND_NOT_VERIFIED = 0;
    public static final Integer SHOP_BOUND_WAITING_VERIFY = 1;
    public static final Integer SHOP_VERIFIED = 2;

    public static final int ADPART_SORTREF_INIT = 0;
    public static final String PATH_RELA_PICS = "/uploads/";
    public static final String PATH_HOST_URL_PREFIX = "ERM-WebIO-1.0";
    public static final String PATH_404_PIC_URL = PATH_HOST_URL_PREFIX + PATH_RELA_PICS + "404.jpeg";
    //添加一个对存储的图片资源的存放的相对地址
    public static String PATH_ABS_WEBROOT_PATH = "";

    public static String generateRandomString() {
        Date date = new Date();
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append(RandomUtils.nextInt());
        stringBuilder.append(date.getTime());
        stringBuilder.append(RandomUtils.nextInt());
        return stringBuilder.toString();
    }
}
