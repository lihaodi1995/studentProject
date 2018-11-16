package com.example.demo.controller;

import com.example.demo.component.EmailsUtil;
import com.example.demo.model.request.OrganizationRegisterForm;
import com.example.demo.utils.BaseRequestEntity;
import com.example.demo.utils.ConvertUtil;
import com.example.demo.utils.TestUtil;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mail.MailSendException;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.WebApplicationContext;

import static org.junit.Assert.*;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/2 13:34
 **/
@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
@WebAppConfiguration
public class OrganizationControllerTest {
    @Autowired
    private WebApplicationContext context;
    @Autowired
    private MockMvc mvc ;

    @Before
    public void setUp(){
        mvc = MockMvcBuilders.webAppContextSetup(context)
                .build();
    }

    @Autowired
    private EmailsUtil emailsUtil;

    @After
    public void tearDown()  {

    }

    @Test
    public void emailTest()
    {
         emailsUtil.sendEmail(emailsUtil.generateMessage("1@qq.com","test","test"));
    }

    @Test
    @Transactional
    @Rollback
    public void organizationRegistration() throws Exception{
        final String filePath="C:\\Users\\叶明林\\Desktop\\11.jpg";

        final String testUrl="http://localhost:8080/api/organization/registration";

        MockMultipartFile file = TestUtil.generateMultiPartFile(filePath);

        String result=TestUtil.testFileRequest(this.mvc,testUrl,
                file,
                this.generateRequestJsonByToken(),
                new ResultMatcher[]{}).getResponse().getContentAsString();

        System.out.println(result);
//        this.resultPath=getUploadPath(result);
//
//        deleteUploadFile();
    }

    private String generateRequestJsonByToken()
    {
        OrganizationRegisterForm form = new OrganizationRegisterForm();
        form.setMail("942481251@qq.com");
        form.setOrganizationName("test");
        return ConvertUtil.convertObjectToJSON(form);
    }
}