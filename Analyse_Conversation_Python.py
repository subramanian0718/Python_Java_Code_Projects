//Pthon project: Take any coversation file involving speakers and prin the statistics like name, number of time spoken and numberr of words.etc
#functiopn to get the list of words from a line after split
def get_word_count(line):    
    try:
        words_without_punctuation= line.translate(str.maketrans('', '', string.punctuation))  #remove puntuations
        words_list=words_without_punctuation.split()
        return words_list
    except:
        words_list=[]
        print("Error reading words from the line", line)        
        return words_list
    
#function to get the time taken for the words spoken by each speaker
def get_time_spoken(sentence:str):
    try:
        timestamps = sentence.split(maxsplit=2)
        speaker_time_per_line = float(timestamps[1]) - float(timestamps[0])  #find difference between start and end time of each line
        return speaker_time_per_line
    except:
        print("Error reading timestamps", sentence)
        return 0

#function to get the speech rate and average number of words per conversation snippet
def speech_rate_average_words(dict_values):
    try:        
        speech_rate_value=0     #intialize to 0 so that speech rate is calculated only if the time spoken is > 0
        if(dict_values[1]>0):
            speech_rate_value=dict_values[2]/(dict_values[1]/60)   #find speech rate per minute
                
        avg_words=dict_values[2]/(dict_values[0])    #find the average no of words
        return speech_rate_value,avg_words
    except:
        print("Error while calculating speech rate and average number of words", dict_values)
        return 0,0
    
try:
    import os
    import string
    fname = input("Enter file name: ")
    path_dir='C:/Users/karth/Documents/601_tech fundamental/'+fname   #fetch the file name from the directory
    fhandle = open(path_dir)
    speaker_detail_dict = dict()   #initialize the dictionary
    no_words_line=[]                #initalize the list which contains words per line after split
    
    for line in fhandle: 
        line=line.strip()           #use strip to remove spaces
        time_name_words = line.split(maxsplit=3)                #max split by 3 to fetch the timestamps,speaker and his speech            
        if(len(time_name_words)>2):                             #make sure the line has words other than just only 2 timestamps                
            if (len(time_name_words)>3 and ":" in time_name_words[2]):      #find the : after maxsplit to find speaker
                current_speaker=time_name_words[2]
                no_words_line=get_word_count(time_name_words[3])                #fecth the words
            else: 
                no_words_line=get_word_count(time_name_words[2])                #fetch the words in case there is no speaker name present
                if(len(time_name_words)>3):                                     #fetch the remaining part of the words in line if present after split
                    rest_of_words=get_word_count(time_name_words[3])
                    if(len(rest_of_words)>0):
                        no_words_line.extend(rest_of_words)                     #add to the existing list of words
                                                        
            speak_num, speak_time,speak_num_words = speaker_detail_dict.get(current_speaker, (0,0,0))  #retreieve the speaker detail
                
            if(":" in time_name_words[2]):
                speak_num+=1

            speaker_detail_dict[current_speaker] = speak_num, speak_time + get_time_spoken(line),speak_num_words+len(no_words_line) #add updated detail of speaker as a tuple

    dash = '-' * 150   #dash to display the column headers
    print(dash)
    print('{:<13s}{:>17s}{:>19s}{:>27s}{:>15s}{:>53s}'.format("Name of Participant","Times Spoken"," Seconds Spoken","Number of Words Spoken","Speech Rate"," Average number of words per conversation snippet"))
    print(dash)

    for key_dict,value_dict  in   speaker_detail_dict.items():  #run a loop to prin the deatils of each speaker
        key_dict=key_dict.replace(":", '')
        speech_rate,avg_num_words=speech_rate_average_words(value_dict)   #fetch the speech rate and average no of words
        print('{:^13s}{:>17d}{:>22f}{:^33d}{:>10.5f}{:^53f}'.format(key_dict, value_dict[0],value_dict[1],value_dict[2],speech_rate,avg_num_words))
        

    fhandle.close()

except FileNotFoundError:                        #print exception if present
    print("File cannot be opened: "+fname)
except:
    print("Error occurred during execution.Please Retry.")