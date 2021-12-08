
//Python Project: To retrieve the compensation retrieval system for people of different categories.


try:
    import os
    import string
    import csv

    #use the dictionary to fetch the numerical value related to respective word    
    number_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '12',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero' : '0'
    }

    #function to calculate the  compensation dollar amount
    def get_amount_compensation_cal(percent,first_amount,second_amount):
        amount=0
        amount=float(((percent/100)*(float(second_amount)-float(first_amount))))
        return amount
    
    #function to remove $ and unwanted characters in a number
    def get_split_amount_offering_calc(split_offering):
        first_amount=0
        if(split_offering.find("$")>-1):
            first_amount=split_offering.replace(',', '')
            if(split_offering[3].find("k")):
                first_amount=first_amount.replace('k', '000')
            first_amount=first_amount.replace('$', '')
        else:
            first_amount=split_offering.replace(',', '')          
        return float(first_amount)
    
    #function to calculate values based on the rule eg:- 8% for first 500k, 10 % for second 500k, 12 % for third 500k etc.
    def get_compensation_amount_dollars(compensation,offering_amt):
        percent_value_1=0
        percent_value_2=0
        percent_value_3=0
        final_amount=0
        split_compensation_line_1=''
        split_compensation_line_2=""
        split_compensation_line_3=""
        offering_amt=get_split_amount_offering_calc(offering_amt)
        if compensation.find("For")>-1:
            compensation=compensation.replace('(', '')
            compensation=compensation.replace(')', '')
            split_compensation_all_line=compensation.split("&")
            split_compensation_line_1=split_compensation_all_line[0].split()
            if(len(split_compensation_all_line)>1):
                split_compensation_line_2=split_compensation_all_line[1].split()
            if(len(split_compensation_all_line)>2):
                split_compensation_line_3=split_compensation_all_line[2].split()
                
            split_compensation_line_1[0]=split_compensation_line_1[0].replace('%', '')
            percent_value_1=float(split_compensation_line_1[0])
            if(split_compensation_line_1[3].find("-")>-1):
                first_amount_split = get_split_amount_offering_calc(split_compensation_line_1[4])
            else:
                first_amount_split = get_split_amount_offering_calc(split_compensation_line_1[3])
            if compensation.find("Between")>-1 or compensation.find("Above")>-1:
                split_compensation_line_2[0]=split_compensation_line_2[0].replace('%', '')
                percent_value_2=float(split_compensation_line_2[0])
            if split_compensation_line_3!="":
                split_compensation_line_3[0]=split_compensation_line_3[0].replace('%', '')
                percent_value_3=float(split_compensation_line_3[0])
            if(len(compensation)>=8):
                
                if(float(offering_amt)>float(first_amount_split)):  
                    final_amount=get_amount_compensation_cal(percent_value_1,0,first_amount_split)
                    if percent_value_2>0:
                        if compensation.find("Between")>-1:
                            second_amount_split=get_split_amount_offering_calc(split_compensation_line_2[3])
                            third_amount_split=get_split_amount_offering_calc(split_compensation_line_2[5])
                            final_amount+=get_amount_compensation_cal(percent_value_2,second_amount_split,third_amount_split)
                            if(float(offering_amt)>third_amount_split):
                                final_amount+=get_amount_compensation_cal(percent_value_3,third_amount_split,offering_amt)
                        else:
                            final_amount+=get_amount_compensation_cal(percent_value_2,first_amount_split,offering_amt) 
                else:
                    final_amount+=get_amount_compensation_cal(percent_value_1,0,offering_amt) 
            else:
                final_amount=get_amount_compensation_cal(percent_value_1,0,offering_amt) 
        
        elif compensation.find("Upto")>-1:
            compensation=compensation.replace('(', '')
            compensation=compensation.replace(')', '')
            split_compensation_all_line=compensation.split()
            first_amount_split = get_split_amount_offering_calc(split_compensation_all_line[2])
            split_compensation_all_line[0]=split_compensation_all_line[0].replace('%', '')
            percent_value_1=float(split_compensation_all_line[0])
            final_amount=get_amount_compensation_cal(percent_value_1,0,offering_amt) 
            if(final_amount>float(first_amount_split)):
                final_amount=first_amount_split
                
        elif compensation.find("No percentage is mentioned")>-1:
            final_amount=0
            
        elif compensation.find("%")>-1 or compensation.find("percent")>-1:
            compensation=compensation.replace('%', '')
            compensation=compensation.replace('<p>', '')
            compensation=compensation.replace('percent', '')
            percent_value_1=float(compensation)
            final_amount=get_amount_compensation_cal(percent_value_1,0,offering_amt)
            
            
        elif compensation.find("$")>-1:
            final_amount=0
              
        return final_amount
    
   #get the dollar amount value from the line of the tsv file
    def get_dollar_value_alone(line):
        variable_return=""
        dollar_str=line.find("$")
        fd_str=line[dollar_str:].split()
        variable_return=fd_str[0]
        return variable_return   

    #get the percent  value from the line of the tsv file
    def get_percent_value_alone(line):
        variable_returned=""
        per_str=line.find("percent")
        f_str=line[0:per_str+1].split()
        variable_returned=f_str[len(f_str)-2]
        variable_returned = number_dict.get(variable_returned) +"%"
        return variable_returned 
  
    #get percentage value for lines gaving % and percent as the substring in the line
    def get_percentage_line(line):
        variable_returned=""
        if(line.find("%")>-1):
            per_str=line.find("%")
            f_str=line[0:per_str+1].split()
            variable_returned=f_str[len(f_str)-1]
            variable_returned=variable_returned.replace("(", "")
        
        elif(line.find("percent")>-1):
            per_str=line.find("percent")
            f_str=line[0:per_str+1].split()
            variable_returned=f_str[len(f_str)-2]
            if(line.find("actually raised to be paid in cash")>-1):
                variable_returned = number_dict.get(variable_returned) +"%"
            else:
                variable_returned +="%"
            
        return variable_returned
    
    #prepare the string for % ranges- 8% for first 100k, 10% for second 100k etc for specific lines
    def get_percent_dollar_amt(splt_str,split_number):
        percent_value=""
        variable_returned=""
        if(len(splt_str)>0):
            per_str=splt_str.find("%")
            f_str=splt_str[0:per_str+1].split()
            percent_value=f_str[len(f_str)-1]
                
            dollar_str=splt_str.find("$")
            fd_str=splt_str[dollar_str:].split()
            if(percent_value!=""):
                variable_returned= percent_value +" (For "+ split_number +" "+fd_str[0]+")"
            else:
                variable_returned= fd_str[0]
        return variable_returned
    
    #prepare the string for % ranges- 8% for first 100k, 10% for second 100k etc   for specific lines
    def get_percent_dollar_amt_ranges(comma_splt_str,split_number):    
        index_string=comma_splt_str.split()
        percent_value=index_string[len(index_string)-1]
        percent_value=percent_value.replace("=", "")
        variable_returned=""
        if(comma_splt_str.find("$")>-1):
            dollar_str=comma_splt_str.find("$")
            fd_str=comma_splt_str[dollar_str:].split()
            
            if comma_splt_str.find("-")>-1:
                variable_returned= fd_str[0]+" - "+fd_str[2]
                if(percent_value!=""):
                    variable_returned= percent_value+ "% ("+ split_number +" "+variable_returned+")"
            else:
                variable_returned= fd_str[0].replace("+", "")
                if(percent_value!=""):
                    variable_returned= percent_value+ "% (For "+ split_number +" "+variable_returned +")"
            
        
        return variable_returned
    
    #get % for specific lines in tsv file
    def get_intermediary_dollar_amt(splt_str):
        if(splt_str.find("%")>-1):
            per_str=splt_str.find("%")
            f_str=splt_str[0:per_str+1].split()
            percent_value=f_str[len(f_str)-1]
            variable_returned=percent_value.replace('%', '')
        
        return variable_returned
    
    #get % and maximum compensation amount value when "Upto" is present in a line    
    def get_smbx_dollar_amt_percent(line_value):
        variable_returned=""
        if(line_value.find("%")>-1):
            per_str=line_value.find("%")
            f_str=line_value[0:per_str+1].split()
            percent_value=f_str[len(f_str)-1]
            variable_returned=percent_value
            
        if(line_value.find("$")>-1):
            dollar_str=line_value.find("$")
            fd_str=line_value[dollar_str:].split()
            variable_returned+=" (Upto "+fd_str[0]+")"   
        return variable_returned
        
    #fetch the path
    path_dir='C:/Users/karth/Documents/FORM_C_DISCLOSURE.tsv'   #fetch the file name from the directory
    fhandle = open(path_dir)
    sec_filing_detail_dict = dict()   #initialize the dictionary
    all_column_values=[]
    all_accession_number=[]
    offering_amount=""
    final_percent=""
    finance_interest_percent=""
    count=0
    
    #read all lines         
    for line in fhandle: 
        line=line.strip()      
        
        count+=1
        all_column_values = line.split('\t')#use strip to remove spaces
        if all_column_values[0]=="ACCESSION_NUMBER": #skip the first line as it has column names
            continue;

        if(len(all_column_values)>1):  # if no space/null is present for column values        
            
            # compensation_amount_line slicing 
            if all_column_values[1]!="":
                compensation_amount_line=all_column_values[1].lower()
                # if no "oofering" is present in the line then read and fetch percentage of the line as per the description of line
                if(compensation_amount_line.find("offering")<0):
                    if(compensation_amount_line.find("+")>-1):
                        if compensation_amount_line.find("on boarding fee +")>-1:    #unique line
                            splt_str=compensation_amount_line.split("+")
                            if(len(splt_str)==2):
                                per_str=splt_str[1].find("%")
                                f_str=splt_str[1][0:per_str+1].split()
                         #unique line
                        elif compensation_amount_line.find("onboarding fee +")>-1:
                            splt_str=compensation_amount_line.split("+")
                            if(len(splt_str)==3):
                                final_percent=get_percent_dollar_amt(splt_str[1],"First")+" & "+ get_percent_dollar_amt(splt_str[2],"Above")
                         #unique line
                        elif(len(splt_str)==2):
                            if compensation_amount_line.find("and up to")>-1:
                                third_split=splt_str[1].split("and up to")
                                final_percent=get_percent_dollar_amt(third_split[0],"First")+" & "+ get_percent_dollar_amt(third_split[1],"Above")
                         #unique line
                        elif compensation_amount_line.find("raised:")>-1:
                            splt_str=compensation_amount_line.split(":")
                            if splt_str[1].find("%")>-1:
                                comma_split=splt_str[1].split("%")
                                
                                final_percent=get_percent_dollar_amt_ranges(comma_split[0],"First")+" & "+ get_percent_dollar_amt_ranges(comma_split[1],"For Between")+" & "+ get_percent_dollar_amt_ranges(comma_split[2],"Above") 
                                
                         #unique line
                        elif compensation_amount_line.find("issuer's and intermediary's agreement.")>-1:
                            splt_str=compensation_amount_line.split("+")
                            final_percent="No percentage is mentioned"
                            
                         #unique line
                        elif compensation_amount_line.find("intermediary compensation ")>-1:
                            splt_str=compensation_amount_line.split("+")
                            final_percent_int=float(get_intermediary_dollar_amt(splt_str[0]))+float(get_intermediary_dollar_amt(splt_str[1]))
                            final_percent=str(final_percent_int)+"%"
                           
                    #unique line   
                    elif compensation_amount_line.find("smbx will be charging ")>-1:
                        final_percent=get_smbx_dollar_amt_percent(compensation_amount_line)
                        
                     #unique line
                    elif compensation_amount_line.find("intermediary will get paid ")>-1:
                        if compensation_amount_line.find("funds raised after")>-1:
                            first_line_split=compensation_amount_line.split("closing.")
                            final_percent=get_percent_dollar_amt(first_line_split[0],"First")+" & "+ get_percent_dollar_amt(first_line_split[1],"Above")
                            
                          #unique line   
                        elif compensation_amount_line.find("capped at")>-1:
                            final_percent=get_smbx_dollar_amt_percent(compensation_amount_line)
                            
                          #unique line       
                        else:
                            final_percent=get_percentage_line(compensation_amount_line)
                            
                    #unique line
                    elif compensation_amount_line.find("%")>-1:
                        final_percent=get_percentage_line(compensation_amount_line)
                        
                     #unique line
                    elif compensation_amount_line.find("percent")>-1:
                        final_percent=get_percentage_line(compensation_amount_line)
                        
                     #unique line
                    elif compensation_amount_line.find("$")>-1:
                        final_percent=get_dollar_value_alone(compensation_amount_line)
                        
            
                else:     
                    #if "offering"  is present in the line
                     #unique line
                    if(compensation_amount_line.find("applied at marginal rate based upon amount")>-1):
                        
                        splt_str=compensation_amount_line.split(":")
                        if splt_str[1].find("%")>-1:
                            comma_split=splt_str[1].split("%")
                                
                            final_percent=get_percent_dollar_amt_ranges(comma_split[0],"First")+" & "+ get_percent_dollar_amt_ranges(comma_split[1],"For Between")+" & "+ get_percent_dollar_amt_ranges(comma_split[2],"Above") 
                              
                      #unique line   
                    elif(compensation_amount_line.find("% to")>-1):
                        splt_str=compensation_amount_line.split("% to")
                        final_percent=get_percentage_line(splt_str[1])
                        
                      #unique line   
                    elif(compensation_amount_line.find("%-")>-1):
                        splt_str=compensation_amount_line.split("%-")
                        final_percent=get_percentage_line(splt_str[1])
                        
                     #unique line
                    elif compensation_amount_line.find("smbx will be charging")>-1:
                        final_percent=get_smbx_dollar_amt_percent(compensation_amount_line)
                        
                       #unique line  
                    elif compensation_amount_line.find("%")>-1:
                        final_percent=get_percentage_line(compensation_amount_line)
                        
                      #unique line   
                    elif compensation_amount_line.find("percent")>-1:
                        final_percent=get_percent_value_alone(compensation_amount_line)
                        
                      #unique line   
                    elif compensation_amount_line.find("until the offering is concluded.")>-1:
                            final_percent="No percentage is mentioned"
                            
                     #unique line
                    elif compensation_amount_line.find("$")>-1:
                        final_percent=get_dollar_value_alone(compensation_amount_line)
                        
            
            # compensation_amount_line slicing              //fetch the value of financial interest if "%" or "percent" is present in the column value
            if(all_column_values[2]!=""):
                financial_interest_line= all_column_values[2].lower()
                if(financial_interest_line!=""):
                    if financial_interest_line.find("%")>-1:
                        finance_interest_percent=get_percentage_line(financial_interest_line)
                        
                    
                    elif financial_interest_line.find("percent")>-1:
                        finance_interest_percent=get_percent_value_alone(financial_interest_line)
                        
                    else:
                        finance_interest_percent="No percentage is mentioned"
                        
                        
            if(all_column_values[8]!=""):           #fetch offering amount
                offering_amount=all_column_values[8]
                   
            
            sec_filing_detail_dict[all_column_values[0]] = final_percent,finance_interest_percent,offering_amount #populate dictionary with all values
        else:
            sec_filing_detail_dict[all_column_values[0]] = final_percent,finance_interest_percent,offering_amount
        
        all_accession_number.append(all_column_values[0]) #add data of accession number to list
        
    
  
    #write the output to a tsv file
    with open('C:/Users/karth/Documents/output.tsv', 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['ACCESSION_NUMBER', 'COMPENSATION_AMOUNT','FINANCIAL_INTEREST','OFFERING_AMOUNT','COMPENSATION_AMOUNT(Dollars)'])
        #run a loop to get the lines as per the order in original data
        for id in all_accession_number:
            #get values related to the  accession number from dictionary
            percent_value,finance_interest_value,offering_amount_value= sec_filing_detail_dict.get(id, (0,0,0)) 
            
            calculation=get_compensation_amount_dollars(percent_value,offering_amount_value)
            
            percent_value=percent_value.replace("<p>","")
            if(percent_value.find("%"))<0:
                percent_value="No percentage is mentioned"
            #write to file
            tsv_writer.writerow([id,percent_value,finance_interest_value,offering_amount_value,calculation])
            

    #print(each line) of output after populating output liens in tsv file
    path_dir='C:/Users/karth/Documents/output.tsv'   #fetch the file name from the directory
    fhandle = open(path_dir)
    for line in fhandle:
        print(line)
        
except Exception as e:
    print("Error occurred during execution.Please Retry.", e)