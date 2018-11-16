package com.example.demo.utils;

import com.fasterxml.jackson.databind.ObjectMapper;

public class ConvertUtil {
    public static String convertObjectToJSON(Object object)
    {
        String jakcson=null;
        try
        {
            ObjectMapper mapper = new ObjectMapper();
            jakcson = mapper.writeValueAsString(object);
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        return jakcson;
    }
}
