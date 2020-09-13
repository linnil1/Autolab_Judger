import java.util.Arrays; 
import java.lang.Thread;
public class Solution {
    public int test(int[] a, int[] b) {
	   
    	//try{
    	//	Thread.sleep(7000);
    	//}
    	//catch(InterruptedException e){
	//}
    	
        return Arrays.stream(a).max().getAsInt() +
               Arrays.stream(b).min().getAsInt();
    }
}
