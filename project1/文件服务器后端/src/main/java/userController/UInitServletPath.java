package userController;

import dataAccessLayer.util.R;
import org.springframework.web.context.ServletContextAware;

import javax.servlet.ServletContext;

public class UInitServletPath implements ServletContextAware {
    @Override
    public void setServletContext(ServletContext servletContext) {
        String rootPath= servletContext.getRealPath("/");
        R.PATH_ABS_WEBROOT_PATH=rootPath;
    }
}
