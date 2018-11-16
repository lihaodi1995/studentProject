package com.example.demo.utils.serializer;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;

import java.io.IOException;
import java.sql.Timestamp;

public class TimeStampJsonSerializer extends JsonSerializer<Timestamp> {

    @Override
    public void serialize(Timestamp date, JsonGenerator jsonGenerator, SerializerProvider serializerProvider) throws IOException {
        try {
            jsonGenerator.writeString(date.toString());
        } catch (IOException e) {
            jsonGenerator.writeString(String.valueOf(date.getTime()));
        }
    }
}
