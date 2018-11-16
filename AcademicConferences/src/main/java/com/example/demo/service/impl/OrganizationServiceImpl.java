package com.example.demo.service.impl;

import com.example.demo.component.*;
import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ExceptionInfo;
import com.example.demo.jpa.*;
import com.example.demo.model.base.Identification;
import com.example.demo.model.base.ResourceType;
import com.example.demo.model.base.Role;
import com.example.demo.model.entity.*;
import com.example.demo.model.request.ConferenceChangeInfo;
import com.example.demo.model.request.ConferenceInfo;
import com.example.demo.model.request.OrganizationRegisterForm;
import com.example.demo.model.request.UserNameAndPassword;
import com.example.demo.model.response.EntryFormInfo;
import com.example.demo.model.response.ListPage;
import com.example.demo.model.response.PaperInfo;
import com.example.demo.service.AuthentificationService;
import com.example.demo.service.OrganizationService;
import com.example.demo.service.ResourceDownloadService;
import com.example.demo.service.UploadFileService;
import com.example.demo.utils.FileTransform;
import com.example.demo.utils.PageFactory;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.sql.Timestamp;
import java.util.*;
import java.util.concurrent.Future;

import static com.example.demo.exception.ExceptionInfo.*;

@Service
public class OrganizationServiceImpl implements OrganizationService {
    private Logger logger = Logger.getLogger(OrganizationServiceImpl.class);

    private final OrganizationRepository organizationRepository;
    private final ConferenceRepository conferenceRepository;
    private final UploadStrategyFactory uploadStrategyFactory;
    private final AuthentificationService authentificationService;
    private final PaperRepository paperRepository;
    private final RegisterFormRepository registerFormRepository;
    private final EmailsUtil emailsUtil;
    private final UploadFileService uploadFileService;
    private final EntryFormRepository entryFormRepository;
    private final AdminRepository adminRepository;

    private final ResourceDownloadService resourceDownloadService;

    private final CollectionClassificationRepository collectionClassificationRepository;

    private final ExcelGenerator excelGenerator;

    @Autowired
    public OrganizationServiceImpl(OrganizationRepository organizationRepository,
                                   ConferenceRepository conferenceRepository,
                                   UploadStrategyFactory uploadStrategyFactory,
                                   AuthentificationService authentificationService, EmailsUtil emailsUtil, UploadFileService uploadFileService,
                                   RegisterFormRepository registerFormRepository,
                                   PaperRepository paperRepository,
                                   EntryFormRepository entryFormRepository, AdminRepository adminRepository, ResourceDownloadService resourceDownloadService, ExcelGenerator excelGenerator, CollectionClassificationRepository collectionClassificationRepository){
        this.organizationRepository = organizationRepository;
        this.conferenceRepository = conferenceRepository;
        this.uploadStrategyFactory = uploadStrategyFactory;
        this.authentificationService = authentificationService;
        this.emailsUtil = emailsUtil;
        this.registerFormRepository = registerFormRepository;
        this.uploadFileService = uploadFileService;
        this.paperRepository = paperRepository;
        this.entryFormRepository = entryFormRepository;
        this.adminRepository = adminRepository;
        this.resourceDownloadService = resourceDownloadService;
        this.excelGenerator = excelGenerator;
        this.collectionClassificationRepository = collectionClassificationRepository;
    }

    @Override
    public void conferencePost(Long organizationId, ConferenceInfo conferenceInfo, List<AttachmentEntity> attachmentEntityList) {
        Optional<OrganizationEntity> organizationEntityOptional = organizationRepository.findById(organizationId);
        OrganizationEntity organizationEntity;
        if(!organizationEntityOptional.isPresent())
            throw new BusinessException(ExceptionInfo.ORGANIZATION_NOT_EXIST);
        organizationEntity = organizationEntityOptional.get();
        ConferenceEntity conferenceEntity = new ConferenceEntity(organizationEntity, conferenceInfo, attachmentEntityList);
        conferenceEntity.setSetDate(new Timestamp(System.currentTimeMillis()));
        conferenceRepository.save(conferenceEntity);
    }

    @Override
    public List<AttachmentEntity> uploadResource(List<String> stringList, ResourceType type, Long organizationid){
        try{
            List<MultipartFile> files = FileTransform.Base64ToMultipartFile(stringList);
            return this.uploadFileService.uploadFiles(files, null,this.generateTemplateUploadStrategy());
        }
        catch (IOException e){
            this.logger.info(this.authentificationService.getCurrentUser().getUserName()+" 用户上传文件时发生错误");
            throw new BusinessException(ExceptionInfo.UPLOAD_SAVE_ERROR);
        }
    }

    @Override
    public ListPage<PaperInfo> getPaperList(Integer conferenceId, Integer page) {
        Identification identification = authentificationService.getCurrentUser();
        Optional<ConferenceEntity> conferenceEntity = conferenceRepository.findById(conferenceId);
        if(!conferenceEntity.isPresent())
            throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        List<PaperInfo> paperInfoList = new ArrayList<>();
        ConferenceEntity conference = conferenceEntity.get();
        if(((AdminEntity)identification).getOrganization().getId().equals(conference.getOrganization().getId())){
            for(PaperEntity paper: conference.getPapers())
                paperInfoList.add(new PaperInfo(paper));
            page = PageFactory.checkPageNumber(page);
            return new ListPage<>(paperInfoList, page, 10);
        }
        else
            throw new BusinessException(ExceptionInfo.NO_PERMISSION);
    }

    @Override
    public void handInRegistrationForm(OrganizationRegisterForm form, MultipartFile evidence) {
        List<AttachmentEntity> evidenceAttachments = null;
        try
        {
            if(evidence!=null)
            {
                evidenceAttachments = this.uploadFileService.uploadFiles(
                        Collections.singletonList(evidence), null,this.generateEvidenceUploadStrategy()
                );
            }
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
        RegisterFormEntity registerFormEntity = this.initRegisterFormEntity(form);
        if(evidence!=null)
            registerFormEntity.addAttachments(evidenceAttachments);
        this.registerFormRepository.save(registerFormEntity);
    }

    private UploadStrategy generateEvidenceUploadStrategy()
    {
        return new UploadStrategy() {
            @Override
            public String getStorePath(Object object) {
                return "/usr/share/registerForm";
            }
            @Override
            public List<String> getSupportTypeOfUploadFile() {
                return Arrays.asList("doc","docx","pdf","png","jpg");
            }
            @Override
            public ResourceType getSupportResourceType() {
                return null;
            }
        };
    }

    private UploadStrategy generateTemplateUploadStrategy() {
        return new UploadStrategy() {
            @Override
            public String getStorePath(Object object) {
                return "/usr/share/template";
            }
            @Override
            public List<String> getSupportTypeOfUploadFile() {
                return Arrays.asList("doc","docx","pdf","png","jpg");
            }
            @Override
            public ResourceType getSupportResourceType() {
                return ResourceType.Template;
            }
        };
    }

    private RegisterFormEntity initRegisterFormEntity(OrganizationRegisterForm form)
    {
        RegisterFormEntity registerFormEntity = new RegisterFormEntity();
        registerFormEntity.setCreditCode(form.getCreditCode());
        registerFormEntity.setLegalInfo(form.getLegalInfo());
        registerFormEntity.setOrganizationName(form.getOrganizationName());
        registerFormEntity.setMail(form.getMail());
        return registerFormEntity;
    }

    @Override
    public void setJudgeStatus(Integer paperId, PaperEntity.JudgeStatus judgeStatus, String opinion) {
        Optional<PaperEntity> paperEntityOptional = paperRepository.findById(paperId);
        if(!paperEntityOptional.isPresent())
            throw new BusinessException(PAPER_NOT_EXIST);
        PaperEntity judgedPaper = paperEntityOptional.get();
//        if(judgedPaper.getJudgeStatus().equals(PaperEntity.JudgeStatus.Qualified)||
//                judgedPaper.getJudgeStatus().equals(PaperEntity.JudgeStatus.Qualified_after_modified)||
//                judgedPaper.getJudgeStatus().equals(PaperEntity.JudgeStatus.Not_qualified))
//            throw new BusinessException(PAPER_JUDGED);
        judgedPaper.setJudgeStatus(judgeStatus);
        judgedPaper.setOpinion(opinion);
        paperRepository.save(judgedPaper);
    }

    @Override
    public void changeConferenceInfo(int id, ConferenceChangeInfo conferenceInfo) {
        Optional<ConferenceEntity> optional=conferenceRepository.findById(id);
        if(optional.isPresent()){
            ConferenceEntity entity=optional.get();
            String name=entity.getName();
            ConferenceEntity en=changeConference(entity,conferenceInfo);
            SendingEmailJob.changeMap(en);//更新map
            conferenceRepository.save(en);
            Set<PaperEntity> set=entity.getPapers();
            Iterator<PaperEntity> iter=set.iterator();
            while(iter.hasNext()){
                PaperEntity paperEntity=iter.next();
                UserEntity user=paperEntity.getFirstauthor();
                String emailTo=user.getEmail();
                if(emailTo!=null){//邮箱未填写不报错
                    emailsUtil.generateMessage(emailTo,"会议'"+name+"'信息更新",
                            "您投稿的《"+paperEntity.getTitle()+"》所属会议信息有更新,请及时查看");
                }
            }
        }
        else{
            throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        }
    }

    private ConferenceEntity changeConference(ConferenceEntity before,ConferenceChangeInfo info){
        String title=info.getTitle();
        if(title!=null)
            before.setName(title);
        String accommodationInfo=info.getAccommodationInfo();
        if(accommodationInfo!=null)
            before.setAccommodationInfo(accommodationInfo);
        Timestamp confBeginDate=info.getConfBeginDate();
        if(confBeginDate!=null)
            before.setConfBeginDate(confBeginDate);
        Timestamp confEndDate=info.getConfEndDate();
        if(confEndDate!=null)
            before.setConfEndDate(confEndDate);
        String contact=info.getContact();
        if(contact!=null)
            before.setContact(contact);
        String cost=info.getCost();
        if(cost!=null)
            before.setCost(cost);
        Timestamp ddlDate=info.getDdlDate();
        if(ddlDate!=null)
            before.setDdlDate(ddlDate);
        Timestamp informDate=info.getInformDate();
        if(informDate!=null)
            before.setInformDate(informDate);
        String introduction=info.getIntroduction();
        if(introduction!=null)
            before.setIntroduction(introduction);
        String schedule=info.getSchedule();
        if(schedule!=null)
            before.setSchedule(schedule);
        String requirement=info.getRequirement();
        if(requirement!=null)
            before.setRequirement(requirement);
        Timestamp registerDate=info.getRegisterDate();
        if(registerDate!=null)
            before.setRegisterDate(registerDate);
        Timestamp repostDdlDate=info.getRepostDdlDate();
        if(repostDdlDate!=null)
            before.setRepostDdlDate(repostDdlDate);
        Timestamp Ddl=before.getDdlDate();
        Timestamp register=before.getRegisterDate();
        Timestamp start=before.getConfBeginDate();
        Timestamp end=before.getConfEndDate();
        Timestamp repost=before.getRepostDdlDate();
        Timestamp inform=before.getInformDate();
        if(repost!=null){
            boolean checkDdl=Ddl.after(register)||Ddl.after(start)||Ddl.after(end)||Ddl.after(repost)||Ddl.after(inform);
            boolean checkRepost=repost.after(inform)||repost.after(register)||repost.after(start)||repost.after(end);
            boolean checkInform=inform.after(register)||inform.after(start)||inform.after(end);
            boolean checkRegister=register.after(start)||register.after(end);
            boolean checkStart=start.after(end);
            if(checkDdl||checkRepost||checkRegister||checkInform||checkStart){
                throw new BusinessException(ExceptionInfo.PARAMS_ILLEGAL);
            }
        }
        else{
            boolean checkDdl=Ddl.after(register)||Ddl.after(start)||Ddl.after(end)||Ddl.after(inform);
            boolean checkInform=inform.after(register)||inform.after(start)||inform.after(end);
            boolean checkRegister=register.after(start)||register.after(end);
            boolean checkStart=start.after(end);
            if(checkDdl||checkRegister||checkInform||checkStart){
                throw new BusinessException(ExceptionInfo.PARAMS_ILLEGAL);
            }
        }
        return before;
    }

    @Override
    public ListPage<SuperParticipantEntity> getParticipants(Integer conferenceId, Integer page) {
        Identification identification = authentificationService.getCurrentUser();
        Optional<ConferenceEntity> conferenceEntity = conferenceRepository.findById(conferenceId);
        if(!conferenceEntity.isPresent())
            throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        ConferenceEntity conference = conferenceEntity.get();
        List<SuperParticipantEntity> participantList = new ArrayList<>();
        if(identification.getRole().equals(Role.ROLE_ORGANIZER)) {
            if (((AdminEntity)identification).getOrganization().getId().equals(conference.getOrganization().getId())) {
                for (EntryFormEntity entryForm : conference.getEntryForms()) {
                    participantList.addAll(entryForm.getParticipants());
                }
            }
        }
        page = PageFactory.checkPageNumber(page);
        return new ListPage<>(participantList, page, 10);
    }

    @Override
    public void participantHandle(Integer entryId, EntryFormEntity.HandleStatus handleStatus) {
        Identification identification = authentificationService.getCurrentUser();
        Optional<EntryFormEntity> entryFormEntity = entryFormRepository.findById(entryId);
        if(!entryFormEntity.isPresent())
            throw new BusinessException(ENTRYFORM_NOT_EXIST);
        EntryFormEntity entryForm = entryFormEntity.get();
        if(identification.getRole().equals(Role.ROLE_ORGANIZER)) {
            if (((AdminEntity)identification).getOrganization().getId().equals(entryForm.getConference().getOrganization().getId())) {
//                if (entryForm.getHandleStatus().equals(EntryFormEntity.HandleStatus.Accepted) ||
//                        entryForm.getHandleStatus().equals(EntryFormEntity.HandleStatus.Rejected))
//                    throw new BusinessException(ENTRY_HANDLED);
                entryForm.setHandleStatus(handleStatus);
                entryFormRepository.save(entryForm);
                if(handleStatus.equals(EntryFormEntity.HandleStatus.Accepted))
                {
                    final String email = entryForm.getUser().getEmail();
                    if(email!=null&&!email.isEmpty())
                    {
                        final ConferenceEntity conferenceEntity = entryForm.getConference();
                        final String content = "您已参加"+conferenceEntity.getName()+"成功，请在"+conferenceEntity.getConfBeginDate().toString()+"准时参加！";
                        this.sendEmail(email,content);
                    }
                }
            }
            else
                throw new BusinessException(NO_PERMISSION);
        }
    }

    private Future<String> sendEmail(String emailUrl, String content)
    {
        if(emailUrl == null)
            throw new BusinessException(EMAIL_NULL);
        return this.emailsUtil.sendEmail(this.emailsUtil.generateMessage(emailUrl,"注册成功",content));
    }

    @Override
    public ListPage<EntryFormInfo> getEntryList(Integer conferenceId, Integer page) {
        Identification identification = authentificationService.getCurrentUser();
        Optional<ConferenceEntity> conferenceEntity = conferenceRepository.findById(conferenceId);
        if(!conferenceEntity.isPresent())
            throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        ConferenceEntity conference = conferenceEntity.get();
        List<EntryFormInfo> entryFormEntityList = new ArrayList<>();
        if(identification.getRole().equals(Role.ROLE_ORGANIZER)) {
            if (((AdminEntity)identification).getOrganization().getId().equals(conference.getOrganization().getId())){
                for (EntryFormEntity entry : conference.getEntryForms()) {
                    entryFormEntityList.add(new EntryFormInfo(entry));
                }
            }
        }
        page = PageFactory.checkPageNumber(page);
        return new ListPage<>(entryFormEntityList, page, 10);
    }

    @Override
    public ListPage<AdminEntity> getAccountByOrganizationIDandPage(long organizationID,int page){
        Optional<OrganizationEntity> optional= organizationRepository.findById(organizationID);
        if(!optional.isPresent())
            throw new BusinessException(ORGANIZATION_NOT_EXIST);
        OrganizationEntity organizationEntity=new OrganizationEntity();
        organizationEntity=optional.get();
        List<AdminEntity> adminEntities=new ArrayList<>(organizationEntity.getAdmins());
        page=PageFactory.checkPageNumber(page);
        ListPage<AdminEntity> adminEntityListPage=new ListPage<AdminEntity>(adminEntities,page,10);
        return adminEntityListPage;
    }

    @Override
    public void addAdmin(UserNameAndPassword userNameAndPassword){
        AdminEntity adminEntity=new AdminEntity();
        adminEntity.setUserName(userNameAndPassword.getUserName());
        adminEntity.setPassword(userNameAndPassword.getPassword());
        OrganizationEntity temp=((AdminEntity)this.authentificationService.getCurrentUser()).getOrganization();
        adminEntity.setOrganization(((AdminEntity)this.authentificationService.getCurrentUser()).getOrganization());
        adminRepository.save(adminEntity);
}

    @Override
    public void setAdmin(long id,UserNameAndPassword userNameAndPassword){
        Optional<AdminEntity> optional=adminRepository.findById(id);
        if(!optional.isPresent())
            throw new BusinessException(ADMIN_NOT_EXIST);
        AdminEntity adminEntity=new AdminEntity();
        adminEntity=optional.get();
        adminEntity.setUserName(userNameAndPassword.getUserName());
        adminEntity.setPassword(userNameAndPassword.getPassword());
        adminRepository.save(adminEntity);
    }

    @Override
    public void deleteAdmin(long id){
        Optional<AdminEntity> optional=adminRepository.findById(id);
        if(!optional.isPresent())
            throw new BusinessException(ADMIN_NOT_EXIST);
        AdminEntity adminEntity=new AdminEntity();
        adminEntity=optional.get();
        adminRepository.delete(adminEntity);
    }

    @Override
    public void deleteConference(Integer conferenceId) {
        Optional<ConferenceEntity> conferenceEntityOptional = conferenceRepository.findById(conferenceId);
        if(!conferenceEntityOptional.isPresent())
            throw new BusinessException(ExceptionInfo.CONFERENCE_NOT_EXIST);
        ConferenceEntity conference = conferenceEntityOptional.get();

        Set<PaperEntity> papers = conference.getPapers();
        Set<EntryFormEntity> entryForms = conference.getEntryForms();
        if(papers !=null &&!papers.isEmpty()||entryForms !=null&&!entryForms.isEmpty())
            throw new BusinessException(CONFERENCE_DELETE_NOT_ALLOWED);
        CollectionClassificationEntity collection =
                this.collectionClassificationRepository.findByConferencesContains(conference);
        if(collection!=null)
        {
            collection.removeConference(conference);
            this.collectionClassificationRepository.save(collection);
        }

        Identification currentUser = this.authentificationService.getCurrentUser();
        if(!currentUser.getRole().equals(Role.ROLE_ORGANIZER)|| !(currentUser instanceof AdminEntity))
            throw new BusinessException(PERMISSION_DENIED);

        AdminEntity admin = (AdminEntity)currentUser;
        if(!admin.getOrganization().equals(conference.getOrganization()))
            throw new BusinessException(PERMISSION_DENIED);

        this.conferenceRepository.delete(conference);
        SendingEmailJob.deleteMap(conference);//更新map
    }

    /**
     * @param conferenceId 会议Id
     */
    @Override
    public ResponseEntity<FileSystemResource> getExcelOfConference(int conferenceId) {
        Optional<ConferenceEntity> optional = this.conferenceRepository.findById(conferenceId);
        if(!optional.isPresent())
            throw new BusinessException(CONFERENCE_NOT_EXIST);
        ConferenceEntity conferenceEntity = optional.get();

        Identification currentUser = this.authentificationService.getCurrentUser();
        if(!currentUser.getRole().equals(Role.ROLE_ORGANIZER)||!(currentUser instanceof AdminEntity))
            throw new BusinessException(PERMISSION_DENIED);

        AdminEntity admin = (AdminEntity) currentUser;
        if(!admin.getOrganization().equals(conferenceEntity.getOrganization()))
            throw new BusinessException(PERMISSION_DENIED);

        try {
            String url = this.excelGenerator.generateExcel(conferenceId);
            return this.resourceDownloadService.download(url, MediaType.parseMediaType("application/x-xls"));
        }
        catch (IOException e) {
            e.printStackTrace();
            throw new BusinessException(FILE_DOWNLOAD_ERROR);
        }
    }

    //private
}


