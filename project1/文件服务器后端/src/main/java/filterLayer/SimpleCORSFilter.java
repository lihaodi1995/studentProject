package filterLayer;


import org.springframework.stereotype.Component;
import userController.utils.R;
import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@Component
public class SimpleCORSFilter implements Filter {

    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) throws IOException, ServletException {
        HttpServletResponse response = (HttpServletResponse) res;


        response.setCharacterEncoding(userController.utils.R.UTF8);


        response.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE");
        response.setHeader("Access-Control-Max-Age", "3600");
        response.setHeader("Access-Control-Allow-Headers", "x-requested-with" + "," + R.HEADER_KEY_CONTENT_TYPE);
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.addHeader(R.HEADER_KEY_CONTENT_TYPE, R.HEADER_VALUE_FORM_URL_ENCODE);



        HttpServletRequest request = (HttpServletRequest) req;
        request.setCharacterEncoding(userController.utils.R.UTF8);

        if (request.getMethod().equals("OPTIONS")) {

            response.setStatus(200);
            response.getWriter().flush();
        } else {

            chain.doFilter(req, res);
        }
    }

    public void init(FilterConfig filterConfig) {
    }

    public void destroy() {
    }

}