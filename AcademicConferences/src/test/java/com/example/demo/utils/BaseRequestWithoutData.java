package com.example.demo.utils;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

import java.io.Serializable;

@ApiModel(value = "不带数据区的请求参数实体")
public class BaseRequestWithoutData implements Serializable {
    @ApiModelProperty("最新的token")
    protected String token;

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }
}
