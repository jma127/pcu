/**
 * $USER
 * $SRCFILE
 */

import java.io.*;
import java.util.*;

public class $PROB {
    static BufferedReader cin;
    static StringTokenizer tk;
    public static String token () throws IOException {
        try {
            while (!tk.hasMoreTokens())
                tk = new StringTokenizer(cin.readLine());
            return tk.nextToken();
        }
        catch (Exception e) {
        }
        return null;
    }
    public static int gInt () throws IOException {
        return Integer.parseInt(token());
    }
    public static long gLong () throws IOException {
        return Long.parseLong(token());
    }
    public static double gDouble () throws IOException {
        return Double.parseDouble(token());
    }
    public static void init () {
        cin = new BufferedReader(new InputStreamReader(System.in));
        tk = new StringTokenizer("");
    }
    public static void quit () throws IOException {
        System.out.flush();
        System.exit(0);
    }
    public static void main (String [] args) throws IOException {
        init();
        quit();
    }
}
