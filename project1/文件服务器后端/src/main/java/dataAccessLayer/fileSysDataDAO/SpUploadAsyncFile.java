package dataAccessLayer.fileSysDataDAO;

import dataAccessLayer.util.QuickFileIOTool;
import dataAccessLayer.util.R;
import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.springframework.stereotype.Repository;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.Iterator;
import java.util.List;

//@Repository
public class SpUploadAsyncFile implements AsyncFileDAOIF {
    @Override
    public String storeFileToGetAbsPath(Object file) {
        MultipartFile mf=(MultipartFile) file;


        String absRootPath = new String(R.PATH_ABS_WEBROOT_PATH);
        String picNameFileName = absRootPath.concat(R.PATH_RELA_PICS);
        String resultString = new String(R.PATH_HOST_URL_PREFIX);
        resultString += R.PATH_RELA_PICS;

        String orgFileName=mf.getOriginalFilename();
        orgFileName=R.generateRandomString()+orgFileName;

        try {

                resultString += orgFileName;
                picNameFileName += orgFileName;
                FileOutputStream out = new FileOutputStream(picNameFileName);
                InputStream in = mf.getInputStream();
                QuickFileIOTool.joinStreams(in, out);
                return resultString;

        } catch (Exception e) {
            e.printStackTrace();
        }
        return R.PATH_404_PIC_URL;
    }
}
