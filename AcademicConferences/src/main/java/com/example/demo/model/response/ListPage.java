package com.example.demo.model.response;

import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ListPage<T> {

    private int nowPage;//当前页数

    private int totalPage;//总页数

    private long totalElement;//总数

    private int pageSize;//每页item数

    private List<T> items;

    public int getNowPage() {
        return nowPage;
    }

    public void setNowPage(int nowPage) {
        this.nowPage = nowPage;
    }

    public int getTotalPage() {
        return totalPage;
    }

    public void setTotalPage(int totalPage) {
        this.totalPage = totalPage;
    }

    public long getTotalElement() {
        return totalElement;
    }

    public void setTotalElement(long totalElement) {
        this.totalElement = totalElement;
    }

    public int getPageSize() {
        return pageSize;
    }

    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }

    public List<T> getItems() {
        return items;
    }

    public void setItems(List<T> items) {
        this.items = items;
    }

    public ListPage(int pageSize) {
        this.pageSize = pageSize;
    }

    public ListPage(List<T> data,int nowPage,int pageSize) {
        if (data == null) {
            data=new ArrayList<>();
        }
        this.items = data;
        this.pageSize = pageSize;
        this.nowPage = nowPage;
        int totalElement = data.size();
        this.totalElement=totalElement;
        this.totalPage = (totalElement + pageSize - 1) / pageSize;
        this.getPagedList();
        this.nowPage+=1;//页号从1开始
    }

    /**
     * 得到分页后的数据
     */
    public void getPagedList() {
        if(totalElement==0)return;
        int fromIndex = nowPage * pageSize;
        if (fromIndex >= totalElement) {
            throw new BusinessException(ExceptionInfo.PAGENUMBER_INVALID);
        }
        int toIndex = (nowPage+1) * pageSize;
        if (toIndex >= totalElement) {
            toIndex = (int)totalElement;
        }
        this.items=items.subList(fromIndex, toIndex);
    }
}
