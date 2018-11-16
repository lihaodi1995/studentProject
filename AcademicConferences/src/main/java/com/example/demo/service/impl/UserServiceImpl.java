package com.example.demo.service.impl;

import com.example.demo.component.UploadStrategy;
import com.example.demo.component.UploadStrategyFactory;
import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import com.example.demo.jpa.*;
import com.example.demo.model.base.Identification;
import com.example.demo.model.base.ResourceType;
import com.example.demo.model.entity.*;
import com.example.demo.model.request.*;
import com.example.demo.model.response.ConferenceDetail;
import com.example.demo.model.response.EntryFormInfo;
import com.example.demo.model.response.JudgeDetail;
import com.example.demo.model.response.RepostInfo;
import com.example.demo.service.AuthentificationService;
import com.example.demo.service.UserService;
import com.example.demo.utils.FileTransform;
import com.example.demo.utils.IdentificationFactory;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.sql.Timestamp;
import java.util.*;

import static com.example.demo.exception.ExceptionInfo.NICKNAME_EXIST;
import static com.example.demo.exception.ExceptionInfo.PAPER_NOT_EXIST;
import static com.example.demo.exception.ExceptionInfo.PAPER_NOT_QUALIFIED;

/**
 * @Author : 陈瀚清
 * @Description: 用户服务
 * @Date created at 2018/6/30
 **/
@Service
public class UserServiceImpl implements UserService {
    private ConferenceRepository conferenceRepository;
    private final AuthentificationService authentificationService;
    private final UserRepository userRepository;
    private final UploadStrategyFactory uploadStrategyFactory;
    private final ResourceUploadService resourceUploadService;
    private Logger logger = Logger.getLogger(UserServiceImpl.class);
    private final PaperRepository paperRepository;
    private final EntryFormRepository entryFormRepository;
    private final AttachmentRepository attachmentRepository;

    @Autowired
    public UserServiceImpl(ConferenceRepository conferenceRepository,
                           AuthentificationService authentificationService, UserRepository userRepository, UploadStrategyFactory uploadStrategyFactory, PaperRepository paperRepository, ResourceUploadService resourceUploadService, EntryFormRepository entryFormRepository, AttachmentRepository attachmentRepository) {
        this.conferenceRepository = conferenceRepository;
        this.authentificationService = authentificationService;
        this.userRepository = userRepository;
        this.uploadStrategyFactory = uploadStrategyFactory;
        this.paperRepository = paperRepository;
        this.resourceUploadService = resourceUploadService;
        this.entryFormRepository = entryFormRepository;
        this.attachmentRepository = attachmentRepository;
    }

    @Override
    public ConferenceDetail getConference(Integer id) {
        Optional<ConferenceEntity> optional=conferenceRepository.findById(id);
        if(optional.isPresent()){
            ConferenceEntity conferenceEntity=optional.get();
            ConferenceDetail detail=new ConferenceDetail(conferenceEntity);
            return detail;
        }
        else{
            throw new BusinessException(ExceptionInfo.RESULT_NOT_FOUND);
        }
    }

    @Override
    public void contributePaper(Integer conferenceId, ContributionInfo contributionInfo) {
        Optional<ConferenceEntity> conf=this.conferenceRepository.findById(conferenceId);
        UserEntity identification=(UserEntity)authentificationService.getCurrentUser();
        Long id=identification.getId();
        MultipartFile file=FileTransform.Base64ToMultipartFile(contributionInfo.getFile());
        if(conf.isPresent()){
            ConferenceEntity conferenceEntity=conf.get();
            checkTimestampBeforeNow(conferenceEntity.getDdlDate());
            AttachmentEntity attachmentEntity=
                    resourceUploadService.uploadFile(file,null,generateUploadStrategy(ResourceType.Paper));
            PaperEntity paper=new PaperEntity((UserEntity)identification,null,
                    contributionInfo.getTitle(),identification.getInstitution(),
                    conferenceEntity,contributionInfo.getAbstractInfo());
            paper.setLastModDate(new Timestamp(System.currentTimeMillis()));
            Set<AttachmentEntity> attachmentEntitySet=new HashSet<>();
            attachmentEntitySet.add(attachmentEntity);
            paper.setAttachments(attachmentEntitySet);
            this.paperRepository.save(paper);
        }
        else{
            throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        }
    }



    @Override
    public void handInConferenceRegistrationForm(int conferenceID, JoinConferenceGroup joinConferenceGroup) {
        List<AttachmentEntity> attachmentEntityList=null;
        EntryFormEntity entryFormEntity=new EntryFormEntity();
        Optional<ConferenceEntity> conf=this.conferenceRepository.findById(conferenceID);
        UserEntity userEntity=(UserEntity) this.authentificationService.getCurrentUser();
        if(conf.isPresent()){
            ConferenceEntity conferenceEntity=conf.get();
            checkTimestampBeforeNow(conferenceEntity.getRegisterDate());
            entryFormEntity.setConference(conferenceEntity);
            entryFormEntity.setUser(userEntity);
            Set<SuperParticipantEntity> superParticipantEntities=new HashSet<>();
            Integer paperid=joinConferenceGroup.getPaperID();

            if(paperid!=null)
            {
                Optional<PaperEntity> optionalPaperEntity = this.paperRepository.findById(paperid);
                if(!optionalPaperEntity.isPresent())
                    throw new BusinessException(PAPER_NOT_EXIST);
                else if(!optionalPaperEntity.get().getJudgeStatus().equals(PaperEntity.JudgeStatus.Qualified))
                    throw new BusinessException(PAPER_NOT_QUALIFIED);
            }

            List<JoinConferencePeople> joinConferencePeoples=joinConferenceGroup.getJoinConferencePeopleList();
            for(JoinConferencePeople j:joinConferencePeoples){
                SuperParticipantEntity superParticipantEntity=new SuperParticipantEntity(paperid,j.getName(),j.getSex(),
                        j.getRealID(),j.getOrdered());
                superParticipantEntities.add(superParticipantEntity);
            }
            entryFormEntity.setParticipants(superParticipantEntities);
            List<MultipartFile> evidence=FileTransform.Base64ToMultipartFile(joinConferenceGroup.getEvidence());
            attachmentEntityList=resourceUploadService.uploadFiles(evidence,null,generateUploadStrategy(ResourceType.Image));
            Set<AttachmentEntity> attachmentEntitySet=new HashSet<>(attachmentEntityList);
            entryFormEntity.setProof(attachmentEntitySet);
            entryFormRepository.save(entryFormEntity);
        }
        else{
            throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        }
    }

    private UploadStrategy generateUploadStrategy(ResourceType type)
    {
        switch(type){
            case Image:
                return new UploadStrategy() {
                    @Override
                    public String getStorePath(Object object) {
                        return "/usr/share/contributePaper";
                    }
                    @Override
                    public List<String> getSupportTypeOfUploadFile() {
                        return Arrays.asList("png","jpg","pdf");
                    }
                    @Override
                    public ResourceType getSupportResourceType() {
                        return ResourceType.Image;
                    }
                };
            case Paper:
                return new UploadStrategy() {
                    @Override
                    public String getStorePath(Object object) {
                        return "/usr/share/conferenceRegistrationForm";
                    }
                    @Override
                    public List<String> getSupportTypeOfUploadFile() {
                        return Arrays.asList("doc","docx","pdf");
                    }
                    @Override
                    public ResourceType getSupportResourceType() {
                        return ResourceType.Paper;
                    }
                };
            default:
                return null;
        }
    }

    @Override
    public List<JudgeDetail> getJudgeDetail() {
        Identification identification=authentificationService.getCurrentUser();
        Optional<UserEntity> user = userRepository.findById(identification.getId());
        List<JudgeDetail> judgeDetailList = new ArrayList<>();
        if(!user.isPresent())
            throw new BusinessException(ExceptionInfo.USER_NOT_EXIST);
        for(PaperEntity paper: user.get().getPapers()){
            judgeDetailList.add(new JudgeDetail(paper, paper.getConference()));
        }
        return judgeDetailList;
    }

    @Override
    public void repostPaper(Integer paperId, ResourceType type, RepostInfo repostInfo) {
        Optional<PaperEntity> paper = this.paperRepository.findById(paperId);
        if(paper.isPresent()){
            PaperEntity paperEntity = paper.get();
            ConferenceEntity conference = paperEntity.getConference();
            Timestamp modDate = longToTimestamp(repostInfo.getRepostDate());
            if(repostInfo.getRepostDate() == null)
                repostInfo.setRepostDate(System.currentTimeMillis());
            if(conference.getRepostDdlDate() != null && modDate != null) {
                if (!conference.getRepostDdlDate().after(modDate)) {
                    throw new BusinessException(ExceptionInfo.TIMEOUT);
                }
            }
            Identification identification = authentificationService.getCurrentUser();
            if (!identification.getId().equals(paperEntity.getFirstauthor().getId()))
                throw new BusinessException(ExceptionInfo.PAPER_CAN_NOT_BE_MODIFIED);
            List<MultipartFile> multipartFileList = FileTransform.Base64ToMultipartFile(repostInfo.getFiles());
            List<AttachmentEntity> attachmentEntityList = resourceUploadService.uploadFiles(multipartFileList, null, generateUploadStrategy(ResourceType.Paper));
            for(AttachmentEntity attachment: attachmentEntityList)
                this.attachmentRepository.save(attachment);
            Set<AttachmentEntity> attachmentEntitySet = new HashSet<>(attachmentEntityList);
            paperEntity.setAttachments(attachmentEntitySet);
            paperEntity.setModInfo(repostInfo.getModInfo());
            paperEntity.setLastModDate(modDate);
            this.paperRepository.save(paperEntity);
        }
        else{
            throw new BusinessException(ExceptionInfo.PAPER_NOT_EXIST);
        }
    }

    @Override
    public void modifyUserInfo(IModifyUserInfo userInfo) {
        UserInfoModificationReq req = (UserInfoModificationReq) userInfo;
        if(this.userRepository.existsByNickNameEquals(req.getNickname()))
            throw new BusinessException(NICKNAME_EXIST);
        Identification identification = this.authentificationService.getCurrentUser();
        userInfo.modifyUser(identification);
        IdentificationFactory factory = IdentificationFactory.getInstance();
        factory.saveEntity(identification);
    }

    public Timestamp longToTimestamp(Long l){
        if(l!=null){
            try{
                return new Timestamp(l);
            }catch (IllegalArgumentException e){
                throw new BusinessException(ExceptionInfo.PARAMS_ILLEGAL);
            }
        }
        else return null;
    }

    /**检查时间戳是否早于现在时间
     * @param timestamp 检查的时间戳
     */
    private void checkTimestampBeforeNow(Timestamp timestamp){
        Timestamp now=new Timestamp(System.currentTimeMillis());
        if(timestamp!=null){
            if(timestamp.before(now)){
                throw new BusinessException(ExceptionInfo.TIMEOUT);
            }
        }
    }

    @Override
    public List<EntryFormInfo> getEntry() {
        Identification identification = this.authentificationService.getCurrentUser();
        List<EntryFormEntity> entryFormEntityList = entryFormRepository.findAllByUserEquals((UserEntity)identification);
        List<EntryFormInfo> entryFormInfoList = new ArrayList<>();
        for(EntryFormEntity entry: entryFormEntityList){
            entryFormInfoList.add(new EntryFormInfo(entry));
        }
        return entryFormInfoList;
    }
}
