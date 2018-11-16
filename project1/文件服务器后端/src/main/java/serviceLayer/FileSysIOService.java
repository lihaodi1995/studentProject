package serviceLayer;

import dataAccessLayer.fileSysDataDAO.AsyncFileDAOIF;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;

@Service
public class FileSysIOService {
    @Resource
    private AsyncFileDAOIF asyncFileDAOIF;

    public AsyncFileDAOIF getAsyncFileDAOIF() {
        return asyncFileDAOIF;
    }

    public void setAsyncFileDAOIF(AsyncFileDAOIF asyncFileDAOIF) {
        this.asyncFileDAOIF = asyncFileDAOIF;
    }

    public String asyncFileIO(Object request) {
        String result = asyncFileDAOIF.storeFileToGetAbsPath(request);
        return result;
    }

}
