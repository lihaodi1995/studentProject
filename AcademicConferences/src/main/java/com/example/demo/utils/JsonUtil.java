package com.example.demo.utils;

import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonUtil {

    //将Map对象转化为json
    public static String convertObjectToJSON(Object object)
    {
        String jsonStr=null;
        try
        {
            ObjectMapper mapper = new ObjectMapper();
            jsonStr=mapper.writeValueAsString(object);
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        return jsonStr;
    }
}
