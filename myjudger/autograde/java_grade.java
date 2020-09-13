import com.google.gson.Gson;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.Reader;
import java.io.Writer;
import java.io.IOException;
/*
javac -cp algs4.jar:gson.jar myjava_grade.java Solution.java
java -cp gson.jar:algs4.jar:. myjava_grade {casename}
*/

public class java_grade {
    public static void main(String[] args) {
        Gson gson = new Gson();
        long clk_s;
	long timeout_limit = 800;

	// read input
        try (Reader reader = new FileReader(args[0] + ".in")) {
            Case cases = gson.fromJson(reader, Case.class);
            int casenum = cases.data.length;

	    // init output
            Output output = new Output(casenum);
            for(int sample=0 ; sample<casenum ; ++sample){
                output.status[sample] = "NA";
                output.time[sample] = 0;
            }    

	    // per sample
            for(int sample=0 ; sample<casenum ; ++sample) {
                try{
                    clk_s = System.currentTimeMillis();
                    int out = new Solution().test(cases.data[sample].a,cases.data[sample].b);
                    output.time[sample] = System.currentTimeMillis() - clk_s;

                    if (out == cases.data[sample].ans) {
                        output.status[sample] = "AC";
                    }
                    else{
                        output.status[sample] = "WA";
                    }

                    if (output.time[sample] > timeout_limit) {
                        output.status[sample] = "TLE";
                    }
                }
                catch (Exception e){
                     output.status[sample] = "RE";
                }
	    }

	    // write to output
	    Writer fout = new FileWriter(args[0] + ".out");
            gson.toJson(output, fout);  
	    fout.flush();
	    fout.close();
            System.out.println(gson.toJson(output));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class Output{
        String[] status;
        long[] time;
        Output(int casenum){
            status = new String[casenum];
            time = new long[casenum];
        };
    }

    static class Case {
	Sample[] data;
	public class Sample{
	    int[] a;
	    int[] b;
	    int ans;
	}
	public Case() {}
    }
}
