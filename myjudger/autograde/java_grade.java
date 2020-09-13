import com.google.gson.Gson;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.Writer;
import java.io.IOException;
import java.util.Arrays; 
/*
javac -cp algs4.jar:gson.jar myjava_grade.java Solution.java
java -cp gson.jar:algs4.jar:. myjava_grade {casename}
*/

public class java_grade {
    // Edit here
    static boolean compare(int[] out, Sample s) {
        return Arrays.equals(out, s.answer);
    }

    static int[] run(Sample s) {
        return new Solution().twoSum(s.nums, s.target);
        // return s.answer;
    }

    static class Sample {
        int[] nums;
        int target;
        int[] answer;
        public Sample() {}
    }

    // Don't edit below
    public static void main(String[] args) {
        Gson gson = new Gson();
        long clk_s;
	long timeout_limit = 800;

	// read input
        try {
            Sample[] samples = gson.fromJson(new FileReader(args[0] + ".in"), Sample[].class);
            int casenum = samples.length;

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
		    int[] out = run(samples[sample]);
                    output.time[sample] = System.currentTimeMillis() - clk_s;

                    if (compare(out, samples[sample])) {
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
}
