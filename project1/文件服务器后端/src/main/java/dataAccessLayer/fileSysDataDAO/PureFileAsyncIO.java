package dataAccessLayer.fileSysDataDAO;

import dataAccessLayer.util.QuickFileIOTool;
import dataAccessLayer.util.R;
import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.apache.commons.fileupload.servlet.ServletRequestContext;
import org.apache.commons.lang.math.RandomUtils;
import org.springframework.stereotype.Repository;

import javax.servlet.http.HttpServletRequest;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

@Repository
public class PureFileAsyncIO implements AsyncFileDAOIF {
    @Override
    public String storeFileToGetAbsPath(Object request) {
        HttpServletRequest requestIN=(HttpServletRequest)request;
        String absRootPath = new String(R.PATH_ABS_WEBROOT_PATH);
        String picNameFileName = absRootPath.concat(R.PATH_RELA_PICS);
        String resultString = new String(R.PATH_HOST_URL_PREFIX);
        resultString += R.PATH_RELA_PICS;
        DiskFileItemFactory factory = new DiskFileItemFactory();

        ServletFileUpload upload = new ServletFileUpload(factory);

        //判断提交表单的类型是否为multipart/form-data

//        if (!ServletFileUpload.isMultipartContent(request)) {
//            return R.PATH_404_PIC_URL;
//        }
        try {
            List list = upload.parseRequest(requestIN);
            Iterator it = list.iterator();

            while (it.hasNext()) {
                FileItem item = (FileItem) it.next();//每一个item就代表一个表单输出项

                if (item.isFormField())//判断input是否为普通表单输入项
                    continue;
                String filename = item.getName();
                String[] strs=filename.split("\\.");
                if(strs.length>1){
                    filename="."+strs[strs.length-1];
                }else {
                    filename=strs[0];
                }
                //得到上传文件要写入的目录
                String randNameString = R.generateRandomString();
                randNameString += filename;

                //set return string
                resultString += randNameString;
                picNameFileName += randNameString;
//            String path=picNameFileName.concat();
                //根据目录和文件创建输出流
                FileOutputStream out = new FileOutputStream(picNameFileName);
                InputStream in = item.getInputStream();
                QuickFileIOTool.joinStreams(in, out);
                return resultString;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return R.PATH_404_PIC_URL;
    }

    public void setToMul(HttpServletRequest request){
       ServletRequestContext requestContext=  new ServletRequestContext(request);
//       requestContext.
    }
//    public String getAfterFix(String s){
//
//    }

}
