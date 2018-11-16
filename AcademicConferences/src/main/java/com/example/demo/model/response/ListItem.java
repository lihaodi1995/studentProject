package com.example.demo.model.response;

public interface ListItem<T,Y> {
    public T getListItem(Y p);//从Y(entity)中取T(item)
}
