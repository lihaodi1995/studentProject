package com.example.demo.utils;

import java.io.Serializable;

public class BaseRequestEntity<T> implements Serializable {
    private T data;

    public BaseRequestEntity() {}

    public BaseRequestEntity( T data) {
        this.data = data;
    }
    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }
}