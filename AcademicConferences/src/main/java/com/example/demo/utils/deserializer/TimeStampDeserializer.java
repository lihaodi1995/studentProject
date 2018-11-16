package com.example.demo.utils.deserializer;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;

import java.io.IOException;
import java.sql.Timestamp;

/**
 * @Author : 叶明林
 * @Description: 字符串转时间json反序列
 * @Date created at 2018/5/31 17:46
 **/
public class TimeStampDeserializer extends JsonDeserializer<Timestamp>{
    @Override
    public Timestamp deserialize(JsonParser jsonParser, DeserializationContext deserializationContext) throws IOException{
        String timeStr =  jsonParser.getText();
        Long time = Long.valueOf(timeStr);
        return new Timestamp(time);
    }
}
