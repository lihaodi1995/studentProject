package com.example.demo.component;

import com.example.demo.model.entity.ConferenceEntity;
import org.apache.log4j.Logger;
import org.quartz.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.context.support.SpringBeanAutowiringSupport;

import javax.mail.internet.MimeMessage;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * @Author : 陈瀚清
 * @Description: 定时任务
 * @Date created at 2018/7/4
 **/
@DisallowConcurrentExecution//多个任务间不会同时执行
@PersistJobDataAfterExecution//保存在JobDataMap传递的参数
public class SendingEmailJob implements Job {

    private final Logger logger= Logger.getLogger(SendingEmailJob.class);
    private final SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    public static Map<String,Set<ConferenceEntity>> map=null;//全局变量
    public static final Queue<MimeMessage> queue= new ConcurrentLinkedQueue<>();//消息队列

    @Autowired
    private EmailsUtil emailsUtil;

    @Override
    public void execute(JobExecutionContext jobExecutionContext) {
        try {
            SpringBeanAutowiringSupport.processInjectionBasedOnCurrentContext(this);
            Date date = new Date(System.currentTimeMillis());
            String str = format.format(date);
            logger.info("定时任务:" + str);
            if (map == null) {
                JobDataMap jobDataMap = jobExecutionContext.getJobDetail().getJobDataMap();
                if (jobDataMap != null) {
                    map = (Map) jobDataMap.getWrappedMap();
                }
            }
            long now = System.currentTimeMillis();
            for (Map.Entry<String, Set<ConferenceEntity>> entry : map.entrySet()) {
                String email = entry.getKey();
                Set<ConferenceEntity> list = entry.getValue();
                Iterator<ConferenceEntity> iter = list.iterator();
                if (list != null) {
                    while (iter.hasNext()) {
                        ConferenceEntity detail = iter.next();
                        long ddl = detail.getDdlDate().getTime() - now;
                        long register = detail.getRegisterDate().getTime() - now;
                        String title = detail.getName();
                        if (ddl > 0 && ddl <= 1800000) {
                            MimeMessage mailMessage = emailsUtil.generateMessage(
                                    email, "截稿日期提醒",
                                    "距离会议'" + title + "'的截稿日期不到半小时，请及时投稿"
                            );
                            emailsUtil.sendEmail(mailMessage);
                        }
                        if (register > 0 && register <= 1800000) {
                            MimeMessage mailMessage = emailsUtil.generateMessage(
                                    email, "注册截止日期提醒",
                                    "距离会议'" + title + "'的注册截止日期不到半小时，请及时注册"
                            );
                            emailsUtil.sendEmail(mailMessage);
                        }
                    }
                }
            }
            sendMessage();
        }catch(Exception e){
            e.printStackTrace();
            logger.warn("job启动异常："+e.getMessage());
        }
    }

    public static void changeMap(String email,Set<ConferenceEntity> list){
        if(map==null){
            map=new HashMap<>();
        }
        if(list!=null){
            map.put(email,list);
        }
        else
            map.remove(email);
    }

    public static void changeMap(ConferenceEntity entity){
        if(map!=null){
            for(Map.Entry<String,Set<ConferenceEntity>> entry:map.entrySet()){
                String email=entry.getKey();
                Set<ConferenceEntity> set=entry.getValue();
                Iterator<ConferenceEntity> iter=set.iterator();
                while(iter.hasNext()){
                    ConferenceEntity en=iter.next();
                    if(en.getId()==entity.getId()){
                        set.remove(en);
                        set.add(entity);
                        break;
                    }
                }
            }
        }
    }

    public static void deleteMap(ConferenceEntity entity){
        if(map==null){
            map=new HashMap<>();
            return;
        }
        for(Map.Entry<String,Set<ConferenceEntity>> entry:map.entrySet()){
            String email=entry.getKey();
            Set<ConferenceEntity> set=entry.getValue();
            if(set.contains(entity))
                set.remove(entity);
        }
    }

    public static void addMessage(MimeMessage message){
        synchronized (queue)
        {
            queue.add(message);
        }
    }

    private void sendMessage(){
        List<MimeMessage> msgList = new ArrayList<>(queue.size());
        while(!queue.isEmpty())
        {
            msgList.add(queue.poll());
        }
        for(MimeMessage x:msgList)
            emailsUtil.sendEmail(x);
    }
}
