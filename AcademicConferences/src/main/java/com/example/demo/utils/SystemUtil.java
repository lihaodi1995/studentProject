package com.example.demo.utils;

/**
 * @Author : 叶明林
 * @Description: 根据系统返回不同路径
 * @Date created at 2018/7/6 9:47
 **/
public class SystemUtil {
    private String windowsUrl;

    private String linuxUrl;

    private String systemType = System.getProperty("os.name").toLowerCase();

    public SystemUtil(String windowsUrl,String linuxUrl) {
        this.windowsUrl = windowsUrl;
        this.linuxUrl = linuxUrl;
    }

    public String getUrl()
    {
        if(this.systemType.contains("windows"))
            return this.windowsUrl;
        else if(this.systemType.contains("linux"))
            return this.linuxUrl;
        return null;
    }
}
