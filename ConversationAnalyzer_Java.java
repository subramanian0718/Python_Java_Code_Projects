import java.io.*;  //import requiries libraries
import java.util.Map;
import java.util.HashMap;
import java.util.Scanner;

public class ConversationAnalyzerAssignment {
	public static void main(String[] args) {
        String file_name="";                    
    try {               
            Scanner userInput = new Scanner(System.in);         //required to read the file input
            System.out.println("Enter file name: ");       
            file_name= userInput.nextLine();
            BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\karth\\Documents\\601_tech fundamental\\"+file_name));
            Participant participant[] = new Participant[5];         //initialize the participant class
            HashMap <String, Participant> participant_mapper = new HashMap<String, Participant>();  //map required to store the values of all the participant object
            String[] name_list=new String[5];                       //array for storing file related participant names

            if(file_name.equalsIgnoreCase("SBC002.TXT")){               //participant for file sbc002.txt
                name_list[0]="JAMIE";
                name_list[1]="HAROLD";
                name_list[2]="MILES";
                name_list[3]="PETE";
                name_list[4]=">ENV";
            }else if(file_name.equalsIgnoreCase("SBC031.TXT")){        //participant for file sbc0031.txt
                name_list[0]="SHERRY";
                name_list[1]="BETH";
                name_list[2]="ROSEMARY";
                name_list[3]=">ENV";
                name_list[4]="JAMIE";
            }else{
                System.out.println("Please enter either SBC002.TXT OR SBC031.TXT as file name in input.") ;
                // Terminate JVM
                System.exit(0);                                       //else condition to terminate the program if the above file names are not entered
            }

            for (int index_value = 0; index_value < 5; index_value++) {                         //put the enteries into Map and create object of a class
                participant[index_value]=new Participant(name_list[index_value]);
                participant_mapper.put(name_list[index_value],participant[index_value]);
            }
        
            
            //declare all relevant variables
            Participant participant_detail = new Participant();
            String[] words,time_name_words,no_name_words,each_particiant_detail;
            String no_punctuations,current_speaker_name, final_particiant_detail,inputline;;
            current_speaker_name="";

            //read each line from file               
            while((inputline = br.readLine())!=null) {
                inputline=inputline.strip();
                time_name_words = inputline.split("\\s+",4);        //split each line into 4 parts for seconds, speaker name & words spoken
                

                if(time_name_words.length>2){                           //only if line has more than 2 parts
                    if(time_name_words[2].contains(":") && time_name_words.length>3){           //only if line contains speaker name
                        for (Participant p:participant){                
                                if(time_name_words[2].contains(p.getName()+":")) {
                                    no_punctuations = time_name_words[3].replaceAll("\\p{Punct}","");                   //remove unnecessary punctuation
                                    p.addSecondsSpoken(Float.parseFloat(time_name_words[1]),Float.parseFloat(time_name_words[0]));   //add seconds spoken
                                    p.addTimeSpoken();                                                                  //add tomes spoken
                                    no_punctuations=no_punctuations.strip();                                            //remove spaces
                                    if(no_punctuations!="" ){
                                        words= no_punctuations.split("\\s+");                                           //split the words to count them
                                        p.addwordsSpoken(words.length);                                                 //count the words
                                        
                                    }
                                    current_speaker_name=p.getName();                       //store the name of current speaker Extra credit (1 point):                                                                                            
                                    break;                                                  
                                }
                        }

                    }else{                                                             //it counts continuing lines where participant names are not mentioned (or lines that do not contain ':')
                            no_name_words=inputline.split("\\s+",3);                        //split the input line as it might have only words spoke
                            no_punctuations = no_name_words[2].replaceAll("\\p{Punct}","");     //remove punctuations
                            no_punctuations=no_punctuations.strip();
                            participant_detail= participant_mapper.get(current_speaker_name);       //use map to retrieve the latest speaker object using the speaker name that was stored initially
                            if(no_punctuations!="" ){
                                words=no_punctuations.split("\\s+");           
                                participant_detail.addwordsSpoken(words.length);                //add the word count
                             }
                            participant_detail.addSecondsSpoken(Float.parseFloat(no_name_words[1]),Float.parseFloat(no_name_words[0]));     //add seconds count
                    }
            }
            }
            

            //Print the output in tabular format.
            System.out.println("---------------------------------------------------------------------------------------------------------------------------");
            System.out.printf("%10s %30s %25s %30s", "Name of Participant", "Times Spoken (Count)", "Seconds Spoken", "Number of Words Spoken"); //table header columns
            System.out.println();
            System.out.println("---------------------------------------------------------------------------------------------------------------------------");
            for (Participant p:participant){
                    final_particiant_detail=p.print();
                    each_particiant_detail=final_particiant_detail.split("--");  //retrieve the entire string and split the same and display in table
                    System.out.format("%10s %30s %30s %23s",each_particiant_detail[0],each_particiant_detail[1],each_particiant_detail[2],each_particiant_detail[3]);
                    System.out.println();
                }
            System.out.println("---------------------------------------------------------------------------------------------------------------------------");
            

        }
        catch (FileNotFoundException ex) {
            System.out.println("File  - " + file_name + " - cannot be opened. "+ex);       //error in case file name NOT PRESENT IN DIRECTORY or wrong values are ENTERED
        }
        catch (Exception e) {
            System.out.println("Error occurred during execution.Please Retry. "+e.toString()); //print exception if any
        }
        
    }

}


 class Participant {                                             //create class of Participant

    private int times_spoken;                                    //declaRe class variables
    private float seconds_spoken;
    private String speaker_name;
    private int number_of_words;

    Participant(){

        this("None");
    }

   public void addTimeSpoken(){                                                 //function to add count of speaker
      times_spoken++;
    }


    public void addSecondsSpoken(float final_second, float initial_second){     //function to add seconds spoken by speaker
        float total_seconds=final_second - initial_second;
        seconds_spoken+=total_seconds;
    }

    public void addwordsSpoken(int words_length){                               //function to add words spoken by speaker
        number_of_words+=words_length;
    }

    public String getName(){                                                    //function to get name of speaker 
        return speaker_name;
    }


    public String print(){                                                      //function to print final values of each participant object
       return speaker_name +"--"+ times_spoken +"--"+ seconds_spoken +"--"+number_of_words;

    }

    Participant(String name){                                                   //contructor called to create an object and initialize all variables
        speaker_name=name;
        number_of_words=0;
        times_spoken=0;
        seconds_spoken=0;
    }



}