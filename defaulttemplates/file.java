/**
 * $USER
 * $SRCFILE
 */

import java.io.*;
import java.util.*;

public class $PROB {
    static BufferedReader cin, in;
    static PrintWriter out;
    static StringTokenizer tk;
    public static String token () {
        try {
            while (!tk.hasMoreTokens())
                tk = new StringTokenizer(in.readLine());
            return tk.nextToken();
        }
        catch (Exception e) {
        }
        return null;
    }
    public static int gInt () {
        return Integer.parseInt(token());
    }
    public static long gLong () {
        return Long.parseLong(token());
    }
    public static double gDouble () {
        return Double.parseDouble(token());
    }
    public static void init () throws IOException {
        cin = new BufferedReader(new InputStreamReader(System.in));
        in = new BufferedReader(new FileReader("$INFILE"));
        tk = new StringTokenizer("");
        out = new PrintWriter(new BufferedWriter(new FileWriter("$OUTFILE")));
    }
    public static void quit () throws IOException {
        System.out.flush();
        out.close();
        System.exit(0);
    }
    public static void main (String [] args) throws IOException {
        init();
        quit();
    }
}