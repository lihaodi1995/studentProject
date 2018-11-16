package com.example.demo.utils.serializer;

import com.example.demo.model.request.ConferenceInfo;
import com.example.demo.model.response.ConferenceListItem;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;

import java.io.IOException;

public class OrganizationInfoSerializer extends JsonSerializer<ConferenceListItem.OrganizationInfo> {

    @Override
    public void serialize(ConferenceListItem.OrganizationInfo organizationInfo, JsonGenerator jsonGenerator, SerializerProvider serializerProvider) throws IOException {
        try {
            jsonGenerator.writeString(organizationInfo.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
