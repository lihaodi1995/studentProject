package com.example.demo.config;

import com.example.demo.AcademicConferencesApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.context.annotation.Configuration;

/**
 * @Reference : https://blog.csdn.net/u013305783/article/details/74454966
 * @Description: 配置部署后的程序入口
 * @Date created at 2018/6/13 11:50
 **/
@Configuration
public class ServletInitializer extends SpringBootServletInitializer {
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(AcademicConferencesApplication.class);
    }
}
