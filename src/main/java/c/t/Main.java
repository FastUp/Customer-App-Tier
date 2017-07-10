package c.t;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by sachi_000 on 6/26/2017.
 */
public class Main {

    public static void main(String[] args) {
        String regex  = "^(?=\\d)([^ ]*)(?:\\s+)(?=.*)([^ ]*)(?:\\s+)(DEBUG|INFO|ERROR)(?:\\s+)(?=.*)([^ ]*)(?:\\s+\\-\\s+)([\\S\\s]+?)(?=\\n)\\Z";
        final Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE);
        final Matcher matcher = pattern.matcher("16:33:09.716 [qtp128893786-12] DEBUG com.api.JerseyCustomLoggingFilter - HTTP RESPONSE : Header: {} - Entity: null\n" +
                "16:33:39.614 [qtp128893786-17] DEBUG com.api.JerseyCustomLoggingFilter - HTTP REQUEST : User: unknown - Path: HealthCheck - Method: GET - Header: {Connection=[close], User-Agent=[ELB-HealthChecker/2.0], Host=[10.0.120.205:8080]} - Entity:\n" +
                "\n" +
                "16:33:39.614 [qtp128893786-17] DEBUG com.api.JerseyCustomLoggingFilter - HTTP RESPONSE : Header: {} - Entity: null\n" +
                "16:33:39.721 [qtp128893786-16] DEBUG com.api.JerseyCustomLoggingFilter - HTTP REQUEST : User: unknown - Path: HealthCheck - Method: GET - Header: {Connection=[close], User-Agent=[ELB-HealthChecker/2.0], Host=[10.0.10.20:8080]} - Entity:\n" +
                "\n" +
                "16:33:39.721 [qtp128893786-16] DEBUG com.api.JerseyCustomLoggingFilter - HTTP RESPONSE : Header: {} - Entity: null\n" +
                "16:33:45.287 [qtp128893786-11] DEBUG com.api.JerseyCustomLoggingFilter - HTTP RESPONSE : Header: {Allow=[POST,OPTIONS]} - Entity: null\n" +
                "16:33:55.878 [qtp128893786-14] DEBUG com.api.JerseyCustomLoggingFilter - HTTP REQUEST : User: unknown - Path: tokens/dev - Method: POST - Header: {Cache-Control=[no-cache], Accept=[*/*], X-Forwarded-Proto=[https], User-Agent=[PostmanRuntime/6.1.6], X-Forwarded-For=[47.190.19.41], Host=[api.io], Postman-Token=[9d2242f0-9a35-4e50-a493-5c2a6277fd3c], Accept-Encoding=[gzip, deflate], Content-Length=[42], X-Forwarded-Port=[443], X-Amzn-Trace-Id=[Root=1-593acdf3-29f5a3fe2467cb793c3c23d4], Content-Type=[application/json]} - Entity: {^M\n" +
                "        \"email\": \"UTC\",^M\n" +
                "        \"password\": \"UTC\"^M\n" +
                "}");
        System.out.println();

    }
}
