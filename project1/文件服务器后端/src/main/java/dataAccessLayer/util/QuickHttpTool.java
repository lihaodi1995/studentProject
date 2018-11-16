package dataAccessLayer.util;



import java.io.*;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;

public class QuickHttpTool {
    public static String sendGet(String request) {
        try {
            URL url = new URL(request);

            URLConnection urlConnection = url.openConnection();
            urlConnection.connect();
            InputStream inputStream = urlConnection.getInputStream();
            return getStringFromStream(inputStream);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static String getStringFromStream(InputStream in) {
        BufferedReader bufferedInputStream = new BufferedReader(new InputStreamReader(in));
        StringBuilder stringBuilder = new StringBuilder();
        String aLine = "";
        try {
            while ((aLine = bufferedInputStream.readLine()) != null) {
                stringBuilder.append(aLine);
            }
            bufferedInputStream.close();
            in.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return stringBuilder.toString();
    }

    //本方法自动将值参数转码utf8，你不要转码再给我
    public static String generateGetString(String baseUrl, String[] keys, String[] values) {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append(baseUrl);
        int len = keys.length;
        if (values.length != len) {
            return null;
        }
        for (int i = 0; i < len; i++) {
            if (i == 0) {
                stringBuilder.append("?");
            } else {
                stringBuilder.append("&");
            }
            try {
                stringBuilder.append(keys[i]).append("=").append(URLEncoder.encode(values[i], "utf-8"));
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
        return stringBuilder.toString();
    }

}
