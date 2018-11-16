package dataAccessLayer.util;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class QuickTimeTool {
    public static SimpleDateFormat simpleDateFormat = new SimpleDateFormat(R.TIME_STANDERD_FORMAT);

    public static Date getCurrentTimeDate() {
        return new Date();
//        return simpleDateFormat.format(new Date());
    }

    public static String getCurrentTimeString() {
        return simpleDateFormat.format(new Date());
    }

    public static String getStringFromDate(Date date) {
        return simpleDateFormat.format(date);
    }

    public static Date getDateFromString(String dateString) {
        try {
            return simpleDateFormat.parse(dateString);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return null;
    }
}
