package userController;

import dataAccessLayer.VGeneralItemOperation;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import serviceLayer.FileSysIOService;
import userController.utils.R;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

//@CrossOrigin(origins = "*",maxAge = 3600)
@RequestMapping("/file")
@Controller
public class UAsyncIOController {
    @Resource
    private FileSysIOService fileSysIOService;

    public FileSysIOService getFileSysIOService() {
        return fileSysIOService;
    }

    public void setFileSysIOService(FileSysIOService fileSysIOService) {
        this.fileSysIOService = fileSysIOService;
    }

    @RequestMapping("/upload.do")
    public void upoloadFile(HttpServletRequest file,HttpServletResponse response) {
//        response.addHeader("Access-Control-Allow-Origin", "*");
        String resultPath = fileSysIOService.asyncFileIO(file);
        VGeneralItemOperation result = new VGeneralItemOperation();
        result.setValue(resultPath);
        //  QuickIOToJson.sendOutputJSON(result,response);
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("{\"link\":\"").append(resultPath).append("\"}");
        try {

            response.getWriter().write(stringBuilder.toString());
            response.getWriter().flush();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }




    @RequestMapping("/alive.do")
    public  void alive(HttpServletRequest request, HttpServletResponse response){
        try {
            response.getWriter().append("{\"alive\":\"yes\"}").flush();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }


}
