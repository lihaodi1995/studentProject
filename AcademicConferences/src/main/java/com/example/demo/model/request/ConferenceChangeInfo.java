package com.example.demo.model.request;

import com.example.demo.utils.deserializer.TimeStampDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import io.swagger.annotations.ApiModelProperty;

import java.sql.Timestamp;

public class ConferenceChangeInfo extends ConferenceInfo {
    @ApiModelProperty(value = "修改稿截止日期")
    private Timestamp repostDdlDate;

    public Timestamp getRepostDdlDate() {
        return repostDdlDate;
    }

    @JsonDeserialize(using = TimeStampDeserializer.class)
    public void setRepostDdlDate(Timestamp repostDdlDate) {
        this.repostDdlDate = repostDdlDate;
    }
}
