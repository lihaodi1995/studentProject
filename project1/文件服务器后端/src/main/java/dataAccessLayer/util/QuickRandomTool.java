package dataAccessLayer.util;

import java.util.Random;

//本类用静态方法实现快速的随机资源的生成
public class QuickRandomTool {

    public static String quickCheckCode() {
        Random random = new Random();
        StringBuilder stringBuilder = new StringBuilder();
        for (int i = 0; i < 4; i++) {
            stringBuilder.append(random.nextInt(10));
        }
        return stringBuilder.toString();
    }
}
