package com.example.demo.utils;

import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import com.example.demo.model.response.ListItem;
import com.example.demo.model.response.ListPage;
import org.springframework.data.domain.Page;

import java.util.ArrayList;
import java.util.List;

/**
 * @Author : 陈瀚清
 * @Description: Page转化为ListPage
 * @Date created at 2018/6/6 0:25
 **/
public class PageFactory<T,Y> {//T为item,Y为entity
    public ListPage getListPage(Page page, int pageSize, ListItem listItem){
        ListPage<T> p=new ListPage<>(pageSize);
        int total=page.getTotalPages();
        p.setTotalPage(total);
        p.setTotalElement(page.getTotalElements());
        p.setNowPage(page.getNumber()+1);
        List<Y> list=page.getContent();
        List<T> item=new ArrayList<>();
        for(Y i : list){
            item.add((T)listItem.getListItem(i));
        }
        p.setItems(item);
        return p;
    }

    public static void checkPageNumber(Page page){//搜索结果页号检查
        if(page.getTotalPages()!=0&&page.getTotalPages()<page.getNumber()+1){
            throw new BusinessException(ExceptionInfo.PAGENUMBER_INVALID);
        }
        else if(page.getTotalPages()==0&&page.getNumber()>=1){
            throw new BusinessException(ExceptionInfo.PAGENUMBER_INVALID);
        }
    }

    public static Integer checkPageNumber(Integer page){//输入页号检查转换
        if(page>0) {
            return page - 1;
        }
        else
            throw new BusinessException(ExceptionInfo.PAGENUMBER_INVALID);
    }
}
