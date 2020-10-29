package com.example.droneapp.util;

import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public final class DateUtils {
    public static String getFormatDateAndTimeString(long seconds) {
        // 요일 정보를 가져오기 위한 포맷
        Calendar calendar = Calendar.getInstance(Locale.KOREA);
        calendar.setTime(new Date(seconds));
        return String.format("%d년 %02d월 %02d일",
                calendar.get(Calendar.YEAR),
                calendar.get(Calendar.MONTH) + 1,
                calendar.get(Calendar.DAY_OF_MONTH),
                calendar.get(Calendar.HOUR_OF_DAY),
                calendar.get(Calendar.MINUTE)
        );
    }
}
