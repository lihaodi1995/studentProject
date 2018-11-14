package com.rua.homeworkController;
import java.io.File;

public class readAllFileNameTest {

    /**
     * 
     * @author zdz8207
     */
    public static void main(String[] args) {
        getFileName();
    }

    public static void getFileName() {
        String path = "E:/workspace/mooc/doc"; // 路径
        File f = new File(path);
        if (!f.exists()) {
            System.out.println(path + " not exists");
            return;
        }

        File fa[] = f.listFiles();
        for (int i = 0; i < fa.length; i++) {
            File fs = fa[i];
            if (fs.isDirectory()) {
                System.out.println(fs.getName() + " [目录]");
            } else {
                System.out.println(fs.getName());
            }
        }
    }
}