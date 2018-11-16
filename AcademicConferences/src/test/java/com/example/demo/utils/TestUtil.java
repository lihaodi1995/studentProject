package com.example.demo.utils;

import org.mockito.Mockito;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

public class TestUtil {
    public static MvcResult testJsonRequest(@NotNull MockMvc mvc, @NotNull String url, @NotNull String content,
                                            @Size(min = 1) ResultMatcher[]expects)throws Exception
    {
        ResultActions resultActions =mvc.perform(MockMvcRequestBuilders.post(url)
                .contentType(MediaType.APPLICATION_JSON)
                .content(content));
        for(ResultMatcher matcher:expects)
            resultActions.andExpect(matcher);
        resultActions.andExpect(status().isOk());
        resultActions.andDo(MockMvcResultHandlers.print());
        return resultActions.andReturn();
    }

    public static MvcResult testFileRequest(@NotNull MockMvc mvc, @NotNull String url, MockMultipartFile multipartFile, @NotNull String content,
                                            ResultMatcher[]expects)throws Exception
    {
        ResultActions resultActions =mvc.perform(MockMvcRequestBuilders.fileUpload(url)
                .file(multipartFile)
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .content(content));
        for(ResultMatcher matcher:expects)
            resultActions.andExpect(matcher);
        resultActions.andExpect(status().isOk());
        resultActions.andDo(MockMvcResultHandlers.print());
        return resultActions.andReturn();
    }
    public static <T>void setExpectResponseOfMethod(T methodCall ,T expect)
    {
        Mockito.when(methodCall).thenReturn(expect);
    }

    public static MockMultipartFile generateMultiPartFile(String filePath)
    {
        try(InputStream inputStream =new FileInputStream(filePath))
        {
            byte[] data =readInputStream(inputStream);
            return new MockMultipartFile("image", filePath, "image/jpeg", data);
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        return null;
    }

    private static byte[] readInputStream(InputStream inStream) throws Exception {
        ByteArrayOutputStream outStream = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int len;
        while ((len = inStream.read(buffer)) != -1) {
            outStream.write(buffer, 0, len);
        }
        inStream.close();
        return outStream.toByteArray();
    }
}
