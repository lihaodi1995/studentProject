package com.example.demo.utils.serializer;

import com.example.demo.model.base.EntityBase;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;

import java.io.IOException;

public class NameJsonSerializer extends JsonSerializer<EntityBase> {
    @Override
    public void serialize(EntityBase entityBase, JsonGenerator jsonGenerator, SerializerProvider serializerProvider) throws IOException {
        try {
            jsonGenerator.writeString(entityBase.getName());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
