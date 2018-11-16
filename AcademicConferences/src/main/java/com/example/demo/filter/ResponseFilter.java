package com.example.demo.filter;

import com.example.demo.utils.JsonUtil;
import com.example.demo.utils.ResponseWrapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.log4j.Logger;
import org.springframework.core.annotation.Order;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@WebFilter(filterName = "responseFilter", urlPatterns = "/api/*")
@Order(2)
public class ResponseFilter implements Filter {
    private Logger logger = Logger.getLogger(ResponseFilter.class);
    @Override
    public void init(FilterConfig filterConfig){

    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain)
    {
        HttpServletResponse response = (HttpServletResponse) servletResponse;
        response.setHeader("charset","utf-8");
        response.setCharacterEncoding("utf-8");
        response.setHeader("Connection","Keep-Alive");
        ResponseWrapper wrapper=new ResponseWrapper(response);
        HttpSession session = ((HttpServletRequest)servletRequest).getSession();
        try
        {
            filterChain.doFilter(servletRequest,wrapper);
            addStatusToJsonContent(wrapper,response,session.getId());
        }
        catch (Exception e)
        {
            logger.info(e.getMessage());
            e.printStackTrace();
        }

    }

    @Override
    public void destroy() {

    }

    @SuppressWarnings("unchecked")
    private void addStatusToJsonContent(ResponseWrapper wrapper, ServletResponse response,String sessionId)throws IOException
    {
        String content=new String(wrapper.getContent(),"UTF-8");
        ObjectMapper objectMapper = new ObjectMapper();
        Map<String,Object> tmp = new HashMap<>();
        if(!content.isEmpty())
        {
            Object data = objectMapper.readValue(content, Object.class);
            if(data instanceof Map)
                tmp = (Map)data;
            else
                tmp.put("data",data);
        }
        tmp.put("JSESSIONID",sessionId);
        if(!tmp.containsKey("errorCode"))
            tmp.put("errorCode",0);
        String json= JsonUtil.convertObjectToJSON(tmp);
        byte[] bytes = json.getBytes("utf-8");
        response.setContentLength(bytes.length);
        response.setContentType("application/json;charset=utf-8");
        ((HttpServletResponse)response).setStatus(200);
        ServletOutputStream out = response.getOutputStream();
        out.write(bytes);
        out.flush();
        out.close();
    }
}
