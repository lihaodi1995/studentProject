package com.example.demo.component;

import com.example.demo.exception.BusinessException;
import com.example.demo.jpa.ConferenceRepository;
import com.example.demo.model.entity.ConferenceEntity;
import com.example.demo.model.entity.PaperEntity;
import com.example.demo.utils.SystemUtil;
import org.apache.poi.hssf.usermodel.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.*;
import java.util.*;

import static com.example.demo.exception.ExceptionInfo.CONFERENCE_NOT_EXIST;
import static com.example.demo.exception.ExceptionInfo.UPLOAD_SAVE_ERROR;

/**
 * @Reference : https://blog.csdn.net/panpan96/article/details/76566475
 * @Description: 投稿情况Excel
 * @Date created at 2018/7/6 9:01
 **/
@Component
public class ExcelGenerator {
    private final ConferenceRepository conferenceRepository;

    @Autowired
    public ExcelGenerator(ConferenceRepository conferenceRepository) {
        this.conferenceRepository = conferenceRepository;
    }

    /**
     * 生成某个会议投稿情况的excel汇总表
     * @param conferenceId 会议Id
     * @return 生成的excel保存地址
     * @throws IOException excel生成错误，文件操作出错
     */
    public String generateExcel(int conferenceId)throws IOException
    {
        //导出的Excel头部
        String[] headers = { "投稿编号", "作者", "题目", "单位","摘要","第一作者邮箱地址"};

        Optional<ConferenceEntity> optional = this.conferenceRepository.findById(conferenceId);
        if(!optional.isPresent())
            throw new BusinessException(CONFERENCE_NOT_EXIST);
        ConferenceEntity conferenceEntity = optional.get();

        Set<PaperEntity> papers = conferenceEntity.getPapers();

        // 声明一个工作薄
        HSSFWorkbook workbook = new HSSFWorkbook();
        // 生成一个表格
        HSSFSheet sheet = workbook.createSheet();
        HSSFRow row = sheet.createRow(0);
        for (int i = 0; i < headers.length; i++) {
            HSSFCell cell = row.createCell(i);
            HSSFRichTextString text = new HSSFRichTextString(headers[i]);
            cell.setCellValue(text);
        }
        //遍历集合数据，产生数据行
        if(papers!=null)
        {
            int index = 1;
            for(PaperEntity paperEntity:papers)
            {
                row = sheet.createRow(index);

                List<String> data = new ArrayList<>(headers.length);
                //投稿编号
                data.add(paperEntity.getId().toString());
                //作者
                StringBuilder authorNames=new StringBuilder();
                authorNames.append(paperEntity.getFirstauthor().getName());
                String authors = paperEntity.getAuthors();
                if(authors!=null&&!authors.isEmpty())
                {
                    authorNames.append(",");
                    authorNames.append(authors);
                }
                data.add(authorNames.toString());
                //题目
                data.add(paperEntity.getTitle());
                //单位
                data.add(paperEntity.getInstitution());
                //摘要
                data.add(paperEntity.getAbstractinfo());
                //第一作者邮箱地址
                data.add(paperEntity.getFirstauthor().getEmail());

                for(int i = 0;i<data.size();i++)
                {
                    HSSFCell cell = row.createCell(i);
                    HSSFRichTextString richString = new HSSFRichTextString(data.get(i));
//                    HSSFFont font3 = workbook.createFont();
//                    font3.setColor(HSSFColor.BLUE.index);//定义Excel数据颜色
//                    richString.applyFont(font3);
                    cell.setCellValue(richString);
                }

                index++;
            }
        }
        SystemUtil systemUtil = new SystemUtil("D:"+File.separator+"excel","/user/share/excel");

        File file = new File(systemUtil.getUrl());
        if(!file.exists()&&!file.mkdirs())
            throw new BusinessException(UPLOAD_SAVE_ERROR);
        String storagePath = systemUtil.getUrl()+File.separator+conferenceId+".xls";
        try (OutputStream outputStream = new FileOutputStream(storagePath))
        {
            workbook.write(outputStream);
            outputStream.flush();
        }
        return storagePath;
    }
}
