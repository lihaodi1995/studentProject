package com.example.demo.model.request;

import com.example.demo.model.entity.SuperParticipantEntity;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
 * Created by 44910_000 on 2018/7/1.
 */
public class UserConferenceRegistrationForm {
    private int conferenceID;

    private JoinConferenceGroup joinConferenceGroup;

    public int getConferenceID() {
        return conferenceID;
    }

    public void setConferenceID(int conferenceID) {
        this.conferenceID = conferenceID;
    }

    public JoinConferenceGroup getJoinConferenceGroup() {
        return joinConferenceGroup;
    }

    public void setJoinConferenceGroup(JoinConferenceGroup joinConferenceGroup) {
        this.joinConferenceGroup = joinConferenceGroup;
    }
}
