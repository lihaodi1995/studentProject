package com.example.demo.model.entity;


import javax.persistence.*;
import java.io.Serializable;
import java.util.Set;

@Entity
public class CollectionClassificationEntity implements Serializable{
    @Id
    @GeneratedValue
    private Integer id;

    private String name;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private UserEntity owner;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
            joinColumns = {@JoinColumn(name = "collectionClassification_id")},
            inverseJoinColumns = {@JoinColumn(name = "conference_id")}
    )
    private Set<ConferenceEntity> conferences;

    public Integer getId() {
        return this.id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public UserEntity getOwner() {
        return owner;
    }

    public void setOwner(UserEntity owner) {
        this.owner = owner;
    }

    public void setConferences(Set<ConferenceEntity> conferences) {
        this.conferences = conferences;
    }

    public Set<ConferenceEntity> getConferences() {
        return conferences;
    }

    public synchronized void removeConference(ConferenceEntity conferenceEntity)
    {
        if(this.conferences==null||!this.conferences.contains(conferenceEntity))
            return ;
        this.conferences.remove(conferenceEntity);
    }
}
