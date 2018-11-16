package dataAccessLayer.util;

import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

import javax.servlet.http.HttpServletRequest;
import java.io.*;
import java.util.LinkedList;


/**
 * Created by luo on 17-7-23.
 */
/*
 * this class  play a role as file_get_contents(), file_write_contents() in phpAPI
 * it will be very simple and stupid
 * */
public class QuickFileIOTool {
    //this relative string can be modified to "" and so on to adapted to the real situation it runs in.
    public static void main(String[] args) {
    }

    public static void writeStringToFile(String content, String fileString) {
//if file not exist , create it
        File f = new File(fileString);
        try {
            if (!f.exists()) {
                f.createNewFile();
            }
            //file exist now
            writeStringToFile(content, f);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void writeStringToFile(String content, File f) {

        try {
            FileOutputStream fos = new FileOutputStream(f);
            fos.write(content.getBytes());
            fos.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String getContentsFromFile(String fString) {
        return getContentsFromFile(new File(fString));
    }

    public static String getContentsFromFile(File f) {
        StringBuilder sb = new StringBuilder();
        try {
            FileReader fr = new FileReader(f);
            BufferedReader br = new BufferedReader(fr);
            String s = null;
            while ((s = br.readLine()) != null) {
                sb.append(s);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return sb.toString();
    }

    public static void joinStreams(InputStream in, OutputStream out, int bufferSize) {
        BufferedInputStream bufferedInputStream = new BufferedInputStream(in);
        byte[] buffer = new byte[bufferSize];
        BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(out);
        int readNum = 0;
        try {
            while ((readNum = bufferedInputStream.read(buffer)) > -1) {
                bufferedOutputStream.write(buffer, 0, readNum);
            }
            bufferedOutputStream.close();
            bufferedInputStream.close();
            out.close();
            in.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void joinStreams(InputStream in, OutputStream out) {
        joinStreams(in, out, 4096);
    }

    public static void joinStreams(InputStream in, String fileUrl) {
        File file = new File(fileUrl);
        try {
            file.createNewFile();
            OutputStream outputStream = new FileOutputStream(file);
            joinStreams(in, outputStream);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static LinkedList<org.apache.commons.fileupload.FileItem> incomeFiles(HttpServletRequest request) {
        DiskFileItemFactory diskFileItemFactory = new DiskFileItemFactory();
        ServletFileUpload servletFileUpload = new ServletFileUpload(diskFileItemFactory);
        try {
            return new LinkedList<>(servletFileUpload.parseRequest(request));
        } catch (FileUploadException e) {
            e.printStackTrace();
            return new LinkedList<>();
        }
    }


}
