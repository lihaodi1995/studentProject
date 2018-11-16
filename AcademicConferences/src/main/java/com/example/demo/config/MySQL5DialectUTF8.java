package com.example.demo.config;

import org.hibernate.dialect.MySQL5InnoDBDialect;

/**
 * @Reference : https://blog.csdn.net/mjl960108/article/details/53543083
 * @Description: 数据库配置
 * @Date created at 2018/6/4 17:16
 **/
public class MySQL5DialectUTF8 extends MySQL5InnoDBDialect {

    @Override
    public String getTableTypeString() {
        return " ENGINE=InnoDB DEFAULT CHARSET=utf8";
    }
}
